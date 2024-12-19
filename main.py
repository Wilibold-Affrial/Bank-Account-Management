import streamlit as st
import hashlib
import time

from hashtable import HashTable
from bst import BankAccount, BankAccountBST
from priority_queue import TransactionProcessor
from graph import TransactionGraph
from datetime import datetime

# Initialize session state
if 'user_db' not in st.session_state:
    st.session_state.user_db = HashTable()

if 'account_bst' not in st.session_state:
    st.session_state.account_bst = BankAccountBST()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'transaction_processor' not in st.session_state:
    st.session_state.transaction_processor = TransactionProcessor()
    st.session_state.transaction_processor.is_processing = False

if 'transaction_graph' not in st.session_state:
    st.session_state.transaction_graph = TransactionGraph()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    stored_password = st.session_state.user_db.get(username)
    if stored_password and stored_password == hash_password(password):
        st.session_state.logged_in = True
        st.session_state.current_user = username
        return True
    return False

def register_user(username, password):
    if st.session_state.user_db.exists(username):
        return False
    hashed_password = hash_password(password)
    st.session_state.user_db.insert(username, hashed_password)
    return True

def create_login_page():
    st.title("Banking System Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if login_user(username, password):
                st.success("Successfully logged in!")
            else:
                st.error("Invalid username or password")

def create_signup_page():
    st.title("Create Bank Account")
    
    with st.form("signup_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up")
        
        if submit:
            if password != confirm_password:
                st.error("Passwords do not match!")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long!")
            elif register_user(username, password):
                st.success("Account created successfully! Please login.")
                time.sleep(1)
            else:
                st.error("Username already exists!")

def handle_transfer(from_account, user_accounts):
    with st.form(f"transfer_form_{from_account.account_number}"):
        st.subheader("Transfer")
        to_account_number = st.selectbox(
            "To Account",
            [acc.account_number for acc in user_accounts if acc.account_number != from_account.account_number]
        )
        transfer_amount = st.number_input("Amount", min_value=0.0)
        transfer_desc = st.text_input("Description")
        
        if st.form_submit_button("Transfer"):
            if transfer_amount <= from_account.balance:
                to_account = st.session_state.account_bst.find_account(to_account_number)
                if to_account:
                    # Add to transaction graph
                    st.session_state.transaction_graph.add_transaction(
                        from_account.account_number,
                        to_account_number,
                        transfer_amount,
                        "transfer"
                    )
                    
                    # Process withdrawal from source account
                    withdraw_transaction = {
                        'type': 'withdraw',
                        'amount': transfer_amount,
                        'description': f"Transfer to {to_account_number}: {transfer_desc}",
                        'account': from_account,
                        'account_type': from_account.account_type
                    }
                    
                    # Process deposit to destination account
                    deposit_transaction = {
                        'type': 'deposit',
                        'amount': transfer_amount,
                        'description': f"Transfer from {from_account.account_number}: {transfer_desc}",
                        'account': to_account,
                        'account_type': to_account.account_type
                    }
                    
                    st.session_state.transaction_processor.add_transaction(withdraw_transaction)
                    st.session_state.transaction_processor.add_transaction(deposit_transaction)
                    
                    st.success(f"Transfer of ${transfer_amount:.2f} initiated")
                    
                    # Check for suspicious patterns
                    if st.session_state.transaction_graph.detect_circular_transactions(from_account.account_number):
                        st.warning("Circular transaction pattern detected!")
            else:
                st.error("Insufficient funds!")

def handle_banking_operations(account, transaction_processor):
    col1, col2 = st.columns(2)
    
    with col1:
        with st.form(f"deposit_form_{account.account_number}"):
            deposit_amount = st.number_input("Amount", min_value=0.0, key=f"deposit_{account.account_number}")
            deposit_desc = st.text_input("Description", key=f"deposit_desc_{account.account_number}")
            if st.form_submit_button("Deposit"):
                if deposit_amount > 0:
                    transaction = {
                        'type': 'deposit',
                        'amount': deposit_amount,
                        'description': deposit_desc,
                        'account': account,
                        'account_type': account.account_type,
                        'timestamp': datetime.now()
                    }

                    transaction_processor.add_transaction(transaction)
                    st.success(f"Deposit of ${deposit_amount:.2f} queued for processing")
    
    with col2:
        with st.form(f"withdraw_form_{account.account_number}"):
            withdraw_amount = st.number_input("Amount", min_value=0.0, key=f"withdraw_{account.account_number}")
            withdraw_desc = st.text_input("Description", key=f"withdraw_desc_{account.account_number}")
            if st.form_submit_button("Withdraw"):
                if withdraw_amount <= account.balance:
                    transaction = {
                        'type': 'withdraw',
                        'amount': withdraw_amount,
                        'description': withdraw_desc,
                        'account': account,
                        'account_type': account.account_type,
                        'timestamp': datetime.now()
                    }

                    transaction_processor.add_transaction(transaction)
                    st.success(f"Withdrawal of ${withdraw_amount:.2f} queued for processing")
                else:
                    st.error("Insufficient funds!")

def create_dashboard():
    st.title(f"Welcome {st.session_state.current_user}!")
    
    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Go to", ["Accounts", "Transaction History", "Pending Transactions"])
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.transaction_processor = TransactionProcessor()
    
    if page == "Accounts":
        st.header("Your Bank Accounts")

        user_accounts = st.session_state.account_bst.get_user_accounts(
            st.session_state.current_user
        )
        
        # Create new account section
        with st.expander("Open New Account"):
            with st.form("create_account"):
                account_number = st.text_input("Account Number")
                account_type = st.selectbox("Account Type", ["Regular", "VIP"])
                initial_deposit = st.number_input("Initial Deposit", min_value=0.0)
                submit = st.form_submit_button("Create Account")
                
                if submit:
                    if not st.session_state.account_bst.find_account(account_number):
                        new_account = BankAccount(
                            account_number=account_number,
                            owner_username=st.session_state.current_user,
                            account_type=account_type,
                            balance=0  # Initialize with 0 balance
                        )
                        st.session_state.account_bst.insert(new_account)
                        if initial_deposit > 0:
                            transaction = {
                                'type': 'deposit',
                                'amount': initial_deposit,
                                'description': "Initial deposit",
                                'account': new_account,
                                'account_type': account_type,
                                'timestamp': datetime.now()
                            }
                            st.session_state.transaction_processor.is_processing = False
                            st.session_state.transaction_processor.add_transaction(transaction)
                        st.success("Account created successfully!")
                    else:
                        st.error("Account number already exists!")
        
        if user_accounts:
            for from_account in user_accounts:
                with st.expander(f"Account: {from_account.account_number}"):
                    # Display account details
                    st.write(f"Balance: ${from_account.balance:.2f}")
                    st.write(f"Type: {from_account.account_type}")
                    st.write(f"Created: {from_account.creation_date.strftime('%Y-%m-%d')}")

                    # Add transfer functionality
                    st.subheader("Transfer Funds")
                    to_account_number = st.selectbox(
                        "Select destination account",
                        [
                            acc.account_number for acc in user_accounts
                            if acc.account_number != from_account.account_number
                        ]
                    )
                    transfer_amount = st.number_input(
                        "Transfer Amount", min_value=0.0, key=f"transfer_{from_account.account_number}"
                    )

                    if st.button(f"Transfer", key=f"transfer_btn_{from_account.account_number}"):
                        to_account = st.session_state.account_bst.find_account(to_account_number)
                        if to_account:
                            success = st.session_state.transaction_graph.transfer_between_accounts(
                                from_account, to_account, transfer_amount, st.session_state.transaction_processor
                            )
                            if success:
                                st.success(f"Successfully transferred ${transfer_amount:.2f} to {to_account_number}.")
                            else:
                                st.error("Insufficient funds for transfer.")
                        else:
                            st.error("Destination account not found.")
        else:
            st.info("No accounts found. Create one to get started!")
            
        # Display user's accounts
        user_accounts = st.session_state.account_bst.get_user_accounts(
            st.session_state.current_user
        )
        
        if user_accounts:
            for account in user_accounts:
                with st.container():
                    st.write("---")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.subheader(f"Account: {account.account_number}")
                        st.write(f"Balance: ${account.balance:.2f}")
                    with col2:
                        st.write(f"Type: {account.account_type}")
                        st.write(f"Created: {account.creation_date.strftime('%Y-%m-%d')}")
                    with col3:
                        if account.account_type == "Regular":
                            if st.button(f"Upgrade to VIP", key=f"upgrade_{account.account_number}"):
                                account.account_type = "VIP"
                                st.success("Account upgraded to VIP!")
                    
                    handle_banking_operations(account, st.session_state.transaction_processor)
        else:
            st.info("You don't have any accounts yet. Create one to get started!")
    
    elif page == "Transaction History":
        st.header("Transaction History")
        user_accounts = st.session_state.account_bst.get_user_accounts(
            st.session_state.current_user
        )
        
        if user_accounts:
            for account in user_accounts:
                with st.expander(f"Account {account.account_number} ({account.account_type})"):
                    if account.transaction_history:
                        for transaction in reversed(account.transaction_history):
                            priority_label = "🔴 High" if transaction.get('priority', 3) == 1 else "🟡 Medium" if transaction.get('priority', 3) == 2 else "🟢 Low"
                            st.write(
                                f"**{transaction['type'].title()}** - "
                                f"${transaction['amount']:.2f} - "
                                f"{transaction['description']} - "
                                f"{transaction['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} - "
                                f"Priority: {priority_label}"
                            )
                    else:
                        st.info("No transactions yet.")
        else:
            st.info("No accounts found.")
    
    elif page == "Pending Transactions":
        st.header("Pending Transactions")
        st.write("Transactions are processed manually by pressing the 'Process' button below.")

        #Display each pending transaction
        for pt in st.session_state.transaction_processor.pending_transactions:
            transaction = pt.transaction
            priority_label = "🔴 High" if pt.priority == 1 else "🟡 Medium" if pt.priority == 2 else "🟢 Low"
            
            col1, col2 = st.columns([3,1])
            with col1:
                st.write(
                    f"**{transaction['type'].title()}** - "
                    f"${transaction['amount']:.2f} - "
                    f"Account: {transaction['account'].account_number} - "
                    f"Description: {transaction['description']} - "
                    f"Priority: {priority_label}"
                )
            with col2:
                if st.button("Process", key=f"process_{pt.id}"):
                    st.session_state.transaction_processor.process_pending_transaction(pt.id)
                    st.success(f"Transaction for ${transaction['amount']:.2f} processed successfully!")
                    st.rerun()  # Refresh the page to update the list

def main():
    if not st.session_state.logged_in:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            create_login_page()
        with tab2:
            create_signup_page()
    else:
        create_dashboard()

if __name__ == "__main__":
    main()