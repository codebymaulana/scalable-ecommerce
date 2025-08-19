from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class Users(SQLModel, table=True):
    """
    Represents a users in the database.
    This model is also used for API requests and responses.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    fullname: str = Field(default=None)
    merchant : Optional["Merchants"] = Relationship(back_populates="user")

class Merchants(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    merchant_id: int = Field(foreign_key="users.id")
    user : Optional[Users] = Relationship(back_populates="merchant")

class UsersUpdate(SQLModel):
    """
    Represents a users update in the database.
    This model is also used for API requests and responses.
    """
    email: Optional[str] = None
    fullname: Optional[str] = None