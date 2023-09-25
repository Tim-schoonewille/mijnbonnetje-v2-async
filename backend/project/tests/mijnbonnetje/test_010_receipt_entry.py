from app import models
from app.db import create_test_tables
from app.mongodb import drop_test_mongodb_database

dummy_receipt_entry = models.ReceiptEntryCreate(
    total_amount=69,
    warranty=30,
    category=models.Categories.ELECTRONICS,
)


async def test_create_receipt_entries(client):
    await drop_test_mongodb_database()
    create_test_tables(drop=True)
    input_schema = dummy_receipt_entry
    response = client.post("/receipt-entry/", json={**input_schema.model_dump()})
    data = response.json()
    print(data)
    assert response.status_code == 201
    assert data["purchaseDate"] == input_schema.purchase_date
    assert data["totalAmount"] == input_schema.total_amount
    assert data["warranty"] == input_schema.warranty
    assert data["category"] == input_schema.category


def test_read_multiple_receipt_entries(client):
    response = client.get("/receipt-entry")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0


def test_read_specific_receipt_entry(client):
    response = client.get("/receipt-entry/1")
    data = response.json()
    assert response.status_code == 200
    assert data["createdAt"] is not None
    assert data["updatedAt"] is None
    assert data["purchaseDate"] == dummy_receipt_entry.purchase_date
    assert data["totalAmount"] == dummy_receipt_entry.total_amount
    assert data["warranty"] == dummy_receipt_entry.warranty
    assert data["category"] == dummy_receipt_entry.category


def test_update_specific_receipt_entry(client):
    update_schema = models.ReceiptEntryUpdate(category=models.Categories.CLOTHING)
    response = client.patch(
        "receipt-entry/1", json={**update_schema.model_dump(exclude_unset=True)}
    )
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert data["updatedAt"] is not None
    assert data["category"] == models.Categories.CLOTHING


def test_delete_receipt_entry(client):
    response = client.delete("/receipt-entry/1")
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "RECEIPT_ENTRY_DELETED"

    response = client.get("/receipt-entry/1")
    assert response.status_code == 404
