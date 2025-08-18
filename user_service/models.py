from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class Users(SQLModel, table=True):
    """
    Represents a users in the database.
    This model is also used for API requests and responses.
    """
    id: Optional[int] = Field(primary_key=True)
    email: str = Field(index=True, unique=True)
    fullname: str = Field(default=None)

class UsersUpdate(SQLModel):
    """
    Represents a users update in the database.
    This model is also used for API requests and responses.
    """
    email: Optional[str] = None
    fullname: Optional[str] = None