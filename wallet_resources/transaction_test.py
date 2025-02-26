# wallet_resources/transaction_test.py

from web3 import Web3

from wallet_resources.wallet import Wallet


def fund_wallet(w3, custom_wallet, amount_eth=0.01):
    """
    Funds the custom wallet with the specified amount of Ether if its balance is too low.
    Uses one of the pre-funded Hardhat accounts (Account #0 in this example).
    """
    # Pre-funded Hardhat account details (Account #0)
    pre_funded_account = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
    pre_funded_private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

    # Check the current balance of the custom wallet
    balance = w3.eth.get_balance(custom_wallet.address)
    if balance >= w3.to_wei(amount_eth, "ether"):
        print("Custom wallet already has sufficient funds.")
        return

    print(f"Funding custom wallet {custom_wallet.address} with {amount_eth} ETH...")
    nonce = w3.eth.get_transaction_count(pre_funded_account)
    tx = {
        "nonce": nonce,
        "to": custom_wallet.address,
        "value": w3.to_wei(amount_eth, "ether"),
        "gas": 21000,
        "gasPrice": w3.to_wei("1", "gwei"),
    }
    signed_tx = w3.eth.account.sign_transaction(tx, pre_funded_private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Funding transaction sent with hash: {tx_hash.hex()}")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Funding transaction confirmed.")


if __name__ == "__main__":
    # Connect to Hardhat node
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    if not w3.is_connected():
        raise ConnectionError("Failed to connect to the Hardhat node.")

    # Create a custom wallet using quantum randomness
    custom_wallet = Wallet()
    wallet_address = custom_wallet.address
    print(f"Custom Wallet Address: {wallet_address}")

    # Automatically fund the wallet if it doesn't have enough funds
    fund_wallet(w3, custom_wallet, amount_eth=0.01)

    # Get the current nonce for the custom wallet address
    nonce = w3.eth.get_transaction_count(wallet_address)
    print(f"Nonce for {wallet_address}: {nonce}")

    # Create a simple transaction: sending a small amount of Ether to itself
    txn = {
        "nonce": nonce,
        "gasPrice": w3.to_wei("1", "gwei"),
        "gas": 21000,
        "to": wallet_address,  # sending to itself
        "value": w3.to_wei(0.001, "ether"),
        # data field is optional; omitted here
    }

    # Sign the transaction using the custom wallet's private key
    signed_txn = custom_wallet.sign_transaction(txn)
    print("Signed transaction:", signed_txn.rawTransaction.hex())

    # Send the signed transaction as a raw transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Transaction sent with hash: {tx_hash.hex()}")

    # Wait for the transaction receipt (mining a block if needed)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction mined in block: {receipt.blockNumber}")
    print("Transaction receipt:", receipt)
