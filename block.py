import hashlib
import json

class Block:
    def __init__(self, previous_block_hash, data, nonce = 0):
        self.previous_block_hash = previous_block_hash
        self.transaction_list = data
        self.block_data = f"{' - '.join(data)}"
        self.nonce = 0
        self.hash = '0'
        
    def get_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()