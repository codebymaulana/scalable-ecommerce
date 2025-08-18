from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, create_engine, Session
from contextlib import asynccontextmanager
from typing import List
from models import Users, UsersUpdate
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

app = FastAPI(title="Users Service", lifespan=lifespan)

def get_session():
    """
    Dependency function to get a database session.
    It creates a session and ensures it's closed after the request.
    """
    with Session(engine) as session:
        yield session

router = APIRouter()

@router.get("/users/", response_model=List[Users])
def get_users(session: Session = Depends(get_session)):
    """Retrieves all users from the database."""
    # Use the session to query the database
    users = session.query(Users).all()
    return users

@router.post("/users/", response_model=Users)
def create_users(users: Users, session: Session = Depends(get_session)):
    """create new user into the database."""
    # Use the session to query the database
    session.add(users)
    session.commit()
    session.refresh(users)
    return users

@router.put("/users/{user_id}", response_model=Users)
def update_users(user_id: int, data_update: UsersUpdate, session: Session = Depends(get_session)):
    """update user in the database."""
    # Use the session to query the database
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = data_update.model_dump(exclude_unset=True)
    user.sqlmodel_update(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "update user data success"}


@router.delete("/users/{user_id}", response_model=Users)
def delete_users(user_id: int, session: Session = Depends(get_session)):
    """delete user from the database."""
    # Use the session to query the database
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()

    return {"message": "delete success"}

app.include_router(router, tags=["users"])