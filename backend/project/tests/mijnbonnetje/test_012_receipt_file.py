from app import models
from app.db import create_test_tables

test_receipt_file_path = './tests/files/test_receipt.jpg'


def test_create_receipt_file(client):
    create_test_tables(drop=True)
    receipt_entry_schema = models.ReceiptEntryCreate(total_amount=69)
    response = client.post('/receipt-entry', json={**receipt_entry_schema.model_dump(exclude_unset=True)})
    assert response.status_code == 201
    response = client.post(
        '/receipt-file/',
        files={'file': open(test_receipt_file_path, 'rb')},
        params={'entry_id': 1})
    assert response.status_code == 200
