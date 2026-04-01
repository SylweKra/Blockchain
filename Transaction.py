import hashlib
import json
import base64
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from dataclasses import dataclass, field
from typing import Optional
import time


class Wallet:

    def __init__(self):

        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

    @classmethod
    def from_private_key(cls, private_key: str):
        "Create a wallet from a given private key."
        wallet = cls()
        wallet.private_key = SigningKey.from_string(
            bytes.fromhex(private_key), curve=SECP256k1
        )
        wallet.public_key = wallet.private_key.get_verifying_key()
        return wallet

    def get_address(self) -> str:
        "Generate a wallet address from the public key."
        public_key_bytes = self.public_key.to_string()
        sha256_hash = hashlib.sha256(public_key_bytes).digest()
        ripemd160_hash = hashlib.new("ripemd160", sha256_hash).digest()
        return base64.b64encode(ripemd160_hash).decode()

    def get_public_key_hex(self) -> str:
        "Get the public key in hexadecimal format."
        return self.public_key.to_string().hex()

    def get_private_key_hex(self) -> str:
        "Get the private key in hexadecimal format."
        return self.private_key.to_string().hex()

    def sign(self, message: bytes) -> str:
        """
        Sign a message with the private key.
        Return the signature encoded in base64.
        """
        signature = self.private_key.sign(message)
        return base64.b64encode(signature).decode("ascii")


@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: float
    timestamp: float = field(default_factory=time.time)
    signature: Optional[str] = None
    public_key: Optional[str] = None

    def to_dict(self) -> dict:
        "Convert the transaction to a dictionary."
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "signature": self.signature,
            "public_key": self.public_key,
            "hash": self.calculate_hash(),
        }

    def calculate_hash(self) -> str:
        "Calculate the hash of the transaction."
        tx_data = {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
        }
        tx_string = json.dumps(tx_data, sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()

    def sign_transaction(self, wallet: Wallet) -> "Transaction":
        "Sign the transaction with the sender's wallet."
        if wallet.get_address() != self.sender:
            raise ValueError("Wallet address does not match sender.")

        message = f"{self.sender}:{self.recipient}:{self.amount}:{self.timestamp}"
        self.signature = wallet.sign(message.encode())
        self.public_key = wallet.get_public_key_hex()

        return self

    def verify_transaction(self) -> bool:
        "Verify the transaction's signature. using the public key"
        if not self.signature or not self.public_key:
            return False
        VerifyingKey = VerifyingKey.from_string(
            bytes.fromhex(self.public_key), curve=SECP256k1
        )
        message = f"{self.sender}:{self.recipient}:{self.amount}:{self.timestamp}"
        try:
            return VerifyingKey.verify(
                base64.b64decode(self.signature), message.encode()
            )
        except Exception as e:
            print(f"Error occurred while verifying signature: {e}")
            return False

    def verify_signature(self) -> bool:
        "Verify the transaction's signature using the public key."
        if not self.signature or not self.public_key:
            return False
        verifying_key = VerifyingKey.from_string(
            bytes.fromhex(self.public_key), curve=SECP256k1
        )
        message = f"{self.sender}:{self.recipient}:{self.amount}:{self.timestamp}"
        try:
            return verifying_key.verify(
                base64.b64decode(self.signature), message.encode()
            )
        except Exception as e:
            print(f"Error occurred while verifying signature: {e}")
            return False

    def __str__(self) -> str:
        "Return a string representation of the transaction."
        return json.dumps(self.to_dict(), indent=4)
