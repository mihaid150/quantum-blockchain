# api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from wallet_resources.wallet import Wallet
from wallet_resources.blockchain import load_contract, get_contract_value

app = FastAPI()


class Transaction(BaseModel):
    nonce: int
    gas_price: int
    gas: int
    to: str
    value: int
    data: str = ""  # data payload


@app.get("")
async def create_wallet():
    """
    Endpoint to generate a new wallet_resources using quantum randomness.
    """
    try:
        wallet = Wallet()
        # For demonstration, we return the private key.
        return wallet.to_dict(include_private=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/wallet/sign")
async def sign_tx(tx: Transaction):
    """
    Endpoint to sign a transaction.
    """
    try:
        # In this demo, we create a new wallet_resources instance per request.
        wallet = Wallet()
        signed_tx = wallet.sign_transaction(tx.dict())
        return {"signed_transaction": signed_tx.rawTransaction.hex()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/contract/value")
async def get_contract_state():
    try:
        abi_path = "../brownie/build/contracts/MyContract.json"
        contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
        contract = load_contract(abi_path, contract_address)
        current_value = get_contract_value(contract)
        return {"value": current_value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=False)
