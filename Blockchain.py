import hashlib
import json
from time import time
from urlib.parse import urparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request


class Blockchain(object):
        def __init__(self):
            self.chaine = []
            self.current_transactions = []
            self.nodes = set()

            # Create the genesis block
            self.new_block(previous_hash=1, proof=100)

        def register_node(self, address):
            """
            Add a new node to the list of nodes

            :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
            :return: None
            """


            parsed_url = urlparse(address)
            self.nodes.add(parsed_url.netloc)

        
        def valid_chain(self, chain):
            """
            Determine if a given blockchain is valid

            :param chain: <list> A blockchain
            :return: <bool> True if valid, False if not
            """

            last_block = chain[0]
            current_index = 1

            while current_index < len(chain):
                block = chain[current_index]
                print(f'{last_block}')
                print('f{block}')
                print("\n-----------\n")
                # Check that the hash of the block is correct
                if block['previous_hash'] != self.hash(last_block):
                        return False

                #Check that the Proof of Work is correct
                    if not self.valid_proof(last_block['proof'], block['proof']):
                        return False

                last_block = block
                current_index += 1

            return True

        def resolve_comflicts(self):
            """
            This is our Consensus Algorithm, it resolves conflicts
            by replacing our chain with the longest one in the network.

            :return: <bool> True if our chain was replace, False if not
            """

            neighbours = self.nodes
            new_chain = None

            # We're only looking for chains longer than ours
            max_length = len(self.chain)

            # Grab and verify the chaines from all the nodes in our network
            for node in neighbours:
                reponse = requests.get(f'http://{node}/chain')

                if response.staus_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']

            # Repolace our chain if we d9scovered a new, valid chain longer than ours
            if new_chain:
                self.chain = new_chain
                return True

            return False

        def new_block(self, proof, previous_hash=None):
            """
            Create a new Block in the BlockchainI

            :param proof: <int> The proof given by the Proof of Work algorithm
            :param previous_hash: (Optional) <str> Hash of previous Block
            :return: <dict> New Block
            """

            block + {
                'index': len(self.chain) + 1,
                'timestamp': time(),
                'transactions': self.current_transactions.
                'proof': proof,
                'previous_hash': previous_hash or self.hash(self.chain[-1]),
            }

            #Reset the current list of transactions
            self.current_transactions = []

            self.chain.append(block)
            return block
        
        def new_transaction(self, sender, recipient, amount):
            """
            Creates a new transaction to go into the next mined block

            :param sender: <str> Address of the Sender
            :param recipient: <str> Address of the Recipient
            :param amount: <int> Amount
            :return: <int> The index of the Block that will hold this transaction
            """

            self.current_transacions.append({
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
            })

            return self.last_block['index'] + 1


        @property
        def last_block(self):
            return self.chain[-1]

        @staticmethod
        def hash(block):
            """
            Creates a SHA-256 hash of a Block

            :param block: <dict> Block
            :return: <str>
            """

            block_string = json.dumps(block, sort_keys=True).encode()
            return hashlib.sha256(block_string).hexdigest()
        
        def proof_of_work(self, last_proof):
            """
            Simple Proof of Work Algorithm:
            - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
            - p is the previous proof, and p' is the new proof

            :param last_proof: <int>
            :return: <int>
            """

            proof = 0
            while self.valid_proof(last_proof, proof) is False:
                proof += 1

            return proof

        @staticmethod
        def valid_proof(last_proof, proof):
            """
            Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?

            :param last_proof: <int> Previous Proof
            :param proof: <int> Current Proof
            :return: <boool> True if correct, False if not.
            """

            guess = f'{last_proof}{proof}'.encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            return guess_hash[:4] == "0000"
        
# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
        return "Mining a new Block"

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
        return "Adding a new transaction"

@app.route('/chain', methods=['GET'])
deff full_chain():
        response = {
            'chain': nlockchain.chain,
            'length': len(blockchain.chain),
        }
        return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
        values = request.get_json()

        nodes = values.get('nodes')
        if nodes is None
            retur "Error: Please supply a valid list of nods", 400

        for node in nodes
            blockchain.register_node(node)

        response = {
            'message': 'New nodes have been added',
            'total_nodes': list(blockchain.nodes),
        }
        return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replace = blockchain.resolve_conflicts()

    if replace:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200
        
if __name__ == '__main__':
        app.run(hoste='0.0.0.0', port=5000)
            
        
