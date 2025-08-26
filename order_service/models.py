from typing import Optional, List
from sqlmodel import SQLModel, Field
from datetime import datetime

class Orders(SQLModel, table=True):
    """
    Represents an order in the product service database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    order_status: str = Field(default="pending", index=True)
    total_amount: float = Field(default=0.0, index=True)
    payment_status: str = Field(default="unpaid", index=True)
    created_at: datetime = Field(default=datetime.utcnow(), index=True)
    updated_at: Optional[str] = Field(default=None, index=True)


class OrderUpdate(SQLModel):
    """
    Represents an update to an order in the order service database.
    """
    order_status: Optional[str] = None
    payment_status: Optional[str] = None
    updated_at: Optional[str] = None


class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", index=True)
    product_id: int = Field(index=True)
    quantity: int = Field(default=1, index=True)
    price: float = Field(default=0.0, index=True)
    subtotal: float = Field(default=0.0, index=True)

class OrderRequest(SQLModel):
    """
    Represents a request to create an order in the order service database.
    """
    user_id: int
    items: List[OrderItem] = Field(default_factory=list)

class Shipping(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", index=True)
    address: str = Field(index=True)
    shipping_status: str = Field(default="pending", index=True)
    tracking_number: Optional[str] = Field(default=None, index=True)
