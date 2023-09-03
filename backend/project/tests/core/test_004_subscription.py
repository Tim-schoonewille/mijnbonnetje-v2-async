from datetime import date
from datetime import timedelta

from app import models
from app.db import create_test_tables

tier = models.TierCreate(
    name="ProTierSubscription",
    price=1000,
    duration=1,
    description="Tier when running pytest from subscription",
    api_call_limit=20,
)

today = date.today().strftime("%Y-%m-%d")


def test_create_and_get_subscription(client):
    create_test_tables(drop=True)
    new_tier_response = client.post("/sub/tier", json={**tier.model_dump()})
    new_tier_id = new_tier_response.json()["id"]
    new_subscription = client.post(
        "sub/subscription", json={"tier_id": new_tier_id, "start_date": today}
    )
    assert new_subscription.status_code == 201

    subscription = client.get(f'/sub/subscription/{new_subscription.json()["id"]}')
    assert subscription.status_code == 200
    assert new_subscription.json() == subscription.json()


def test_read_subscriptions(client):
    subscriptions = client.get("/sub/subscription")
    data = subscriptions.json()
    print(data)
    assert subscriptions.status_code == 200
    assert len(data) > 0
    assert data["subscriptions"]


def test_read_specific_subscription(client):
    response = client.get("/sub/subscription/1")
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert data["active"] is False


async def test_new_subscription_while_pending_payment(client):
    response = client.post(
        "/sub/subscription", json={"tier_id": 1, "start_date": today}
    )
    data = response.json()
    assert response.status_code == 402
    assert data["detail"] == "PAYMENT_PENDING_FOR_SUB"


def test_update_subscription(client):
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    response = client.patch(
        "/sub/subscription/1", json={"start_date": tomorrow, "active": True}
    )
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert data["startDate"] == tomorrow
    assert data["active"] is True


async def test_new_sub_while_actively_subbed(client):
    response = client.post(
        "/sub/subscription", json={"tier_id": 1, "start_date": today}
    )
    data = response.json()
    assert response.status_code == 409
    assert data["detail"] == "ALREADY_SUBBED"


def test_delete_subscription(client):
    response = client.delete("/sub/subscription/1")
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Subscription deleted"

    response = client.get("/sub/subscription/1")
    assert response.status_code == 404


def test_404_subscription(client):
    response = client.get("/sub/subscription/9999")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "SUBSCRIPTION_NOT_FOUND"
