# Define a HashTable class for user authentication
class HashTable:
    # Constructor to initialize the hash table with a given size (default is 100)
    def __init__(self, size=100):
        self.size = size  # Set the size of the hash table
        # Create a list of empty lists to serve as buckets for storing key-value pairs
        self.table = [[] for _ in range(size)]
    
    # Private method to compute the hash value of a given key
    def _hash(self, key):
        # Use Python's built-in hash function and take modulo to fit within table size
        return hash(key) % self.size
    
    # Method to insert or update a key-value pair in the hash table
    def insert(self, key, value):
        # Calculate the hash key (index) for the given key
        hash_key = self._hash(key)
        # Iterate through the bucket at the computed hash index
        for i, (k, v) in enumerate(self.table[hash_key]):
            # If the key already exists, update its value and return
            if k == key:
                self.table[hash_key][i] = (key, value)
                return
        # If the key does not exist, append the new key-value pair to the bucket
        self.table[hash_key].append((key, value))
    
    # Method to retrieve the value associated with a given key
    def get(self, key):
        # Calculate the hash key (index) for the given key
        hash_key = self._hash(key)
        # Iterate through the bucket at the computed hash index
        for k, v in self.table[hash_key]:
            # If the key is found, return its corresponding value
            if k == key:
                return v
        # Return None if the key is not found
        return None
    
    # Method to check if a key exists in the hash table
    def exists(self, key):
        # Check if the value retrieved for the key is not None
        return self.get(key) is not None
