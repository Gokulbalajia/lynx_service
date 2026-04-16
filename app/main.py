from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints import (
    auth_endpoint,
    user_endpoint,
    category_endpoint,
    pet_type_endpoint,
    pet_breed_endpoint,
    product_endpoint,
    pet_endpoint,
    cart_endpoint,
    order_endpoint,
    address_endpoint,
    payment_endpoint,
    shipment_endpoint,
    upload_endpoint
)

app = FastAPI(
    title="Pet Shop API",
    description="Clean Architecture FastAPI backend",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_endpoint.router)
app.include_router(user_endpoint.router)
app.include_router(category_endpoint.router)
app.include_router(pet_type_endpoint.router)
app.include_router(pet_breed_endpoint.router)
app.include_router(product_endpoint.router)
app.include_router(pet_endpoint.router)
app.include_router(cart_endpoint.router)
app.include_router(order_endpoint.router)
app.include_router(address_endpoint.router)
app.include_router(payment_endpoint.router)
app.include_router(shipment_endpoint.router)
app.include_router(upload_endpoint.router)

@app.get("/")
def read_root():
    return {"message": "Backend Running Successfully"}
