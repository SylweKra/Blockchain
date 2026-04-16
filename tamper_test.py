import json

from Blockchain import Blockchain


def print_block_summary(blockchain: Blockchain) -> None:
    print("\nAvailable mined blocks:")
    for block in blockchain.chain:
        print(
            f"  Block {block.index} | txs: {len(block.transactions)} | "
            f"hash: {block.hash[:16]}..."
        )


def tamper_live_blockchain(blockchain: Blockchain) -> bool:
    if len(blockchain.chain) < 2:
        print("❌ You need at least one mined block before running the tamper test.")
        return False

    print_block_summary(blockchain)

    try:
        block_index = int(input("\nWhich block do you want to tamper with? "))
    except ValueError:
        print("❌ Invalid block index.")
        return False

    if block_index <= 0 or block_index >= len(blockchain.chain):
        print("❌ Pick a mined block after genesis and before the end of the chain.")
        return False

    block = blockchain.chain[block_index]
    if not block.transactions:
        print("❌ The selected block has no transactions to tamper with.")
        return False

    try:
        tx_index = int(input("Which transaction in that block do you want to tamper with? "))
    except ValueError:
        print("❌ Invalid transaction index.")
        return False

    if tx_index < 0 or tx_index >= len(block.transactions):
        print("❌ Invalid transaction index.")
        return False

    transaction = block.transactions[tx_index]
    print("\nBefore tampering:")
    print(json.dumps(transaction.to_dict(), indent=2))

    field = input(
        "\nWhich field do you want to change? (amount/recipient/sender): "
    ).strip().lower()

    if field == "amount":
        try:
            new_value = float(input("Enter the new amount: "))
        except ValueError:
            print("❌ Invalid amount.")
            return False
    elif field in {"recipient", "sender"}:
        new_value = input(f"Enter the new {field}: ").strip()
        if not new_value:
            print("❌ Field value cannot be empty.")
            return False
    else:
        print("❌ Unsupported field.")
        return False

    setattr(transaction, field, new_value)

    print("\nAfter tampering:")
    print(json.dumps(transaction.to_dict(), indent=2))

    print("\nRe-running chain validation:")
    valid = blockchain.is_chain_valid()
    print("Valid" if valid else "Invalid")

    if not valid:
        print(
            "\nWhy it was detected: the transaction change altered the block's Merkle root, "
            "which changed the block hash. The next block still stores the old previous hash, "
            "so reverse chain validation detects the broken link immediately."
        )

    return valid
