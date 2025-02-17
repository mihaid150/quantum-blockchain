# wallet/api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from wallet import Wallet

app = FastAPI()


class Transaction(BaseModel):
    nonce: int
    gas_price: int
    gas: int
    to: str
    value: int
    data: str = ""  # data payload optional


@app.get("/wallet")
async def create_wallet():
    """
    Endpoint to generate a new wallet using quantum randomness.
    Note: In production, avoid returning private keys.
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
    In a production system, you would securely persist and retrieve the wallet.
    """
    try:
        # In this demo, we create a new wallet instance per request.
        wallet = Wallet()
        signed_tx = wallet.sign_transaction(tx.dict())
        return {"signed_transaction": signed_tx.rawTransaction.hex()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=False)
