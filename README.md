P2P Blockchain Simulation
A professional, web-based simulation of a peer-to-peer blockchain network built using Python (Flask) and JavaScript. This simulation helps learners and developers explore how decentralized blockchains work—through mining, transaction creation, and node syncing.

Overview
Each blockchain node runs independently on a different port and maintains its own ledger. Nodes can be registered with each other to simulate a decentralized peer-to-peer (P2P) network. The system implements:

Block creation with proof-of-work

Longest chain consensus

Peer syncing

Transaction pooling and block mining

Visual interface for real-time interaction

Features
Send transactions between nodes

Mine new blocks using proof-of-work

Register peers to simulate decentralized networking

Synchronize chains to resolve differences

View the full blockchain in JSON format

Web dashboard with Bootstrap UI

Getting Started
Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
Running the Application
Run multiple blockchain nodes on different ports:

bash
Copy
Edit
python app.py --port 8000
python app.py --port 8001
python app.py --port 8002
Open each node in separate terminals.

Accessing the Web Interface
Visit the following URLs in your browser:

http://localhost:8000

http://localhost:8001

http://localhost:8002

Example Usage
On port 8000, register peers at http://localhost:8001 and http://localhost:8002

Send transactions between registered peers

Mine blocks to confirm transactions

Sync chains to ensure all nodes have the latest version

API Endpoints
Endpoint	Method	Description
/api/chain	GET	Returns the full blockchain
/api/send	POST	Adds a new transaction
/api/mine	POST	Mines a block with pending transactions
/api/register_peer	POST	Registers a new peer
/api/sync_chains	GET	Syncs the local chain with peer chains

User Interface
Built with HTML, Bootstrap, and JavaScript, the dashboard allows users to:

View the blockchain and individual blocks

Send transactions

Register and manage peer nodes

Mine blocks

Synchronize chains across peers

Screenshot
<img width="1720" height="1542" alt="Screenshot 2025-07-14 at 19 40 38" src="https://github.com/user-attachments/assets/3f49c9c4-6688-4c9b-a6e7-977a0ff95d64" />
<img width="1564" height="1794" alt="Screenshot 2025-07-14 at 19 40 49" src="https://github.com/user-attachments/assets/4d1c3c4d-7072-4981-a188-334db68f0bd0" />


