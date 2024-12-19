# Import necessary modules
from datetime import datetime  # For tracking transaction timestamps
import threading  # To handle concurrent operations safely

# Class representing a transaction graph
class TransactionGraph:
    def __init__(self):
        # Adjacency list to represent the graph: 
        # {account_number: [(connected_account, transaction_details)]}
        self.adjacency_list = {}
        self.lock = threading.Lock()  # Ensure thread-safe access

    def add_transaction(self, from_account_number, to_account_number, amount, transaction_type):
        """Add a new transaction to the graph"""
        with self.lock:  # Lock to ensure thread-safe operations
            # Initialize adjacency lists for accounts if they don't exist
            if from_account_number not in self.adjacency_list:
                self.adjacency_list[from_account_number] = []
            if to_account_number not in self.adjacency_list:
                self.adjacency_list[to_account_number] = []

            # Create a transaction detail dictionary
            transaction_detail = {
                'amount': amount,
                'timestamp': datetime.now(),  # Record the current time
                'type': transaction_type  # Type of transaction (e.g., transfer)
            }

            # Add transaction details to both the sender and receiver's adjacency lists
            self.adjacency_list[from_account_number].append((to_account_number, transaction_detail))
            self.adjacency_list[to_account_number].append((from_account_number, transaction_detail))

    def transfer_between_accounts(self, from_account, to_account, amount, transaction_processor):
        """Handle transfer between two accounts"""
        try:
            if from_account.balance >= amount:  # Ensure sufficient funds
                # Create a withdrawal transaction for the sender
                withdraw_transaction = {
                    'type': 'withdraw',
                    'amount': amount,
                    'description': f"Transfer to {to_account.account_number}",
                    'account': from_account,
                    'account_type': from_account.account_type,
                    'timestamp': datetime.now()
                }
                
                # Create a deposit transaction for the receiver
                deposit_transaction = {
                    'type': 'deposit',
                    'amount': amount,
                    'description': f"Transfer from {from_account.account_number}",
                    'account': to_account,
                    'account_type': to_account.account_type,
                    'timestamp': datetime.now()
                }

                # Add both transactions to the transaction processor for handling
                transaction_processor.add_transaction(withdraw_transaction)
                transaction_processor.add_transaction(deposit_transaction)

                # Add the transfer details to the transaction graph
                self.add_transaction(
                    from_account.account_number,
                    to_account.account_number,
                    amount,
                    "transfer"
                )
                return True  # Transfer succeeded
            else:
                # Insufficient funds
                print(f"Insufficient funds. Available balance: {from_account.balance}, Required: {amount}")
                return False
        except Exception as e:
            # Handle any errors during the transfer
            print(f"Error during transfer: {str(e)}")
            return False

    def get_account_connections(self, account_number):
        """Get all connections for an account"""
        # Retrieve all connected accounts and transaction details for the given account
        return self.adjacency_list.get(account_number, [])

    def detect_circular_transactions(self, account_number, threshold_hours=24):
        """Detect if there are circular transactions within the last 24 hours"""
        visited = set()  # Set to track visited accounts
        path = []  # Track the current DFS path
        
        def dfs(current_account, start_time):
            # Mark the current account as visited
            visited.add(current_account)
            path.append(current_account)
            
            # Explore all connected accounts
            for connected_account, transaction in self.adjacency_list.get(current_account, []):
                # Check if the transaction is within the time threshold
                if (datetime.now() - transaction['timestamp']).total_seconds() / 3600 <= threshold_hours:
                    if connected_account in path:
                        # Found a cycle: extract and return the cycle
                        cycle_start = path.index(connected_account)
                        return path[cycle_start:]
                    if connected_account not in visited:
                        # Recursive DFS call for unvisited accounts
                        result = dfs(connected_account, start_time)
                        if result:
                            return result
            
            # Backtrack: remove the account from the current path
            path.pop()
            return None

        # Start DFS from the given account
        return dfs(account_number, datetime.now())

    def get_transaction_volume(self, account_number, hours=24):
        """Get total transaction volume for an account in the last 24 hours"""
        total_volume = 0  # Initialize the total transaction volume
        if account_number in self.adjacency_list:
            current_time = datetime.now()  # Record the current time
            # Iterate over all transactions for the account
            for _, transaction in self.adjacency_list[account_number]:
                # Check if the transaction is within the time threshold
                if (current_time - transaction['timestamp']).total_seconds() / 3600 <= hours:
                    total_volume += transaction['amount']  # Add the transaction amount
        return total_volume  # Return the total volume
