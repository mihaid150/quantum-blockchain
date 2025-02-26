# wallet_resources.py

from eth_keys import keys
from eth_account import Account
from quantis.quantum_random_pool import QuantumRandomPool

# define __all__ to expose only the Wallet class
__all__ = ['Wallet']

quantum_random_pool = QuantumRandomPool()


def _generate_wallet(random_bytes):
    """
    Generate a wallet_resources (private key, public key, address) from a 32-byte random source.
    """
    if len(random_bytes) != 32:
        raise ValueError("Random bytes must be 32 bytes long")
    private_key = keys.PrivateKey(random_bytes)
    public_key = private_key.public_key
    address = public_key.to_checksum_address()
    return private_key, public_key, address


class Wallet:
    """
    A class representing a digital wallet_resources.
    It encapsulates key generation, storage, and signing operations.
    """

    def __init__(self, random_bytes=None):
        if random_bytes is None:
            print(f"There are {quantum_random_pool.total_numbers_available()} numbers available in the pool.")
            random_bytes = quantum_random_pool.get_random_bytes()
        self.private_key, self.public_key, self.address = _generate_wallet(random_bytes)

    def sign_transaction(self, txn_dict):
        """
        Sign an Ethereum transaction using the stored private key.
        txn_dict should include nonce, gasPrice, gas, to, value, data, etc.
        """
        acct = Account.from_key(self.private_key.to_hex())
        signed_txn = acct.sign_transaction(txn_dict)
        return signed_txn

    def to_dict(self, include_private=False):
        """
        Return wallet_resources information as a dictionary.
        Note: Do not include the private key in production responses.
        """
        data = {
            "address": self.address,
            "public_key": self.public_key.to_hex()
        }
        if include_private:
            data["private_key"] = self.private_key.to_hex()
        return data
