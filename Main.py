import random
import json
import copy
from Transaction import Transaction, Wallet
from MerkleTree import MerkleTree


def print_header(title):
    print(f"\n{'='*15} {title.upper()} {'='*15}")


def mostra_saldi(wallets, balances):
    print("\n--- Current Balances ---")
    for name, address in wallets.items():
        print(
            f"User: {name} | Balance: {balances[name]} COIN | Address: {address[:17]}..."
        )
    print("---------------------\n")


def main():
    # Dictionaries to store generated wallets and fictitious balances
    wallets_obj = {}  # { "Alice": Wallet() }
    wallets_addr = {}  # { "Alice": "base64_address..." }
    balances = {}  # { "Alice": 1000 }

    transactions_list = []
    merkle_tree = None

    print("Welcome to the Blockchain and Merkle Tree Demo!")

    while True:
        print_header("Main Menu")
        print("1. Create Users (Wallets)")
        print("2. Create a Manual Transaction")
        print("3. Generate Random Transactions in Batch")
        print("4. Generate and Display the Merkle Tree")
        print("5. Verify a Transaction (Merkle Proof)")
        print("6. Tamper with a Transaction (Attack!)")
        print("7. Exit")

        scelta = input("\nChoose an option (1-7): ")

        # ==========================================
        # OPTION 1: CREATE USERS AND ASSIGN BALANCES
        # ==========================================
        if scelta == "1":
            print_header("User Creation")
            try:
                num_utenti = int(input("How many users do you want to generate? "))
                for i in range(num_utenti):
                    nome = input(
                        f"Enter the name for user {i+1} (e.g. Alice, Bob): "
                    ).strip()
                    if nome in wallets_obj:
                        print("Name already exists, try again.")
                        continue

                    nuovo_wallet = Wallet()
                    wallets_obj[nome] = nuovo_wallet
                    wallets_addr[nome] = nuovo_wallet.get_address()
                    # Assign a fictitious initial balance of 1000 COIN to all users
                    balances[nome] = 1000.0
                    print(f"✅ Wallet for {nome} generated successfully!")

                mostra_saldi(wallets_addr, balances)
            except ValueError:
                print("❌ Please enter a valid number.")

        # ==========================================
        # OPTION 2: MANUAL TRANSACTION
        # ==========================================
        elif scelta == "2":
            print_header("New Transaction")
            if len(wallets_obj) < 2:
                print(
                    "❌ You must create at least 2 users before making a transaction (Use option 1)."
                )
                continue

            mostra_saldi(wallets_addr, balances)

            mittente = input("Who sends the funds? (Enter the name): ").strip()
            destinatario = input("Who receives the funds? (Enter the name): ").strip()

            if mittente not in wallets_obj or destinatario not in wallets_obj:
                print("❌ Invalid names. Make sure to write them correctly.")
                continue

            try:
                ammontare = float(
                    input(
                        f"How much do you want to send from {mittente} to {destinatario}? "
                    )
                )
                if ammontare <= 0 or ammontare > balances[mittente]:
                    print("❌ Invalid amount or insufficient funds!")
                    continue

                # Transaction creation
                tx = Transaction(
                    sender=wallets_addr[mittente],
                    recipient=wallets_addr[destinatario],
                    amount=ammontare,
                )

                # Transaction signing
                tx.sign_transaction(wallets_obj[mittente])
                transactions_list.append(tx)

                # Update fictitious balances
                balances[mittente] -= ammontare
                balances[destinatario] += ammontare

                print("\n✅ Transaction created and signed successfully!")
                print("Transaction Dictionary Details:")
                print(json.dumps(tx.to_dict(), indent=4))

            except ValueError:
                print("❌ Please enter a valid numeric amount.")

        # ==========================================
        # OPTION 3: RANDOM TRANSACTIONS
        # ==========================================
        elif scelta == "3":
            print_header("Random Transaction Generator")
            if len(wallets_obj) < 2:
                print("❌ Create at least 2 users first (Option 1).")
                continue

            try:
                num_tx = int(
                    input("How many random transactions do you want to generate? ")
                )
                utenti = list(wallets_obj.keys())

                for _ in range(num_tx):
                    mittente, destinatario = random.sample(utenti, 2)
                    ammontare = round(random.uniform(1.0, 50.0), 2)

                    tx = Transaction(
                        sender=wallets_addr[mittente],
                        recipient=wallets_addr[destinatario],
                        amount=ammontare,
                    )
                    tx.sign_transaction(wallets_obj[mittente])
                    transactions_list.append(tx)

                    # Update fictitious balances without fund checks for demo simplicity
                    balances[mittente] -= ammontare
                    balances[destinatario] += ammontare

                print(f"\n✅ Generated {num_tx} random transactions.")
                # print the transactions details
                for idx, tx in enumerate(transactions_list[-num_tx:]):
                    print(
                        f" [{idx}] Sender: {tx.sender[:8]}... | Recipient: {tx.recipient[:8]}... | Amount: {tx.amount}"
                    )

                mostra_saldi(wallets_addr, balances)

            except ValueError:
                print("❌ Please enter a valid number.")

        # ==========================================
        # OPTION 4: BUILD MERKLE TREE
        # ==========================================
        elif scelta == "4":
            print_header("Merkle Tree")
            if not transactions_list:
                print(
                    "❌ There are no transactions to add to the block! Create some first."
                )
                continue

            merkle_tree = MerkleTree(transactions_list)
            print("✅ Merkle Tree built successfully!\n")
            print("Structure visualization:")
            print(merkle_tree)  # Uses the __str__ method you defined

        # ==========================================
        # OPTION 5: VERIFY PROOF
        # ==========================================
        elif scelta == "5":
            print_header("Merkle Proof Verification")
            if not merkle_tree or not transactions_list:
                print(
                    "❌ You must first generate transactions and build the Merkle Tree (Options 2/3 and 4)."
                )
                continue

            print("Transactions in the current block:")
            for idx, tx in enumerate(transactions_list):
                print(f" [{idx}] Sender: {tx.sender[:8]}... | Amount: {tx.amount}")

            try:
                tx_index = int(
                    input("\nEnter the index of the transaction to verify: ")
                )
                if tx_index < 0 or tx_index >= len(transactions_list):
                    print("❌ Invalid index.")
                    continue

                # Get the transaction
                tx_to_verify = transactions_list[tx_index]
                # Calculate the leaf hash using the same method as the tree (double hash)
                tx_hash = merkle_tree._hash_transaction(tx_to_verify)

                # Get the proof and the root
                proof = merkle_tree.get_proof(tx_index)
                root = merkle_tree.get_root()

                print(f"\nGenerating Proof for transaction [{tx_index}]...")
                print(f"Transaction Hash (Leaf): {tx_hash}")
                print(f"Tree Root: {root}")
                print("Proof Path (Siblings):", proof)

                # Execute the verification
                is_valid = merkle_tree.verify_proof(tx_hash, proof, root)

                if is_valid:
                    print("\n✅ SUCCESS: The transaction belongs to the Merkle Tree!")
                else:
                    print(
                        "\n❌ FAILURE: The transaction does not belong to the Merkle Tree."
                    )

            except ValueError:
                print("❌ Please enter a valid numeric index.")

        # ==========================================
        # OPTION 6: TAMPER AND VERIFY
        # ==========================================
        elif scelta == "6":
            print_header("Attack: Transaction Tampering")
            if not merkle_tree or not transactions_list:
                print(
                    "❌ Create transactions and the Merkle Tree before running this test."
                )
                continue

            print("Available transactions:")
            for idx, tx in enumerate(transactions_list):
                print(f" [{idx}] Sender: {tx.sender[:8]}... | Amount: {tx.amount}")

            try:
                tx_index = int(
                    input(
                        "\nWhich transaction do you want to tamper with? (Enter index): "
                    )
                )
                if tx_index < 0 or tx_index >= len(transactions_list):
                    print("❌ Invalid index.")
                    continue

                # Clone the transaction to avoid corrupting the original object in memory,
                # but we'll pretend the attacker modified it
                tx_hacked = copy.deepcopy(transactions_list[tx_index])

                nuovo_importo = float(
                    input(
                        f"The current amount is {tx_hacked.amount}. What do you want to change it to? "
                    )
                )
                tx_hacked.amount = nuovo_importo

                print("\n☠️ Transaction tampered!")
                print(json.dumps(tx_hacked.to_dict(), indent=4))

                print("\n--- Security Verification Phase ---")

                # 1. Digital signature verification
                print("1. Checking Digital Signature validity...")
                is_sig_valid = tx_hacked.verify_signature()
                if not is_sig_valid:
                    print(
                        "   ❌ INVALID SIGNATURE! The data was altered after signing."
                    )
                else:
                    print(
                        "   ✅ Valid signature (this shouldn't happen if you changed the data)."
                    )

                # 2. Merkle Proof verification
                print("\n2. Checking block inclusion (Merkle Proof)...")
                fake_tx_hash = merkle_tree._hash_transaction(tx_hacked)
                proof = merkle_tree.get_proof(tx_index)
                root = merkle_tree.get_root()

                print(f"   Hash calculated post-tampering: {fake_tx_hash}")
                is_merkle_valid = merkle_tree.verify_proof(fake_tx_hash, proof, root)

                if not is_merkle_valid:
                    print(
                        "   ❌ MERKLE PROOF FAILED! The modified transaction hash does not lead to the original Root."
                    )
                else:
                    print("   ✅ Valid Merkle Proof (this shouldn't happen).")

            except ValueError:
                print("❌ Invalid input.")

        # ==========================================
        # OPTION 7: EXIT
        # ==========================================
        elif scelta == "7":
            print("Exiting the Demo. See you next time!")
            break
        else:
            print("❌ Invalid option, try again.")


if __name__ == "__main__":
    main()
