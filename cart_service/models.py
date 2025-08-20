from typing import Optional
from sqlmodel import SQLModel, Field

class Cart(SQLModel, table=True):
    """
    Represents a cart in the product service database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(index=True)
    quantity: int = Field(default=1, index=True)
    user_id: int = Field(index=True)

class CartUpdate(SQLModel):
    """
    Represents the data structure for updating a cart.
    All fields are optional to allow partial updates.
    """
    quantity: Optional[int] = None