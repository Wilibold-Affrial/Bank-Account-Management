# Bank Account Management

A secure and efficient banking system implementation using various data structures and algorithms. This project demonstrates the practical application of fundamental computer science concepts in a real-world scenario.

## Features

- User Authentication
- Account Management
- Transaction Processing
- Fund Transfers
- Transaction History Tracking
- Suspicious Activity Detection

## Data Structures Used

### 1. Binary Search Tree (BST)
- Implements efficient account storage and retrieval
- Maintains account hierarchy
- Supports quick lookups by account number
- Located in `bst.py`

### 2. Hash Table
- Manages user authentication
- Provides O(1) lookup time for user credentials
- Implements secure password storage using SHA-256
- Located in `hashtable.py`

### 3. Priority Queue
- Handles transaction processing
- Prioritizes transactions based on account type and amount
- Ensures VIP accounts get preferential treatment
- Located in `priority_queue.py`

### 4. Graph
- Tracks relationships between accounts
- Monitors transaction patterns
- Detects suspicious circular transactions
- Located in `graph.py`

## Account Types

1. Regular Account
   - Standard priority level (3)
   - Basic banking features
   - Upgradeable to VIP

2. VIP Account
   - High priority level (1)
   - Preferential transaction processing
   - Enhanced features

## Transaction Priority Levels

1. Priority 1 (Highest)
   - VIP account transactions
   - High-value transactions (>$10,000)

2. Priority 2 (Medium)
   - Medium-value transactions ($1,000-$10,000)

3. Priority 3 (Regular)
   - Standard transactions (<$1,000)

## Security Features

- Password hashing using SHA-256
- Transaction monitoring for suspicious patterns
- Circular transaction detection
- Thread-safe transaction processing
- Secure balance updates

## Usage

### Requirements
- Python 3.x
- Streamlit
- Threading support

### Installation
1. Clone the repository
2. Install required dependencies:
```bash
pip install streamlit
```

### Running the Application
```bash
streamlit run main.py
```

### User Operations
1. Account Creation
   - Register with username and password
   - Create multiple bank accounts
   - Choose account type (Regular/VIP)

2. Banking Operations
   - Deposit funds
   - Withdraw funds
   - Transfer between accounts
   - View transaction history
   - Monitor pending transactions

3. Account Management
   - View account details
   - Upgrade to VIP status
   - Track transaction history

## Implementation Details

### Transaction Processing
- Asynchronous processing using threading
- Priority-based execution
- Transaction status tracking
- Automatic balance updates

### Security Measures
1. Authentication
   - Secure password storage
   - Session management
   - Login/logout functionality

2. Transaction Security
   - Balance verification before transactions
   - Thread-safe operations
   - Transaction logging

### Monitoring
- Transaction pattern analysis
- Circular transaction detection
- Transaction volume tracking
- Account connection mapping

## File Structure

```
banking_system/
├── data_structures/
│   ├── bst.py           # Binary Search Tree implementation
│   ├── hashtable.py     # Hash Table for user authentication
│   ├── priority_queue.py # Priority Queue for transactions
│   └── graph.py         # Transaction relationship tracking
└── main.py              # Main application file
```


## Error Handling

The system includes comprehensive error handling for:
- Insufficient funds
- Invalid transactions
- Authentication failures
- System errors
- Concurrent access issues

## Future Improvements

1. Database integration
2. Enhanced security features
3. API implementation
4. Mobile application
5. Additional account types
6. Advanced analytics
7. Automated fraud detection