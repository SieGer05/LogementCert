from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from blockchain.blockchain import LogementBlockchain
import uvicorn
import time

app = FastAPI()
blockchain = LogementBlockchain(consensus_type="poa")

# Allow frontend JS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulated login system
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), role: str = Form(...)):
    if (username == "admin" and password == "admin" and role == "authority") or \
       (username == "owner" and password == "owner" and role == "owner"):
        return {"status": "success", "role": role}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/validator/add")
async def add_validator(file: UploadFile = File(...)):
    key_pem = (await file.read()).decode()
    try:
        blockchain.add_validator(key_pem)
        return {"message": "Validator added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/submit_property")
async def submit_property(
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    owner: str = Form("unknown_owner")
):
    tx = {
        "from": owner,
        "to": "authority",
        "title": title,
        "description": description,
        "price": price,
        "status": "pending",
        "timestamp": time.time()
    }
    blockchain.add_new_transaction(tx)
    return {"message": "Logement submitted for validation"}

@app.get("/properties")
def get_properties(owner: str):
    return blockchain.get_transactions_by_address(owner)

@app.get("/listings")
def get_validated_logements():
    return blockchain.get_validated_logements()

@app.get("/pending")
def get_pending():
    return [
        tx for tx in blockchain.unconfirmed_transactions
        if tx.get("status") == "pending"
    ]

@app.get("/stats")
def get_stats():
    return blockchain.get_chain_stats()


# You can add `/mine` endpoint for dev authority to approve housing
@app.post("/mine")
def mine(private_key: str = Form(...), title: str = Form(...)):
    for tx in blockchain.unconfirmed_transactions:
        if tx["title"] == title:
            index = blockchain.mine_transaction(tx, private_key)
            if index is not None:
                return {"message": f"Transaction '{title}' validated in block {index}"}
            else:
                raise HTTPException(status_code=400, detail="Mining failed")

    raise HTTPException(status_code=404, detail="Transaction not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
