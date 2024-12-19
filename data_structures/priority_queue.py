# Import necessary modules
from queue import PriorityQueue  # Priority-based queue to handle transactions
from dataclasses import dataclass, field  # Simplify creation of data structures
from typing import Any  # Allows using generic types

# For generating unique transaction IDs and simulating delays
import uuid  
import time  
import threading  # For concurrent transaction processing

# Define a data class for prioritized transactions
@dataclass(order=True)
class PrioritizedTransaction:
    # Priority of the transaction (lower value = higher priority)
    priority: int
    # The actual transaction data (not used for ordering)
    transaction: Any = field(compare=False)
    # Unique identifier for each transaction
    id: str = field(default_factory=lambda: str(uuid.uuid4()), compare=False)

# Class to handle transaction processing
class TransactionProcessor:
    def __init__(self):
        # Priority queue to hold transactions based on their priority
        self.transaction_queue = PriorityQueue()
        # List to track pending transactions (not yet processed)
        self.pending_transactions = []
        # Lock to ensure thread-safe operations
        self.lock = threading.Lock()

    # Method to calculate the priority of a transaction
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

    # Method to add a transaction to the queue
    def add_transaction(self, transaction):
        print(f"Adding transaction: {transaction}")
        with self.lock:  # Ensure thread-safe access
            # Calculate the transaction's priority
            priority = self.calculate_priority(transaction)
            # Wrap the transaction in a PrioritizedTransaction object
            prioritized_transaction = PrioritizedTransaction(
                priority=priority,
                transaction=transaction
            )
            # Add the transaction to the priority queue
            self.transaction_queue.put(prioritized_transaction)
            # Track it in the pending transactions list
            self.pending_transactions.append(prioritized_transaction)
        
        print(f"Transaction added: {transaction}")  # Debugging message

    # Start the processing thread for transactions
    def start_processing(self):
        self.is_processing = True  # Set the processing flag
        self.processing_thread = threading.Thread(target=self.process_transactions)
        self.processing_thread.daemon = True  # Allows the thread to exit with the main program
        self.processing_thread.start()  # Start the background thread

    # Process transactions from the queue
    def process_transactions(self):
        print("Processing transactions...")
        while self.is_processing:  # Keep processing while the flag is true
            try:
                with self.lock:  # Ensure thread-safe access
                    if not self.transaction_queue.empty():  # Check if there are transactions in the queue
                        # Get the highest-priority transaction
                        prioritized_transaction = self.transaction_queue.get_nowait()
                        # Process the transaction
                        self._process_single_transaction(prioritized_transaction.transaction)
                        self.transaction_queue.task_done()  # Mark the task as done

                time.sleep(0.1)  # Prevent CPU overuse
            except Exception as e:  # Catch and log errors
                print(f"Error processing transaction: {e}")
                time.sleep(0.1)  # Add delay to handle errors gracefully

    # Process a specific transaction from the pending list by its ID
    def process_pending_transaction(self, transaction_id):
        with self.lock:  # Ensure thread-safe access
            # Iterate over the pending transactions
            for i, pt in enumerate(self.pending_transactions):
                if pt.id == transaction_id:  # Match transaction by its unique ID
                    transaction = pt.transaction
                    # Process the transaction
                    self._process_single_transaction(transaction)
                    # Remove it from the pending list
                    del self.pending_transactions[i]
                    print(f"Processed transaction: {transaction}")
                    break

    # Retrieve all pending transactions without disrupting the queue order
    def pending_transactions(self):
        pending = []  # List to hold pending transactions
        temp_queue = PriorityQueue()  # Temporary queue to restore order
        
        # Transfer transactions from the queue to the temporary list
        while not self.transaction_queue.empty():
            transaction = self.transaction_queue.get()
            pending.append(transaction)
            temp_queue.put(transaction)
            
        # Restore transactions to the main queue
        while not temp_queue.empty():
            self.transaction_queue.put(temp_queue.get())
            
        return pending

    # Internal method to process a single transaction
    def _process_single_transaction(self, transaction):
        account = transaction['account']  # Get the account associated with the transaction

        # Handle deposit transactions
        if transaction['type'] == 'deposit':
            account.update_balance(transaction['amount'], 'deposit')
        # Handle withdrawal transactions
        elif transaction['type'] == 'withdraw':
            if account.balance >= transaction['amount']:  # Check for sufficient balance
                account.update_balance(transaction['amount'], 'withdraw')
            else:
                print(f"Insufficient balance for transaction: {transaction}")
                return  # Exit if funds are insufficient
        
        # Log the transaction in the account's history
        account.add_transaction(
            transaction['type'],
            transaction['amount'],
            transaction['description']
        )

        print(f"Processed transaction: {transaction}")  # Debugging message
