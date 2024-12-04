from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.user import User
from app.schemas.checkout import CheckoutCreate, CheckoutResponse
from app.models.library import Checkout
from app.api.deps import get_current_user, get_db
from datetime import date


router = APIRouter()


@router.post("/checkout", response_model=CheckoutResponse)
def checkout_item(
        checkout: CheckoutCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if current_user.role != "member":
        raise HTTPException(status_code=403, detail="Only members can checkout items")

    db_checkout = Checkout(
        user_id=current_user.id,
        item_type=checkout.item_type,
        item_id=checkout.item_id,
        checkout_date=date.today()
    )
    db.add(db_checkout)
    db.commit()
    db.refresh(db_checkout)
    return db_checkout


@router.post("/return/{checkout_id}")
def return_item(
        checkout_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    checkout = db.query(Checkout).filter(
        Checkout.id == checkout_id,
        Checkout.user_id == current_user.id
    ).first()

    if not checkout:
        raise HTTPException(status_code=404, detail="Checkout not found")

    if checkout.return_date:
        raise HTTPException(status_code=400, detail="Item already returned")

    checkout.return_date = date.today()
    db.commit()
    return {"message": "Item returned successfully"}


@router.get("/history/item/{item_type}/{item_id}", response_model=List[CheckoutResponse])
def get_item_history(
        item_type: str,
        item_id: int,
        db: Session = Depends(get_db)
):
    return db.query(Checkout).filter(
        Checkout.item_type == item_type,
        Checkout.item_id == item_id
    ).all()


@router.get("/history/me", response_model=List[CheckoutResponse])
def get_user_history(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return db.query(Checkout).filter(Checkout.user_id == current_user.id).all()