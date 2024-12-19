from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any


import uuid
import time
import threading


@dataclass(order=True)
class PrioritizedTransaction:
    priority: int
    transaction: Any = field(compare=False)
    id: str = field(default_factory=lambda: str(uuid.uuid4()), compare=False)

class TransactionProcessor:
    def __init__(self):
        self.transaction_queue = PriorityQueue()
        self.pending_transactions = []
        self.lock = threading.Lock()

    def calculate_priority(self, transaction):
        # Priority levels (lower number = higher priority):
        # 1: VIP accounts or high-value transactions (>$10000)
        # 2: Medium-value transactions ($1000-$10000)
        # 3: Regular transactions (<$1000)
        
        amount = transaction['amount']
        account_type = transaction['account_type']
        
        if account_type == 'VIP' or amount > 10000:
            return 1
        elif 1000 <= amount <= 10000:
            return 2
        else:
            return 3

    def add_transaction(self, transaction):
        print(f"Adding transaction: {transaction}")
        with self.lock:
            priority = self.calculate_priority(transaction)
            prioritized_transaction = PrioritizedTransaction(
                priority=priority,
                transaction=transaction
            )
            self.transaction_queue.put(prioritized_transaction)
            self.pending_transactions.append(prioritized_transaction)
        
        print(f"Transaction added: {transaction}") #Debug
        

    def start_processing(self):
        self.process_transactions()
        self.is_processing = True
        self.processing_thread = threading.Thread(target=self.process_transactions)
        self.processing_thread.daemon = True
        self.processing_thread.start()

    def process_transactions(self):
        print("Processing transactions...")
        while self.is_processing:
            try:
                with self.lock:
                    if not self.transaction_queue.empty():
                        prioritized_transaction = self.transaction_queue.get_nowait()
                        self._process_single_transaction(prioritized_transaction.transaction)
                        self.transaction_queue.task_done()

                time.sleep(0.1)  # Prevent CPU overuse
            except Exception as e:
                print(f"Error processing transaction: {e}")
                time.sleep(0.1)

    def process_pending_transaction(self, transaction_id):
        with self.lock:
            for i, pt in enumerate(self.pending_transactions):
                if pt.id == transaction_id:
                    transaction = pt.transaction
                    self._process_single_transaction(transaction)
                    del self.pending_transactions[i]
                    print(f"Processed transaction: {transaction}")
                    break

    def pending_transactions(self):
        pending = []
        temp_queue = PriorityQueue()
        
        while not self.transaction_queue.empty():
            transaction = self.transaction_queue.get()
            pending.append(transaction)
            temp_queue.put(transaction)
            
        # Restore queue
        while not temp_queue.empty():
            self.transaction_queue.put(temp_queue.get())
            
        return pending

    def _process_single_transaction(self, transaction):
        account = transaction['account']

        if transaction['type'] == 'deposit':
            account.update_balance(transaction['amount'], 'deposit')
        elif transaction['type'] == 'withdraw':
            if account.balance >= transaction['amount']:
                account.update_balance(transaction['amount'], 'withdraw')
            else:
                print(f"Insufficient balance for transaction: {transaction}")
                return
        
        account.add_transaction(
            transaction['type'],
            transaction['amount'],
            transaction['description']
        )

        print(f"Processed transaction: {transaction}")