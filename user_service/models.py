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
    is_merchant: bool = Field(default=False, index=True)

class UsersUpdate(SQLModel):
    """
    Represents a users update in the database.
    This model is also used for API requests and responses.
    """
    email: Optional[str] = None
    fullname: Optional[str] = None

class Address(SQLModel, table=True):
    """
    Represents an address in the database.
    This model is also used for API requests and responses.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    street: str = Field(index=True)
    city: str = Field(index=True)
    state: str = Field(index=True)
    zip_code: str = Field(index=True)
    country: str = Field(index=True)
    default: bool = Field(default=False, index=True)