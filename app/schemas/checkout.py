from datetime import date
from pydantic import BaseModel


class CheckoutCreate(BaseModel):
    item_type: str
    item_id: int


class CheckoutResponse(BaseModel):
    id: int
    user_id: int
    item_type: str
    item_id: int
    checkout_date: date
    return_date: date | None

    class Config:
        from_attributes = True
