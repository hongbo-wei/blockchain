# A simple blockchain program in Python would involve creating blocks with basic attributes
# like an index, a timestamp, a list of transactions, a proof (like a nonce in Bitcoin mining),
# and the hash of the previous block to ensure the chain's integrity.

import hashlib
import time

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.transactions}{self.timestamp}{self.previous_hash}{self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.mining_reward = 10

    def create_genesis_block(self):
        return Block(0, [], time.time(), "0")

    def get_last_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, mining_reward_address):
        block = Block(len(self.chain), self.pending_transactions, time.time(), self.get_last_block().hash)
        block.mine_block(self.difficulty)

        print(f"Block successfully mined! The miner is rewarded with {self.mining_reward} coins.")
        self.chain.append(block)

        self.pending_transactions = [
            {"from_address": None, "to_address": mining_reward_address, "amount": self.mining_reward}
        ]

    def create_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

# Demonstrate the Blockchain class with a simple example

# Create a new Blockchain
my_blockchain = Blockchain()

# Add a transaction
my_blockchain.create_transaction({"from_address": "address1", "to_address": "address2", "amount": 5})

# Mine pending transactions
my_blockchain.mine_pending_transactions("my_address")

# Check if the chain is valid
is_valid = my_blockchain.is_chain_valid()
print(f"Is blockchain valid? {is_valid}")

# Add another block
my_blockchain.create_transaction({"from_address": "address2", "to_address": "my_address", "amount": 3})
my_blockchain.mine_pending_transactions("my_address")

# Check if the chain is still valid
is_valid_after = my_blockchain.is_chain_valid()
print(f"Is blockchain valid after new block? {is_valid_after}")
