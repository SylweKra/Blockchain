# TASCoin - A mini blockchain demo

## Members of Group 4
- DI BIASE Amedeo, SID: 25550225
- KRASINSKI Sylwester, SID: 25550276
- ZELENYUK Tamara Yevhenivna, SID: 25408038

## Sources

- https://github.com/shafu0x/blockchain-from-scratch?tab=readme-ov-file
- https://github.com/shafu0x/block-explorer/blob/main/README.md

## HW/OS requirements
- CPU: 1 GHz 64-bit or faster
- RAM: 512 MB (2 GB+ recommended)
- Disk Space: 500 MB for installation and libraries
- OS: Windows 10+, any modern Linux

## Required libraries and dependencies
- Python 3
- `ecdsa` (installed with `pip install -r requirements.txt`)

## How to run

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
7. Mine and Create New Block
    1. The block header is hashed repeatedly with an incrementing nonce until the hash starts with ``000000``.
    2. Pending transactions are then committed to the chain with the valid nonce.
8. Display Blockchain
    1. Shows the mined blocks, hashes, nonces, and Merkle roots.
9. Run Block Tamper Test
    1. Mutates a block from the currently built blockchain and re-runs chain validation.
10. Exit

## Execution guide
1. First we have to create two or more users using function (1);
2. Then we can create some transactions (manually or automatically), using functions (2) or (3), respectively;
3. After that we can either: generate the Merkle Tree (4), validate a previous transaction (5), try to tamper with a transaction (6), mine a new block (7), or run the block tamper test (9).

### Expected output
- The program starts with a TASCoin welcome message and a numbered menu.
- Creating users prints generated wallet addresses and initial balances.
- Creating transactions prints transaction details and updates the pending list.
- Mining a block prints the block index, nonce, hash, and Merkle root.
- Displaying the blockchain prints the chain contents so you can confirm the blocks were added correctly.
- Tamper tests print a validation result showing whether the chain is still valid after modification.
