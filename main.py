from fastapi import FastAPI
from api.middleware.cors import setup_cors
from api.routes.auth import auth_router
from api.routes.blockchain import blockchain_router
from api.routes.listings import listings_router

app = FastAPI(title="LogementCert API")

setup_cors(app)

app.include_router(auth_router, prefix="/auth")
app.include_router(blockchain_router, prefix="/blockchain")
app.include_router(listings_router, prefix="/listings")

if __name__ == "__main__":
   import uvicorn
   uvicorn.run(app, host="0.0.0.0", port=8000)