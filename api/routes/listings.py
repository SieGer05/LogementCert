from fastapi import APIRouter, Form, HTTPException
from api.services.blockchain_service import blockchain_service
from datetime import datetime

listings_router = APIRouter()

@listings_router.get("/public_listings")
def public_listings():
   listings = blockchain_service.get_validated_logements()
   now = datetime.now()
   result = []

   for idx, entry in enumerate(listings):
      tx = entry.get("transaction", {})
      title = tx.get("title")
      price = tx.get("price")

      if not title or price is None:
         continue

      bookings = tx.get("bookings", [])
      booked_until = None
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

@listings_router.post("/book")
def book_logement(
   listing_id: int = Form(...),
   user_email: str = Form(...),
   user_name: str = Form(...),
   start_date: str = Form(...),
   end_date: str = Form(...)
):
   validated = blockchain_service.get_validated_logements()
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