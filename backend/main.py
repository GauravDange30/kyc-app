from fastapi import FastAPI
from fastapi.routing import APIRouter
from src.app.views import webhook_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from src.services import db_connector 

app = FastAPI()

router = APIRouter()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

route_prefix = "/kyc_verification"

app.include_router(router)
app.include_router(webhook_router, prefix=route_prefix)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")