# brownie/scripts/deploy.py

from brownie import MyContract, accounts


def main():
    dev = accounts[0]
    # Specify a valid gas price to overcome the base fee issue.
    deployed = MyContract.deploy(42, {'from': dev, 'gas_price': 1_000_000_000})
    print("Contract deployed at:", deployed.address)
