from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, create_engine, Session
from contextlib import asynccontextmanager
from typing import List
from models import Payment, PaymentMethod, PaymentUpdate
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

app = FastAPI(title="Payments Service", lifespan=lifespan)

def get_session():
    """
    Dependency function to get a database session.
    It creates a session and ensures it's closed after the request.
    """
    with Session(engine) as session:
        yield session

router = APIRouter()

@router.get("/payment", response_model=List[Payment])
def get_history_payment(session: Session = Depends(get_session)):
    """Retrieves list of order from the database, filtered by user_id"""
    # Use the session to query the database
    query = session.query(Payment)

    return query.all()

@router.post("/payment/method", response_model=PaymentMethod)
def create_payment_method(payment_method_data: PaymentMethod, session: Session = Depends(get_session)):
    """create payment method into the database."""
    # Use the session to add the new payment method
    session.add(payment_method_data)
    session.commit()
    session.refresh(payment_method_data)

    return payment_method_data

@router.put("/payment/method", response_model=PaymentMethod)
def update_payment_method(payment_mtd_id: int, payment_method_data: PaymentMethod, session: Session = Depends(get_session)):
    """update payment method into the database."""
    # Use the session to query the database
    existing_payment_method = session.get(PaymentMethod, payment_mtd_id)
    if not existing_payment_method:
        raise HTTPException(status_code=404, detail="Payment method not found")
    payment_method_update = payment_method_data.model_dump(exclude_unset=True)
    existing_payment_method.sqlmodel_update(payment_method_update)
    session.add(existing_payment_method)
    session.commit()
    session.refresh(existing_payment_method)

    return existing_payment_method

@router.post("/payment", response_model=Payment)
def create_payment(payment_data: Payment, session: Session = Depends(get_session)):
    """create payment into the database."""
    # Use the session to add the new payment
    session.add(payment_data)
    session.commit()
    session.refresh(payment_data)

    return payment_data

@router.put("/payment", response_model=Payment)
def update_payment(payment_id: int, payment_data: PaymentUpdate, session: Session = Depends(get_session)):
    """update payment into the database."""
    # Use the session to query the database
    existing_payment = session.get(Payment, payment_id)
    if not existing_payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    payment_update = payment_data.model_dump(exclude_unset=True)
    existing_payment.sqlmodel_update(payment_update)
    session.add(existing_payment)
    session.commit()
    session.refresh(existing_payment)

    return existing_payment

app.include_router(router, tags=["payment"], prefix="/api/v1")