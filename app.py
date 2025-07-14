from flask import Flask, jsonify, request, render_template
import requests
import json
from time import time
import hashlib
import argparse

app = Flask(__name__)
peers = {}
# ============================== Blockchain Classes ==============================

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_dict(self):
        return {"sender": self.sender, "recipient": self.recipient, "amount": self.amount}

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True, default=str).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'hash': getattr(self, 'hash', None),
            'transactions': [tx.to_dict() for tx in self.transactions]
        }

class Blockchain:
    def __init__(self):
        self.chain = []
        self.unconfirmed_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0000') and block_hash == block.compute_hash())

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0000'):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        if not self.unconfirmed_transactions:
            return None
        last_block = self.last_block
        new_block = Block(
            index=last_block.index + 1,
            transactions=self.unconfirmed_transactions,
            timestamp=time(),
            previous_hash=last_block.hash
        )
        proof = self.proof_of_work(new_block)
        if self.add_block(new_block, proof):
            self.unconfirmed_transactions = []
            return new_block.index
        return None

blockchain = Blockchain()

# ============================== Flask API ==============================

@app.route('/')
def index():
    return render_template("index.html", peers=peers)

@app.route('/api/chain', methods=['GET'])
def get_chain():
    return jsonify([block.to_dict() for block in blockchain.chain])

@app.route('/api/send', methods=['POST'])
def send_transaction():
    data = request.get_json()
    try:
        sender = data['sender']
        recipient = data['recipient']
        amount = int(data['amount'])
        blockchain.add_new_transaction(Transaction(sender, recipient, amount))
        return jsonify({"success": True, "message": "Transaction added."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/api/mine', methods=['POST'])
def mine_block():
    try:
        result = blockchain.mine()
        if result is not None:
            return jsonify({"success": True, "message": f"Block #{result} mined!"})
        return jsonify({"success": False, "message": "No transactions to mine."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/register_peer', methods=['POST'])
def register_peer():
    name = request.form.get("name")
    url = request.form.get("url")
    if name and url:
        peers[name] = url
        return jsonify({"success": True, "message": f"Registered {name} at {url}."})
    return jsonify({"success": False, "message": "Missing name or URL."}), 400

@app.route('/api/sync_chains', methods=['GET'])
def sync_chains():
    results = {}
    for name, url in peers.items():
        try:
            res = requests.get(f"{url}/api/chain")
            if res.status_code == 200:
                chain = res.json()
                if len(chain) > len(blockchain.chain):
                    blockchain.chain = [
                        Block(
                            b['index'],
                            [Transaction(**tx) for tx in b['transactions']],
                            b['timestamp'],
                            b['previous_hash']
                        ) for b in chain
                    ]
                    for i in range(len(blockchain.chain)):
                        blockchain.chain[i].hash = blockchain.chain[i].compute_hash()
                results[name] = {"status": "success", "length": len(chain)}
            else:
                results[name] = {"status": "failed", "code": res.status_code}
        except Exception as e:
            results[name] = {"status": "error", "error": str(e)}
    return jsonify(results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port, debug=True)
