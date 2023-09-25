import os
import shutil

from app import models
from app.db import create_test_tables

test_receipt_file_path = "./tests/files/test_receipt.jpg"


def test_create_receipt_file(client):
    create_test_tables(drop=True)
    folder_to_delete = "./public-test/1"
    try:
        shutil.rmtree(folder_to_delete)
    except FileNotFoundError:
        pass
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


def test_read_receipt_file(client):
    response = client.get("/receipt-file/1")
    data = response.json()
    entry_id = data["receiptEntryId"]
    file_name = data["fileName"]
    file_path = str(data["filePath"])
    assert response.status_code == 200
    assert data["createdAt"] is not None
    assert data["updatedAt"] is None
    assert data["userId"] == 10
    assert entry_id == 1
    assert file_name == "test_receipt.jpg"
    assert data["fileType"] == "image/jpeg"
    assert data["fileSize"] == 186030
    assert file_path.startswith(f"./public-test/{entry_id}/")
    assert file_path.endswith(file_name)


def test_read_multiple_files(client):
    response = client.get("/receipt-file/")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0


def test_delete_receipt_file(client):
    receipt_file_on_disk = client.get("/receipt-file/1").json()["filePath"]
    assert os.path.exists(receipt_file_on_disk)
    response = client.delete("receipt-file/1")
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "RECEIPT_FILE_DELETED"
    assert os.path.exists(receipt_file_on_disk) is False
