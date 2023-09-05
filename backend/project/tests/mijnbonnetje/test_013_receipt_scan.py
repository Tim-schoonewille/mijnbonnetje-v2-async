import shutil


from app import models
from app.db import create_test_tables

dummy_receipt_scan = models.ReceiptScanCreate(
    receipt_entry_id=1, receipt_file_id=1, scan="lalalalalalal"
)


test_receipt_file_path = "./tests/files/test_receipt.jpg"


def test_create_receipt_file_for_scan(client):
    create_test_tables(drop=True)
    folder_to_delete = "./public-test/1"
    shutil.rmtree(folder_to_delete)
    receipt_entry_schema = models.ReceiptEntryCreate(total_amount=69)
    response = client.post(
        "/receipt-entry", json={**receipt_entry_schema.model_dump(exclude_unset=True)}
    )
    assert response.status_code == 201

    response = client.post(
        "/receipt-file/",
        files={"file": open(test_receipt_file_path, "rb")},
        params={"entry_id": 1},
    )
    data = response.json()
    assert response.status_code == 201
    assert data["fileName"] == "test_receipt.jpg"
    assert data["fileType"] == "image/jpeg"
    assert data["fileSize"] == 186030


def test_create_receipt_scan(client):
    response = client.post("/receipt-scan/", params={"receipt_file_id": 1})
    data = response.json()
    print(data)
    assert response.status_code == 201
    assert data["createdAt"] is not None
    assert data["updatedAt"] is None
    assert data['receiptEntryId'] == 1
    assert data["receiptFileId"] == dummy_receipt_scan.receipt_file_id


def test_read_multiple_receipt_scans(client):
    response = client.get("/receipt-scan")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0


def test_read_specific_receipt_scan(client):
    response = client.get("/receipt-scan/1")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == 1
    assert data["receiptFileId"] == 1
    assert data["createdAt"] is not None
    assert data["updatedAt"] is None
    assert isinstance(data["scan"], str)


def test_delete_specific_receipt_scan(client):
    response = client.delete("/receipt-scan/1")
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "RECEIPT_SCAN_REMOVED"
