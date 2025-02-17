# wallet.py

import requests
import os
from eth_keys import keys
from eth_account import Account
from config import QUANTUM_API_URL

# define __all__ to expose only the Wallet class
__all__ = ['Wallet']


def _get_quantum_random_bytes():
    """
    Fetch a 32-byte random value from a quantum random generator API.
    Falls back to os.urandom if the API call fails.
    """
    try:
        response = requests.get(QUANTUM_API_URL)
        response.raise_for_status()
        data = response.json()
        # Assuming the API returns a JSON object like: {"random": "a1b2c3..."}
        random_hex = data.get("random")
        if not random_hex:
            raise ValueError("API response missing 'random' field.")
        random_bytes = bytes.fromhex(random_hex)
        if len(random_bytes) != 32:
            raise ValueError("Random value must be 32 bytes long.")
        return random_bytes
    except Exception as e:
        print(f"Falling back to os.urandom due to: {e}")
        return os.urandom(32)


def _generate_wallet(random_bytes):
    """
    Generate a wallet (private key, public key, address) from a 32-byte random source.
    """
    if len(random_bytes) != 32:
        raise ValueError("Random bytes must be 32 bytes long")
    private_key = keys.PrivateKey(random_bytes)
    public_key = private_key.public_key
    address = public_key.to_checksum_address()
    return private_key, public_key, address


class Wallet:
    """
    A class representing a digital wallet.
    It encapsulates key generation, storage, and signing operations.
    """

    def __init__(self, random_bytes=None):
        if random_bytes is None:
            random_bytes = _get_quantum_random_bytes()
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
        Return wallet information as a dictionary.
        Note: Do not include the private key in production responses.
        """
        data = {
            "address": self.address,
            "public_key": self.public_key.to_hex()
        }
        if include_private:
            data["private_key"] = self.private_key.to_hex()
        return data
