from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from blockchain.blockchain import LogementBlockchain
from Crypto.key_manager import KeyManager
from Crypto.signature import SignatureManager

app = FastAPI(title="Logement Blockchain API")

# Instantiate blockchain (could also be done per user/session if needed)
blockchain = LogementBlockchain(consensus_type="poa")
key_manager = KeyManager()
sig_manager = SignatureManager()

class LogementTransaction(BaseModel):
    from_: str
    to: str
    logement_id: str
    action: str  
    property_type: Optional[str] = None
    address: Optional[str] = None
    price: Optional[int] = None
    monthly_rent: Optional[int] = None
    deposit: Optional[int] = None
    duration_months: Optional[int] = None
    cadastral_ref: Optional[str] = None
    status: str

class ValidatorKey(BaseModel):
    public_key: str

class ValidatorSignature(BaseModel):
    private_key: str

@app.get("/logements")
def list_validated_logements():
    logements = blockchain.get_validated_logements()
    return [item["transaction"] for item in logements]

@app.post("/logement")
def create_logement(tx: LogementTransaction):
    tx_data = tx.dict()
    tx_data["from"] = tx_data.pop("from_")  # Fix Pydantic naming
    blockchain.add_new_transaction(tx_data)
    return {"message": "Transaction added to mempool", "logement_id": tx_data["logement_id"]}

@app.post("/logement/{logement_id}/validate")
def validate_logement(logement_id: str, sig: ValidatorSignature):
    tx = next((t for t in blockchain.transaction_pool if t["logement_id"] == logement_id), None)
    if not tx:
        raise HTTPException(status_code=404, detail="Logement transaction not found")

    block_index = blockchain.mine(private_key_pem=sig.private_key)
    if block_index is None:
        raise HTTPException(status_code=403, detail="Validation failed (unauthorized validator or no transactions)")

    return {"message": f"Logement {logement_id} validated in block {block_index}"}

@app.post("/logement/{logement_id}/cancel")
def cancel_logement(logement_id: str):
    original_len = len(blockchain.transaction_pool)
    blockchain.transaction_pool = [tx for tx in blockchain.transaction_pool if tx["logement_id"] != logement_id]
    if len(blockchain.transaction_pool) == original_len:
        raise HTTPException(status_code=404, detail="Logement transaction not found or already mined")
    return {"message": f"Transaction for logement {logement_id} cancelled"}

@app.get("/logement/{logement_id}")
def get_logement_details(logement_id: str):
    all_txs = blockchain.get_all_transactions()
    for item in all_txs:
        tx = item["transaction"]
        if tx["logement_id"] == logement_id:
            return tx
    raise HTTPException(status_code=404, detail="Logement not found")

@app.get("/logements/user/{user}")
def get_user_logements(user: str):
    txs = blockchain.get_transactions_by_address(user)
    return [item["transaction"] for item in txs]

@app.post("/validator")
def add_validator(key: ValidatorKey):
    blockchain.add_validator(key.public_key.encode())
    return {"message": "Validator public key added"}

@app.get("/validators")
def list_validators():
    return blockchain.get_validators()
