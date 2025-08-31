from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field
from datetime import datetime


class OrderStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    shipping = "shipping"
    completed = "completed"

class PaymentStatus(str, Enum):
    unpaid = "unpaid"
    paid = "paid"

class ShippingMethod(str, Enum):
    standard = "standard"
    express = "express"
    overnight = "overnight"

class Orders(SQLModel, table=True):
    """
    Represents an order in the product service database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    order_status: OrderStatus = Field(default=OrderStatus.pending, index=True)
    total_amount: float = Field(default=0.0, index=True)
    payment_status: PaymentStatus = Field(default=PaymentStatus.unpaid, index=True)
    shipping_id: Optional[int] = Field(default=None, index=True)
    created_at: datetime = Field(default=datetime.utcnow(), index=True)
    updated_at: Optional[datetime] = Field(default=None,sa_column_kwargs={"onupdate": datetime.utcnow}, index=True)


class OrderUpdate(SQLModel):
    """
    Represents an update to an order in the order service database.
    """
    order_id: int
    order_status: Optional[OrderStatus] = None
    payment_status: Optional[PaymentStatus] = None


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
    shipping_method: ShippingMethod = Field(default=ShippingMethod.standard, index=True)
    tracking_number: Optional[str] = Field(default=None, index=True)
    shipped_at: Optional[datetime] = Field(default=None, index=True)
    delivered_at: Optional[datetime] = Field(default=None, index=True)


class ShippingUpdate(SQLModel):
    """
    Represents an update to a shipping record in the order service database.
    """
    shipping_id: int
    tracking_number: Optional[str] = None
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
