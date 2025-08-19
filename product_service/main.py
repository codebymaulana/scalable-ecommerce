from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, create_engine, Session
from contextlib import asynccontextmanager
from typing import List
from models import Products, ProductUpdate
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """Creates the database tables based on your SQLModel definitions."""
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that runs on application startup and shutdown.
    It's the perfect place to create the database tables.
    """
    create_db_and_tables()
    yield

app = FastAPI(title="Product Service", lifespan=lifespan)

def get_session():
    """
    Dependency function to get a database session.
    It creates a session and ensures it's closed after the request.
    """
    with Session(engine) as session:
        yield session

router = APIRouter()

@router.get("/products/", response_model=List[Products])
def get_users(session: Session = Depends(get_session)):
    """Retrieves all product from the database."""
    # Use the session to query the database
    users = session.query(Products).all()
    return users

@router.post("/products/", response_model=Products)
def create_users(product: Products, session: Session = Depends(get_session)):
    """create new product into the database."""
    # Use the session to query the database
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.put("/products/{product_id}", response_model=Products)
def update_product(product_id: int, data_update: ProductUpdate, session: Session = Depends(get_session)):
    """update product in the database."""
    # Use the session to query the database
    product = session.get(Products, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_data = data_update.model_dump(exclude_unset=True)
    product.sqlmodel_update(product_data)
    session.add(product)
    session.commit()
    session.refresh(product)

    return {"message": "update user data success"}


@router.delete("/products/{product_id}", response_model=Products)
def delete_users(product_id: int, session: Session = Depends(get_session)):
    """delete user from the database."""
    # Use the session to query the database
    product = session.get(Products, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    session.delete(product)
    session.commit()

    return {"message": "delete success"}

app.include_router(router, tags=["products"])