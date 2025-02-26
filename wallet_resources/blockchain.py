# wallet_resources/blockchain.py

import json
import os
from web3 import Web3


# url for hardhat node
RPC_URL = os.getenv("HARDHAT_RPC_URL", "http://127.0.0.1:8546")

# web3 connection initialization
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    raise ConnectionError(f"Failed to connect to Hardhat node at {RPC_URL}")


def load_contract(abi_path, contract_address):
    """
    Load a contract given the path to its ABI JSON file and its deployed address.
    """
    with open(abi_path, "r") as f:
        contract_data = json.load(f)
    contract_abi = contract_data.get("abi")
    if not contract_abi:
        raise ValueError("ABI not found in the provided JSON file")
    return w3.eth.contract(address=contract_address, abi=contract_abi)


def get_contract_value(contract):
    """
    Function that calls a getter on the contract
    """
    return contract.functions.value().call()