import hashlib
import threading

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hashlib.sha256()
        sha.update(
            str(self.index).encode() +
            str(self.timestamp).encode() +
            str(self.data).encode() +
            str(self.previous_hash).encode()
        )
        return sha.hexdigest()
    
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        data = "Genesis Block"
        previous_hash = "0"  # Replace with meaningful initial hash
        self.add_block(data, previous_hash)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data, previous_hash):
        new_block = Block(len(self.chain), time.time(), data, previous_hash)
        if self.is_chain_valid(self.chain):
            self.chain.append(new_block)

    def is_chain_valid(self, chain):
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]

            # Ensure block hashes are correct
            if current_block.hash != current_block.hash_block():
                return False

            # Ensure hashes link previous blocks
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

def hash(data):
    sha = hashlib.sha256()
    sha.update(data.encode())
    return sha.hexdigest()

def mine_block(block):
    difficulty = "0"*4  # Adjust based on desired difficulty
    nonce = 0

    while True:
        computed_hash = hash(str(block.index) + str(block.timestamp) + str(block.data) + str(block.previous_hash) + str(nonce))
        if computed_hash.startswith(difficulty):
            break
        nonce += 1

    return computed_hash, nonce

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

import socket
import time

# Peer-to-peer network settings
HOST = '127.0.0.1'  # Replace with your local IP address if needed
PORT = 5000
NODE_ID = 'your_node_id'  # Replace with a unique identifier for your node

# Mining difficulty
TARGET_DIFFICULTY = "0" * 4  # Adjust based on desired difficulty

# Blockchain and transactions
blockchain = Blockchain()
current_transactions = []

# Peer nodes
peers = set()

def connect_to_peers():
    # Implement code to connect to other nodes in the network
    # ...
    pass




def connect_to_peers():
    # Implement code to connect to other nodes in the network
    # ...
    pass


def announce_new_block(block):
    # Implement code to announce the new block to connected peers
    # ...
    pass


def handle_incoming_connection(client_socket):
    try:
        while True:
            data = client_socket.recv(1024).decode()
            # Handle received data (e.g., new blocks, transactions)
            # ...
    except ConnectionError:
        # Handle connection errors gracefully
        print("Connection error:")
        # Remove disconnected peer from peers set
        peers.discard(client_socket.getpeername())# ...
    finally:
        client_socket.close()


def broadcast(message):
    # Send message to all connected peers
    for peer in peers:
        try:
           peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           peer_socket.connect(peer)
           peer_socket.sendall(message.encode())  # Encode message for sending
           peer_socket.close()

        except ConnectionError as e:
            print(f"Failed to send message to {peer}: {e}")
            # Remove unreachable peer from peers set
            peers.discard(peer)


def proof_of_work(block):
    nonce = 0
    computed_hash = None
    while not computed_hash.startswith(TARGET_DIFFICULTY):
        nonce += 1
        computed_hash = mine_block(block, nonce)
    return computed_hash, nonce


def handle_new_transaction(transaction):
    # Validate and add transaction to current pool
    # ...
    current_transactions.append(transaction)


def create_new_block():
    previous_block = blockchain.get_latest_block()
    previous_hash = previous_block.hash
    index = previous_block.index + 1
    timestamp = time.time()

    # Add current transactions to data
    block_data = current_transactions
    current_transactions = []  # Reset pool for next block

    difficulty, nonce = proof_of_work(Block(index, timestamp, block_data, previous_hash))

    new_block = Block(index, timestamp, block_data, previous_hash, difficulty, nonce)

    # Validate and add to blockchain
    if blockchain.is_chain_valid(blockchain.chain + [new_block]):
        blockchain.add_block(new_block)
        announce_new_block(new_block)
        return new_block
    else:
        print("New block invalid! Discarding...")
        return None


def run():
    # Create or load a blockchain from storage (if applicable)
    # ...

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Node {NODE_ID} listening on {HOST}:{PORT}")

    connect_to_peers()  # Connect to other nodes

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        thread = threading.Thread(target=handle_incoming_connection, args=(conn,))
        thread.start()

        # Handle user input (e.g., creating transactions)
        # ...

        # Mine a new block periodically
        new_block = create_new_block()
        if new_block:
            print(f"Mined new block {new_block.index}")

if __name__ == "__main__":
    run()

