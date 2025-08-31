from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, create_engine, Session
from contextlib import asynccontextmanager
from typing import List
from models import Orders, OrderItem, OrderUpdate, OrderRequest
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

app = FastAPI(title="Order Service", lifespan=lifespan)

def get_session():
    """
    Dependency function to get a database session.
    It creates a session and ensures it's closed after the request.
    """
    with Session(engine) as session:
        yield session

router = APIRouter()

@router.get("/order", response_model=List[Orders])
def get_all_orders(session: Session = Depends(get_session)):
    """Retrieves list of order from the database"""
    # Use the session to query the database
    query = session.query(Orders)
    order_list = query.all()
    return order_list

@router.post("/order", response_model=Orders)
def place_order(order_data: OrderRequest, session: Session = Depends(get_session)):
    """place order into the database."""
    try:
        total_amount = sum(item.price * item.quantity for item in order_data.items)

        new_order = Orders(user_id=order_data.user_id, total_amount=total_amount)
        session.add(new_order)
        session.commit()

        for item in order_data.items:
            order_item = OrderItem(order_id=new_order.id,
                                   product_id=item.product_id,
                                   quantity=item.quantity,
                                   price=item.price)
            session.add(order_item)
            session.commit()

        order_data = session.get(Orders, new_order.id)

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to place order: {str(e)}")

    return order_data

@router.put("/order", response_model=Orders)
def update_product(data_update: OrderUpdate, session: Session = Depends(get_session)):
    """update order in the database."""
    # Use the session to query the database
    order_data = session.get(Orders, data_update.order_id)
    if not order_data:
        raise HTTPException(status_code=404, detail="Order not found")

    try:
        order_update = data_update.model_dump(exclude_unset=True)
        order_data.sqlmodel_update(order_update)
        session.add(order_data)
        session.commit()
        session.refresh(order_data)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update order: {str(e)}")


    return order_data

@router.delete("/order/{order_id}", response_model=Orders)
def delete_cart(order_id: int, session: Session = Depends(get_session)):
    """delete order from the database."""
    # Use the session to query the database
    order = session.get(Orders, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    session.delete(order)
    session.commit()

    return {"message": "Delete order success"}

app.include_router(router, tags=["order"], prefix="/api/v1")