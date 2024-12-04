import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.library import Checkout
from datetime import date

def test_checkout_item(
    client: TestClient, db: Session, test_user: User
):
    response = client.post(
        "/api/v1/checkout",
        json={"item_type": "book", "item_id": 1},
        headers={"Authorization": f"Bearer {test_user.token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["item_type"] == "book"
    assert data["item_id"] == 1

def test_return_item(
    client: TestClient, db: Session, test_checkout: Checkout
):
    response = client.post(
        f"/api/v1/return/{test_checkout.id}",
        headers={"Authorization": f"Bearer {test_checkout.user.token}"}
    )
    assert response.status_code == 200
    db.refresh(test_checkout)
    assert test_checkout.return_date == date.today()

def test_get_item_history(
    client: TestClient, db: Session
):
    response = client.get("/api/v1/history/item/book/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_user_history(
    client: TestClient, db: Session, test_user: User
):
    response = client.get(
        "/api/v1/history/me",
        headers={"Authorization": f"Bearer {test_user.token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert all(checkout["user_id"] == test_user.id for checkout in data)