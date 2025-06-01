from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from blockchain.blockchain import LogementBlockchain
import uvicorn
import time
from datetime import datetime

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

@app.get("/public_listings")
def public_listings():
    listings = blockchain.get_validated_logements()
    now = datetime.now()
    result = []

    for idx, entry in enumerate(listings):
        tx = entry.get("transaction", {})
        title = tx.get("title")
        price = tx.get("price")

        if not title or price is None:
            continue  # Skip invalid entries

        bookings = tx.get("bookings", [])
        booked_until = None

        # Determine if currently booked
        is_booked = False
        if bookings:
            try:
                latest = max(bookings, key=lambda b: b["end_date"])
                booked_until = latest["end_date"]
                is_booked = datetime.strptime(booked_until, "%Y-%m-%d") > now
            except Exception:
                is_booked = False

        result.append({
            "id": idx + 1,
            "title": title,
            "price": f"{price}DH/nuit",
            "priceValue": price,
            "emoji": "🏡",
            "isBooked": is_booked,
            "bookedUntil": booked_until,
            "type": tx.get("type", "appartement"),
            "location": tx.get("location", "Inconnu"),
            "maxGuests": tx.get("maxGuests", 4)
        })

    return result



@app.post("/book")
def book_logement(
        listing_id: int = Form(...),
        user_email: str = Form(...),
        user_name: str = Form(...),
        start_date: str = Form(...),
        end_date: str = Form(...)
    ):
    validated = blockchain.get_validated_logements()

    if listing_id < 1 or listing_id > len(validated):
        raise HTTPException(status_code=404, detail="Logement non trouvé")

    tx = validated[listing_id - 1]
    if "bookings" not in tx:
        tx["bookings"] = []

    tx["bookings"].append({
        "user": user_name,
        "email": user_email,
        "start_date": start_date,
        "end_date": end_date
    })

    return {"message": "Réservation enregistrée avec succès"}


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
