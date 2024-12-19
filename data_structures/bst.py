from datetime import datetime  # Importing datetime to handle timestamps for accounts and transactions

# Class representing a bank account
class BankAccount:
    def __init__(self, account_number, owner_username, account_type="Regular", balance=0):
        # Initializing basic account attributes
        self.account_number = account_number  # Unique identifier for the account
        self.owner_username = owner_username  # Username of the account owner
        self.account_type = account_type  # Type of account: "Regular" or "VIP"
        self.balance = balance  # Initial account balance
        self.transaction_history = []  # List to store all transactions associated with the account
        self.creation_date = datetime.now()  # Timestamp of account creation
        self.pending_transactions = []  # Transactions awaiting processing

    def add_transaction(self, transaction_type, amount, description):
        """Add a new transaction to the account's history"""
        transaction = {
            'type': transaction_type,  # Type of transaction: deposit or withdraw
            'amount': amount,  # Amount involved in the transaction
            'description': description,  # Description of the transaction
            'timestamp': datetime.now(),  # Timestamp of when the transaction occurred
            'status': 'completed',  # Status of the transaction
            'priority': 3 if self.account_type == "Regular" else 1  # Priority based on account type
        }
        self.transaction_history.append(transaction)  # Add transaction to history

    def update_balance(self, amount, transaction_type):
        """Update the account balance based on the transaction type"""
        if transaction_type == "deposit":
            self.balance += amount  # Increase balance for deposits
        elif transaction_type == "withdraw":
            self.balance -= amount  # Decrease balance for withdrawals

        print(f"Updated balance: {self.balance}")  # Debugging: Print updated balance

# Node class for Binary Search Tree (BST)
class BSTNode:
    def __init__(self, account):
        # Initialize a node with a bank account and references to left and right child nodes
        self.account = account  # BankAccount instance
        self.left = None  # Left child node
        self.right = None  # Right child node

# Binary Search Tree for managing bank accounts
class BankAccountBST:
    def __init__(self):
        # Initialize an empty BST
        self.root = None

    def insert(self, account):
        """Insert a new account into the BST"""
        if not self.root:
            # If tree is empty, set the root to a new node containing the account
            self.root = BSTNode(account)
        else:
            # Otherwise, recursively find the correct position and insert
            self._insert_recursive(self.root, account)

    def _insert_recursive(self, node, account):
        """Helper function to insert an account recursively"""
        if account.account_number < node.account.account_number:
            # Go left if the account number is less than the current node's account number
            if node.left is None:
                node.left = BSTNode(account)  # Create a new node if left child is empty
            else:
                self._insert_recursive(node.left, account)  # Recurse to the left subtree
        else:
            # Go right if the account number is greater or equal
            if node.right is None:
                node.right = BSTNode(account)  # Create a new node if right child is empty
            else:
                self._insert_recursive(node.right, account)  # Recurse to the right subtree

    def find_account(self, account_number):
        """Find and return an account by account number"""
        return self._find_recursive(self.root, account_number)

    def _find_recursive(self, node, account_number):
        """Helper function to search for an account recursively"""
        if node is None or node.account.account_number == account_number:
            # Base case: If node is None or account found, return the account
            return node.account if node else None

        if account_number < node.account.account_number:
            # Search the left subtree if account number is smaller
            return self._find_recursive(node.left, account_number)
        return self._find_recursive(node.right, account_number)  # Search the right subtree otherwise

    def get_user_accounts(self, username):
        """Get all accounts owned by a specific user"""
        accounts = []  # List to collect user's accounts
        self._get_user_accounts_recursive(self.root, username, accounts)  # Recursive helper call
        return accounts

    def _get_user_accounts_recursive(self, node, username, accounts):
        """Helper function to find all accounts owned by a user recursively"""
        if node:
            if node.account.owner_username == username:
                # Add account to list if it matches the owner's username
                accounts.append(node.account)
            # Recurse into left and right subtrees
            self._get_user_accounts_recursive(node.left, username, accounts)
            self._get_user_accounts_recursive(node.right, username, accounts)