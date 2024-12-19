# Hash Table for User Authentication
class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def _hash(self, key):
        return hash(key) % self.size
    
    def insert(self, key, value):
        hash_key = self._hash(key)
        for i, (k, v) in enumerate(self.table[hash_key]):
            if k == key:
                self.table[hash_key][i] = (key, value)
                return
        self.table[hash_key].append((key, value))
    
    def get(self, key):
        hash_key = self._hash(key)
        for k, v in self.table[hash_key]:
            if k == key:
                return v
        return None
    
    def exists(self, key):
        return self.get(key) is not None