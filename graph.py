from datetime import datetime
import threading

class TransactionGraph:
    def __init__(self):
        self.adjacency_list = {}  # {account_number: [(connected_account, transaction_details)]}
        self.lock = threading.Lock()

    def add_transaction(self, from_account_number, to_account_number, amount, transaction_type):
        """Add a new transaction to the graph"""
        with self.lock:
            # Initialize lists if they don't exist
            if from_account_number not in self.adjacency_list:
                self.adjacency_list[from_account_number] = []
            if to_account_number not in self.adjacency_list:
                self.adjacency_list[to_account_number] = []

            # Add transaction details to both accounts
            transaction_detail = {
                'amount': amount,
                'timestamp': datetime.now(),
                'type': transaction_type
            }

            self.adjacency_list[from_account_number].append((to_account_number, transaction_detail))
            self.adjacency_list[to_account_number].append((from_account_number, transaction_detail))

    def transfer_between_accounts(self, from_account, to_account, amount, transaction_processor):
        """Handle transfer between two accounts"""
        try:
            if from_account.balance >= amount:
                # Create withdrawal transaction
                withdraw_transaction = {
                    'type': 'withdraw',
                    'amount': amount,
                    'description': f"Transfer to {to_account.account_number}",
                    'account': from_account,
                    'account_type': from_account.account_type,
                    'timestamp': datetime.now()
                }
                
                # Create deposit transaction
                deposit_transaction = {
                    'type': 'deposit',
                    'amount': amount,
                    'description': f"Transfer from {from_account.account_number}",
                    'account': to_account,
                    'account_type': to_account.account_type,
                    'timestamp': datetime.now()
                }

                # Add transactions to processor
                transaction_processor.add_transaction(withdraw_transaction)
                transaction_processor.add_transaction(deposit_transaction)

                # Add to transaction graph using account numbers
                self.add_transaction(
                    from_account.account_number,
                    to_account.account_number,
                    amount,
                    "transfer"
                )
                return True
            else:
                print(f"Insufficient funds. Available balance: {from_account.balance}, Required: {amount}")
                return False
        except Exception as e:
            print(f"Error during transfer: {str(e)}")
            return False

    def get_account_connections(self, account_number):
        """Get all connections for an account"""
        return self.adjacency_list.get(account_number, [])

    def detect_circular_transactions(self, account_number, threshold_hours=24):
        """Detect if there are circular transactions within the last 24 hours"""
        visited = set()
        path = []
        
        def dfs(current_account, start_time):
            visited.add(current_account)
            path.append(current_account)
            
            for connected_account, transaction in self.adjacency_list.get(current_account, []):
                if (datetime.now() - transaction['timestamp']).total_seconds() / 3600 <= threshold_hours:
                    if connected_account in path:
                        # Found a cycle
                        cycle_start = path.index(connected_account)
                        return path[cycle_start:]
                    if connected_account not in visited:
                        result = dfs(connected_account, start_time)
                        if result:
                            return result
            
            path.pop()
            return None

        return dfs(account_number, datetime.now())

    def get_transaction_volume(self, account_number, hours=24):
        """Get total transaction volume for an account in the last 24 hours"""
        total_volume = 0
        if account_number in self.adjacency_list:
            current_time = datetime.now()
            for _, transaction in self.adjacency_list[account_number]:
                if (current_time - transaction['timestamp']).total_seconds() / 3600 <= hours:
                    total_volume += transaction['amount']
        return total_volume