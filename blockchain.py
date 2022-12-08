from block import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 4
        self.generate_genesis_block()

    def generate_genesis_block(self):
        self.chain.append(Block("0", ['Genesis Block']))
           
    def add_data(self, data):
        last_block = self.last_block
        new_block = Block(data=data,
                          previous_block_hash=last_block.hash)
        proof = self.proof_of_work(new_block)
        new_block.hash = proof
        self.chain.append(new_block)

    def display_chain(self):
        for i in range(len(self.chain)):
            print(f"Variables {i + 1}: {self.chain[i].block_data}")
            print(f"Previous hash {i + 1}: {self.chain[i].previous_block_hash}")
            print(f"Data {i + 1}: {self.chain[i].transaction_list}")
            print(f"Hash {i + 1}: {self.chain[i].hash}\n")
            
    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.get_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.get_hash()
        return computed_hash
    
    @property
    def last_block(self):
        return self.chain[-1]
