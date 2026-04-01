from typing import List, Optional
import hashlib
from Transaction import Transaction
import pdb


class MerkleTree:
    def __init__(self, transactions: List[Transaction]):
        self.transactions = transactions
        self.leaves: List[str] = []
        self.tree: List[str] = []
        self._build_tree()

    def _hash_transaction(self, tx: Transaction) -> str:
        "Calculate the hash of every single transaction,uses double hash as a real blockchain does"
        tx_hash = tx.calculate_hash()
        return hashlib.sha256(hashlib.sha256(tx_hash.encode()).digest()).hexdigest()

    def _hash_pair(self, left: str, right: str) -> str:
        "Calculate the hash of the two child nodes"
        combined = left + right
        return hashlib.sha256(combined.encode()).hexdigest()

    def _build_tree(self):
        "Builds the Merkle starting from the leafes to the root"

        if not self.transactions:
            self.leaves = []
            self.tree = []
            return
        # level 0 leaves
        current_level = []
        for tx in self.transactions:
            tx_hash = self._hash_transaction(tx)
            current_level.append(tx_hash)
            self.leaves.append(tx_hash)
        self.tree.append(current_level)

        # process nodes in couple
        while len(current_level) > 1:
            next_level = []

            for i in range(0, len(current_level), 2):
                left = current_level[i]
                # if there is a even node, use it if not double the last
                if i + 1 < len(current_level):
                    right = current_level[i + 1]
                else:
                    right = left
                parent_hash = self._hash_pair(left, right)
                next_level.append(parent_hash)

            self.tree.append(next_level)
            current_level = next_level

    def get_root(self) -> Optional[str]:
        "return hash of root merkle tree"

        if not self.tree:
            return None
        return self.tree[-1][0] if self.tree[-1] else None

    def get_proof(self, transaction_index: int) -> List[str]:
        "generete the merkle proof for a specific transaction."
        "the proof is a list of has necessary to verify the transaction is included in the root"
        ""
        if not self.transactions or transaction_index >= len(self.transactions):
            return []

        proof = []
        current_index = transaction_index

        # for every level to root
        for level in range(len(self.tree) - 1):
            current_level = self.tree[level]

            if current_index % 2 == 0:  # is a left
                if current_index + 1 < len(current_level):
                    # has a brother
                    sibling = current_level[current_index + 1]
                    proof.append(("right", sibling))  # brother goes to right
                else:
                    # solo node,we need to duplicate it
                    proof.append(("right", current_level[current_index]))
            else:  # is right
                sibling = current_level[current_index - 1]  # has a brotther on left
                proof.append(("left", sibling))

            current_index = current_index // 2  # update index to next level

        return proof

    def verify_proof(
        self, transaction_hash: str, proof: List[str], root_hash: str
    ) -> bool:
        "Verify Merkle Proof"
        "transaction_hash= Hash of the transaction to verify"
        "proof = List of hash generate from get_proof()"
        "root_hash= hash root of the Merkle tree"
        current_hash = transaction_hash

        for direction, sibling_hash in proof:
            if direction == "left":
                # the brother is at left, so the current_hash is right
                combined = sibling_hash + current_hash
            else:  # direction == right
                # the brother is at right, so current_hash is at left
                combined = current_hash + sibling_hash

            current_hash = hashlib.sha256(combined.encode()).hexdigest()

        return current_hash == root_hash

    def get_tree_structure(self) -> dict:
        """
        Return the full tree structure for visualization.
        """
        return {
            "levels": len(self.tree),
            "leaves_count": len(self.leaves),
            "root": self.get_root(),
            "tree": self.tree,
        }

    def __str__(self) -> str:
        """
        Text representation of the Merkle Tree.
        """
        if not self.tree:
            return "Empty Merkle Tree"

        result = f"Merkle Tree (levels: {len(self.tree)}, leaves: {len(self.leaves)})\n"
        result += "=" * 50 + "\n"

        for level_idx, level in enumerate(self.tree):
            result += f"\nLevel {level_idx} ({len(level)} nodes):\n"
            for node_idx, node_hash in enumerate(level[:5]):  # Show max 5 per level
                result += f"  [{node_idx}] {node_hash[:16]}...\n"
            if len(level) > 5:
                result += f"  ... and {len(level) - 5} more nodes\n"

        result += f"\nRoot Hash: {self.get_root()}\n"
        return result
