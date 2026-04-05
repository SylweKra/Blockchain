import hashlib
import json
import time
from typing import List, Optional
from Transaction import Transaction
from MerkleTree import MerkleTree


class Block:
    
    def __init__(
        self,
        index: int,
        transactions: List[Transaction],
        previous_hash: str,
        timestamp: Optional[float] = None,
        nonce: int = 0  #Nonce starting with 0
    ):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp if timestamp else time.time()
        self.nonce = nonce  
        self.merkle_tree = MerkleTree(transactions)
        self.hash = self.SHA256_block_hash()
    
    def SHA256_block_hash(self) -> str:     
        block_data = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,  
            "merkle_root": self.merkle_tree.get_root()
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    

    
    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "nonce": self.nonce,
            "merkle_root": self.merkle_tree.get_root(),
            "transactions_count": len(self.transactions)
        }


class Blockchain:
    def __init__(self):
        self.chain = []
        self.add_block([])  # genesis block
    
    def add_block(self, transactions: List[Transaction]) -> Block:
        if not self.chain:  #if the chain is empty it is a genesis block with no transactions
            index = 0
            previous_hash = "0" * 64
        else:  #Regular block
            index = len(self.chain)
            previous_hash = self.chain[-1].hash
        
        block = Block(index, transactions, previous_hash)
         ####ADD MINING HERE
        self.chain.append(block)
        print(f"Block {index} added ({'Genesis' if index == 0 else 'Regular'})")
        return block
    
    def is_chain_valid(self, difficulty: int = 2) -> bool: #Basic chain verification
        for i, block in enumerate(self.chain):
            if i > 0:
                if block.previous_hash != self.chain[i-1].hash:
                    print(f"Block {i} link broken!")
                    return False
            
            if block.hash != block.calculate_hash():
                print(f"Block {i} hash invalid!")
                return False
        
        print("Blockchain valid!")
        return True
    
    def display_chain(self) -> None:  #Printing for user viewing/ debugging
        print("\n" + "="*50)
        print("BLOCKCHAIN")
        print("="*50)
        for block in self.chain:
            print(f"\nBlock #{block.index}")
            print(f"  Timestamp: {block.timestamp}")
            print(f"  Previous Hash: {block.previous_hash[:20]}...")
            print(f"  Hash: {block.hash[:20]}...")
            print(f"  Nonce: {block.nonce}")
            
            merkle_root = block.merkle_tree.get_root()
            if merkle_root:
                print(f"Merkle Root: {merkle_root[:20]}...")
            else:
                print(f"Merkle Root: None (empty block)")
                
            print(f"Transactions: {len(block.transactions)}")