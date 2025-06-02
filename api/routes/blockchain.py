from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from api.services.blockchain_service import blockchain_service
import time

blockchain_router = APIRouter()

@blockchain_router.post("/validator/add")
async def add_validator(file: UploadFile = File(...)):
   key_pem = (await file.read()).decode()
   try:
      blockchain_service.add_validator(key_pem)
      return {"message": "Validator added successfully"}
   except Exception as e:
      raise HTTPException(status_code=400, detail=str(e))

@blockchain_router.post("/submit_property")
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
   blockchain_service.add_new_transaction(tx)
   return {"message": "Logement submitted for validation"}

@blockchain_router.get("/properties")
def get_properties(owner: str):
   return blockchain_service.get_transactions_by_address(owner)

@blockchain_router.get("/pending")
def get_pending():
   return [
      tx for tx in blockchain_service.unconfirmed_transactions
      if tx.get("status") == "pending"
   ]

@blockchain_router.get("/stats")
def get_stats():
   return blockchain_service.get_chain_stats()

@blockchain_router.post("/mine")
def mine(private_key: str = Form(...), title: str = Form(...)):
   for tx in blockchain_service.unconfirmed_transactions:
      if tx["title"] == title:
         index = blockchain_service.mine_transaction(tx, private_key)
         if index is not None:
            return {"message": f"Transaction '{title}' validated in block {index}"}
         else:
            raise HTTPException(status_code=400, detail="Mining failed")
   raise HTTPException(status_code=404, detail="Transaction not found")