from typing import Optional
from sqlmodel import SQLModel, Field

class Products(SQLModel, table=True):
    """
    Represents a product in the product service database.
    This model stores a reference to the merchant_id from the Merchants table in another service.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    price: float = Field()
    stock: int = Field(default=0)
    image_url: Optional[str] = Field(default=None)
    merchant_id: int = Field(index=True)  # Reference to the merchant's ID from user service

class ProductUpdate(SQLModel):
    """
    Represents the data structure for updating a product.
    All fields are optional to allow partial updates.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None