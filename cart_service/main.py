from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, create_engine, Session
from contextlib import asynccontextmanager
from typing import List
from models import Cart, CartUpdate
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

app = FastAPI(title="Cart Service", lifespan=lifespan)

def get_session():
    """
    Dependency function to get a database session.
    It creates a session and ensures it's closed after the request.
    """
    with Session(engine) as session:
        yield session

router = APIRouter()

@router.get("/cart", response_model=List[Cart])
def get_users(user_id: int, session: Session = Depends(get_session)):
    """Retrieves list of cart from the database, filtered by user_id"""
    # Use the session to query the database
    query = session.query(Cart)
    if user_id is not None:
        query = query.filter(Cart.user_id == user_id)
    cart_list = query.all()
    return cart_list

@router.post("/cart", response_model=Cart)
def add_cart(cart_item: Cart, session: Session = Depends(get_session)):
    """add cart into the database."""
    # Use the session to query the database
    session.add(cart_item)
    session.commit()
    session.refresh(cart_item)
    return cart_item

@router.put("/cart", response_model=Cart)
def update_cart(cart_id: int, data_update: CartUpdate, session: Session = Depends(get_session)):
    """update product in the database."""
    # Use the session to query the database
    cart_item = session.get(Cart, cart_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_data = data_update.model_dump(exclude_unset=True)
    cart_item.sqlmodel_update(cart_data)
    session.add(cart_item)
    session.commit()
    session.refresh(cart_item)

    return {"message": "Update cart success"}


@router.delete("/cart", response_model=Cart)
def delete_cart(cart_id: int, session: Session = Depends(get_session)):
    """delete cart from the database."""
    # Use the session to query the database
    cart_item = session.get(Cart, cart_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart not found")

    session.delete(cart_item)
    session.commit()

    return {"message": "Delete cart success"}

app.include_router(router, tags=["cart"])