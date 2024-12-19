from datetime import datetime

# BST for Account Management
class BankAccount:
    def __init__(self, account_number, owner_username, account_type="Regular", balance=0):
        self.account_number = account_number
        self.owner_username = owner_username
        self.account_type = account_type  # "Regular" or "VIP"
        self.balance = balance
        self.transaction_history = []
        self.creation_date = datetime.now()
        self.pending_transactions = []

    def add_transaction(self, transaction_type, amount, description):
        transaction = {
            'type': transaction_type,
            'amount': amount,
            'description': description,
            'timestamp': datetime.now(),
            'status': 'completed',
            'priority': 3 if self.account_type == "Regular" else 1
        }
        self.transaction_history.append(transaction)

    def update_balance(self, amount, transaction_type):
        if transaction_type == "deposit":
            self.balance += amount
        elif transaction_type == "withdraw":
            self.balance -= amount

        print(f"Updated balance: {self.balance}") #Debug

class BSTNode:
    def __init__(self, account):
        self.account = account
        self.left = None
        self.right = None

class BankAccountBST:
    def __init__(self):
        self.root = None
    
    def insert(self, account):
        if not self.root:
            self.root = BSTNode(account)
        else:
            self._insert_recursive(self.root, account)
    
    def _insert_recursive(self, node, account):
        if account.account_number < node.account.account_number:
            if node.left is None:
                node.left = BSTNode(account)
            else:
                self._insert_recursive(node.left, account)
        else:
            if node.right is None:
                node.right = BSTNode(account)
            else:
                self._insert_recursive(node.right, account)
    
    def find_account(self, account_number):
        return self._find_recursive(self.root, account_number)
    
    def _find_recursive(self, node, account_number):
        if node is None or node.account.account_number == account_number:
            return node.account if node else None
            
        if account_number < node.account.account_number:
            return self._find_recursive(node.left, account_number)
        return self._find_recursive(node.right, account_number)
    
    def get_user_accounts(self, username):
        accounts = []
        self._get_user_accounts_recursive(self.root, username, accounts)
        return accounts
    
    def _get_user_accounts_recursive(self, node, username, accounts):
        if node:
            if node.account.owner_username == username:
                accounts.append(node.account)
            self._get_user_accounts_recursive(node.left, username, accounts)
            self._get_user_accounts_recursive(node.right, username, accounts)