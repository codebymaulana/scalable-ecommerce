from typing import Optional
from sqlmodel import SQLModel, Field

class Payment(SQLModel, table=True):
    """
    Represents payments in the payment service database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(index=True)
    total_amount: float = Field(default=0.0, index=True)
    payment_status: str = Field(default="unpaid", index=True)
    payment_method_id: Optional[int] = Field(default=None, foreign_key="paymentmethod.id", index=True)
    created_at: Optional[str] = Field(default=None, index=True)
    updated_at: Optional[str] = Field(default=None, index=True)

class PaymentMethod(SQLModel, table=True):
    """
    Represents payment methods in the payment service database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    method_type: str = Field(default="credit_card", index=True)
    created_at: Optional[str] = Field(default=None, index=True)
    updated_at: Optional[str] = Field(default=None, index=True)

class PaymentUpdate(SQLModel):
    """
    Represents the data required to update a payment.
    """
    total_amount: Optional[float] = Field(default=None)
    payment_status: Optional[str] = Field(default=None)
    payment_method_id: Optional[int] = Field(default=None, foreign_key="paymentmethod.id")
    updated_at: Optional[str] = Field(default=None)