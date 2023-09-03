from uuid import uuid4

from app.db import create_test_tables

from .test_003_tier import tier
from .test_004_subscription import today


async def test_read_all_payments(client):
    create_test_tables(drop=True)
    tier_db_id = client.post("/sub/tier", json={**tier.model_dump()}).json()["id"]
    subscription_db = client.post(
        "/sub/subscription", json={"tier_id": tier_db_id, "start_date": today}
    )
    assert subscription_db.status_code == 201

    response = client.get("/sub/payment")
    data = response.json()
    assert response.status_code == 200
    assert len(data) > 0


def test_read_1_payment(client):
    response = client.get("/sub/payment/1")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == 1
    assert data["status"] == "pending"


async def test_payment_pending(client):
    response = client.get("/sub/payment/pending")
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert isinstance(data, dict)


def test_attempt_new_payment_while_pending(client):
    response = client.post("/sub/payment", json={"subscription_id": 1})
    data = response.json()
    assert response.status_code == 402
    assert data["detail"] == "PAYMENT_PENDING"


def test_update_payment_wrong_external_id(client):
    response = client.post(
        "/sub/payment/update",
        params={"external_id": uuid4()},
        json={"method": "ideal", "status": "completed"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "INVALID_PAYMENT_ID"


def test_update_failed_payment(client):
    external_id = client.get("/sub/payment").json()[-1]["externalId"]
    response = client.post(
        "/sub/payment/update",
        params={"external_id": external_id},
        json={"method": "ideal", "status": "failed"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["status"] == "failed"
    assert data["method"] == "ideal"


def test_create_new_payment(client):
    response = client.post("/sub/payment", json={"subscription_id": 1})
    data = response.json()
    assert response.status_code == 201
    assert data["id"] != 1


def test_update_payment(client):
    external_id = client.get("/sub/payment").json()[-1]["externalId"]
    response = client.post(
        "/sub/payment/update",
        params={"external_id": external_id},
        json={"method": "ideal", "status": "completed"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["status"] == "completed"
    assert data["method"] == "ideal"
