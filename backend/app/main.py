from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import import_products

# Create FastAPI app
app = FastAPI(title="Shopify Import Engine")

# CORS for frontend
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your router
app.include_router(import_products.router)
