import json
import shutil
from datetime import datetime

from app import models
from app.db import create_test_tables

test_receipt_file_path = "./tests/files/triade-bon.jpg"
test_receipt_data = './data/triade_bon.json'
mock_store_aldi = models.StoreCreate(name="Aldi", city="Brunssum", country="NL")


dummy_product_item = models.ProductItemCreate(
    receipt_entry_id=1,
    purchase_date=str(datetime.utcnow().date()),
    name="Klopboor",
    price=69.69,
)


def test_create_full_receipt_without_product_items(client):
    create_test_tables(drop=True)
    folder_to_delete = "./public-test/1"
    shutil.rmtree(folder_to_delete)

    store_create = client.post("/store", json={**mock_store_aldi.model_dump()})
    assert store_create.status_code == 201

    full_receipt = client.post(
        "/receipt",
        files={"file": open(test_receipt_file_path, "rb")},
        params={"include_external_ocr": False},
    )
    data = full_receipt.json()
    assert full_receipt.status_code == 201
    receipt_file = data["receiptFiles"][0]
    receipt_scan = data["receiptScans"][0]
    assert data["id"] == 1
    assert receipt_file["id"] == 1
    assert receipt_scan["id"] == 1

    with open(test_receipt_data, 'r') as f:
        receipt_data = json.load(f)
    receipt = receipt_data['receipts'][0]
    store_name = receipt['merchant_name']
    total_amount = receipt['total']
    product_items = receipt['items']
    assert data['store']['name'] == store_name
    assert data['totalAmount'] == int(total_amount*100)
    assert len(product_items) == 10


def test_read_multiple_receipts(client):
    second_receipt = client.post(
        "/receipt",
        files={"file": open(test_receipt_file_path, "rb")},
        params={"exclude_ai_scan": True},
    )
    assert second_receipt.status_code == 201

    response = client.get("/receipt")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 2


def test_read_specific_receipt(client):
    response = client.get('/receipt/1')
    data = response.json()
    receipt_file = data['receiptFiles'][0]
    receipt_scan = data['receiptScans'][0]
    assert response.status_code == 200
    assert data['createdAt'] is not None
    assert receipt_file['id'] == 1
    assert receipt_file['receiptEntryId'] == 1
    assert receipt_file['fileName'] == 'triade-bon.jpg'
    assert receipt_file['fileType'] == 'image/jpeg'
    assert receipt_file['fileSize'] == 2225572
    assert receipt_scan['id'] == 1
    assert isinstance(receipt_scan['scan'], str)


def test_delete_specific_receipt(client):
    response = client.delete('/receipt/1')
    data = response.json()
    assert response.status_code == 200
    assert data['message'] == "RECEIPT_DELETED"