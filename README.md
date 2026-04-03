# Blockchain

## Sources

- https://github.com/shafu0x/blockchain-from-scratch?tab=readme-ov-file
- https://github.com/shafu0x/block-explorer/blob/main/README.md

## Instructions

1) Enter WSL
2) Clone the repo: ``git clone https://github.com/SylweKra/Blockchain``
3) Enter the directory: ``cd Blockchain``
4) Create the virtual environment: ``python -m venv blockchain_venv``
5) Activate the virtual environment: ``source blockchain_venv/bin/activate``
6) Install the dependencies: ``pip install -r requirements.txt``
7) Start the program: ``python Main.py``

## Feature overview

1. Create Users (Wallets)
    1. Enter number of users:
        - Expected value: ``positive integer``
	2. Enter name for each user:
		- Expected value: ``string``
2. Create a Manual Transaction
    1. Enter sender name:
        - Expected value: ``string``
    2. Enter receiver name:
        - Expected value: ``string``
    3. Enter amount:
        - Expected value: ``positive integer``
3. Generate Random Transactions in Batch
    1. Enter number of transactions:
    	- Expected value: ``positive integer``
4. Generate and Display the Merkle Tree
	1. Generates the Merkle tree of all the transactions (no input required)
5. Verify a Transaction (Merkle Proof)
    1. Enter id of transaction to validate:
    	- Expected value: ``positive integer``
6. Tamper with a Transaction (Attack!)
    1. Enter id of transaction to tamper:
    	- Expected value: ``positive integer``
    2. Enter new amount for selected transaction:
        - Expected value: ``positive integer``