from typing import Optional
from sqlmodel import SQLModel, Field

class Orders(SQLModel, table=True):
    """
    Represents an order in the product service database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    order_status: str = Field(default="pending", index=True)
    total_amount: float = Field(default=0.0, index=True)
    payment_status: str = Field(default="unpaid", index=True)
    created_at: Optional[str] = Field(default=None, index=True)
    updated_at: Optional[str] = Field(default=None, index=True)

class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", index=True)
    product_id: int = Field(index=True)
    quantity: int = Field(default=1, index=True)
    price: float = Field(default=0.0, index=True)
    subtotal: float = Field(default=0.0, index=True)

class Shipping(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", index=True)
    address: str = Field(index=True)
    shipping_status: str = Field(default="pending", index=True)
    tracking_number: Optional[str] = Field(default=None, index=True)
