from fastapi import APIRouter, Form, HTTPException

auth_router = APIRouter()

@auth_router.post("/login")
def login(username: str = Form(...), password: str = Form(...), role: str = Form(...)):
   if (username == "admin" and password == "admin" and role == "authority") or \
      (username == "owner" and password == "owner" and role == "owner"):
      return {"status": "success", "role": role}
   raise HTTPException(status_code=401, detail="Invalid credentials")