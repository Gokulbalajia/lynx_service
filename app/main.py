from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, factory, products, pets, cart, orders
from app.models.product import CategoryResponse
from app.models.pet import PetTypeResponse
from app.core.config import settings

app = FastAPI(
    title="Pet Shop API",
    description="Production-ready FastAPI backend for Pet Shop marketplace",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)

# Categories
app.include_router(
    factory.create_crud_router(
        table_name="categories",
        response_model=CategoryResponse,
        name="categories",
        tags=["Categories"]
    )
)

# Pet Types
app.include_router(
    factory.create_crud_router(
        table_name="pet_types",
        response_model=PetTypeResponse,
        name="pet-types",
        tags=["Pet Types"]
    )
)

# Products
app.include_router(products.router)

# Pets
app.include_router(pets.router)

# Cart
app.include_router(cart.router)

# Orders
app.include_router(orders.router)

@app.get("/")
def read_root():
    return {"message": "API Running Successfully"}
