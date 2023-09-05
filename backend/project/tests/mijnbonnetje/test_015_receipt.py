import shutil
from datetime import datetime

from app import models
from app.db import create_test_tables

test_receipt_file_path = "./tests/files/test_receipt.jpg"

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

    store_create = client.post('/store', json={**mock_store_aldi.model_dump()})
    assert store_create.status_code == 201

    full_receipt = client.post(
        '/receipt',
        files={'file': open(test_receipt_file_path, 'rb')},
        params={'exclude_ai_scan': True}
    )
    data = full_receipt.json()
    print(data)
    assert full_receipt.status_code == 201
    receipt_entry = data['receiptEntry']
    receipt_file = data['receiptFiles'][0]
    receipt_scan = data['receiptScans'][0]
    assert receipt_entry['id'] == 1
    assert receipt_file['id'] == 1
    assert receipt_scan['id'] == 1
