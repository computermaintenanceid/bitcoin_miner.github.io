import hashlib
import time
import json
import requests

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(data='Genesis Block')  # Initialize with a genesis block

    def create_block(self, data):
        block = Block(index=len(self.chain) + 1,
                      previous_hash=self.chain[-1].hash if self.chain else '0',
                      timestamp=time.time(),
                      data=data)
        self.chain.append(block)
        return block

    def mine_block(self, block, difficulty):
        while not block.hash.startswith('0' * difficulty):
            block.nonce += 1
            block.hash = block.calculate_hash()
        print(f"Block mined! Nonce: {block.nonce}, Hash: {block.hash}")
        return block

    def get_unconfirmed_transactions(self):
        # Fetch unconfirmed transactions from the Bitcoin network
        response = requests.get('https://blockchain.info/unconfirmed-transactions?format=json')
        return response.json()['txs']

if __name__ == "__main__":
    difficulty = 4  # Difficulty level
    blockchain = Blockchain()

    # Fetch unconfirmed transactions
    unconfirmed_transactions = blockchain.get_unconfirmed_transactions()
    transactions = [tx['hash'] for tx in unconfirmed_transactions]  # Get transaction hashes

    new_block = blockchain.create_block(transactions)

    # Mining process
    mined_block = blockchain.mine_block(new_block, difficulty)