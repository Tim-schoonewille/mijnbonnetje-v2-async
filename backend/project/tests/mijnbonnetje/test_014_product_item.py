from datetime import datetime

from app import models
from app.db import create_test_tables

dummy_product_item = models.ProductItemCreate(
    receipt_entry_id=1,
    purchase_date=str(datetime.utcnow().date()),
    name="Klopboor",
    price=69.69,
)


def test_create_product_item(client):
    create_test_tables(drop=True)

    receipt_entry_schema = models.ReceiptEntryCreate(total_amount=69)
    response = client.post(
        "/receipt-entry", json={**receipt_entry_schema.model_dump(exclude_unset=True)}
    )
    assert response.status_code == 201

    response = client.post("/product-item", json={**dummy_product_item.model_dump()})
    data = response.json()
    assert response.status_code == 201
    assert data["receiptEntryId"] == dummy_product_item.receipt_entry_id
    assert data["purchaseDate"] == dummy_product_item.purchase_date
    assert data["name"] == dummy_product_item.name
    assert data["price"] == dummy_product_item.price
    assert data["quantity"] == 1
    assert data["createdAt"] is not None
    assert data["updatedAt"] is None
    assert data["userId"] == 10


def test_read_multiple_product_items(client):
    response = client.get("/product-item")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0


def test_read_specific_product_item(client):
    response = client.get("/product-item/1")
    data = response.json()
    assert response.status_code == 200
    assert data["receiptEntryId"] == dummy_product_item.receipt_entry_id
    assert data["purchaseDate"] == dummy_product_item.purchase_date
    assert data["name"] == dummy_product_item.name
    assert data["price"] == dummy_product_item.price
    assert data["quantity"] == 1
    assert data["createdAt"] is not None
    assert data["updatedAt"] is None
    assert data["userId"] == 10


def test_update_specific_product_item(client):
    update_schema = models.ProductItemUpdate(name="Stapelkit", quantity=2)
    response = client.patch(
        "/product-item/1", json={**update_schema.model_dump(exclude_unset=True)}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["receiptEntryId"] == dummy_product_item.receipt_entry_id
    assert data["purchaseDate"] == dummy_product_item.purchase_date
    assert data["name"] == update_schema.name
    assert data["price"] == dummy_product_item.price
    assert data["quantity"] == update_schema.quantity
    assert data["createdAt"] is not None
    assert data["updatedAt"] is not None
    assert data["userId"] == 10


def test_delete_specific_product_item(client):
    response = client.delete("/product-item/1")
    assert response.status_code == 200
    assert response.json()["message"] == "PRODUCT_ITEM_DELETED"


def test_404_product_item(client):
    response = client.get("/product-item/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "PRODUCT_ITEM_NOT_FOUND"
