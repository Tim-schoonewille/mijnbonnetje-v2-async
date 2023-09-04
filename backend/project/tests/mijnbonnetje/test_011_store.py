from app import models
from app.db import create_test_tables


mock_store_aldi = models.StoreCreate(name="Aldi", city="Brunssum", country="NL")
mock_store_albertheijn = models.StoreCreate(name="Albert Heijn", city="Brunssum")
mock_receipt_entry = models.ReceiptEntryCreate(store_id=1, total_amount=30)


def test_create_store(client):
    create_test_tables(drop=True)
    response = client.post("/store", json={**mock_store_aldi.model_dump()})
    data = response.json()
    print(data)
    assert response.status_code == 201
    assert data["name"] == "Aldi"
    assert data["city"] == mock_store_aldi.city
    assert data["country"] == mock_store_aldi.country

    response = client.post("/store", json={**mock_store_albertheijn.model_dump()})
    assert response.status_code == 201


def test_search_store_with_one_letter(client):
    response = client.get("/store/search", params={"q": "A"})
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 2


def test_search_specific_store(client):
    response = client.get("/store/search", params={"q": "Ald"})
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    store = data[0]
    assert store["name"] == "Aldi"


def test_read_single_store(client):
    response = client.get("/store/1")
    data = response.json()
    assert response.status_code == 200
    assert data["createdAt"]
    assert data["updatedAt"] is None
    assert data["name"] == mock_store_aldi.name
    assert data["city"] == mock_store_aldi.city
    assert data["country"] == mock_store_aldi.country


def test_multi_read_store(client):
    response = client.get("/store")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) >= 2


def test_update_store(client):
    store_update_schema = models.StoreUpdate(country="NL")
    response = client.patch(
        "/store/2", json={**store_update_schema.model_dump(exclude_unset=True)}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["updatedAt"] is not None
    assert data["country"] == store_update_schema.country


# def test_add_receiptentry_with_store(client):
#     response = client.post('/receipt-entry', json={**mock_receipt_entry.model_dump()})
#     data = response.json()
#     assert response.status_code == 201
#     assert data['storeId'] == mock_receipt_entry.store_id


# def test_stores_in_user_model(client):
#     response = client.get('/store/user')
#     data = response.json()
#     print(data)
#     assert response.status_code == 200
#     assert isinstance(data, list)
#     assert len(data) == 1


def test_delete_store(client):
    response = client.delete("/store/1")
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "STORE_DELETED"

    response = client.get("/store/1")
    assert response.status_code == 404
