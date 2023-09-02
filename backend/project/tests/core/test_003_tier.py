from datetime import date, datetime

from app import models

tier = models.TierCreate(
    name='TestTier',
    price=1000,
    duration=1,
    description='Tier when running pytest',
    api_call_limit=69,
)

subscription_create_schema = models.SubscriptionCreateSchema(  # type: ignore
    start_date=date.today(), tier_id=1
)


def test_create_tier(client):
    response = client.post('/sub/tier', json={**tier.model_dump()})
    data = response.json()
    assert response.status_code == 201
    data_from_db = models.TierCreate(**data)
    assert data_from_db == tier
    assert data['id']
    created_at_date_obj = datetime.fromisoformat(data['createdAt']).date()
    assert created_at_date_obj == date.today()


def test_read_tiers(client):
    response = client.get('/sub/tier')
    data = response.json()
    assert response.status_code == 200
    assert len(data) > 0

    first_tier = data[0]
    response = client.get(f'/sub/tier/{first_tier["id"]}')
    assert response.status_code == 200
    print(data)
    print(response.json())
    assert first_tier == response.json()


def test_update_tier(client):
    response = client.get('/sub/tier/1')
    print(response.json())
    old_tier = response.json()
    updated_tier = models.TierUpdate(**tier.model_dump())
    tier_name_update = 'Updated Tier'
    updated_tier.name = 'Updated Tier'
    response = client.patch('/sub/tier/1', json=updated_tier.model_dump())
    updated_tier_db = response.json()
    assert response.status_code == 200
    assert updated_tier_db['name'] == tier_name_update
    assert old_tier != updated_tier_db


def test_404_read_tier(client):
    response = client.get('/sub/tier/9999999')
    assert response.status_code == 404


def test_delete_tier(client):
    response = client.delete('/sub/tier/1')
    assert response.status_code == 200
    assert response.json()['message'] == 'Tier deleted'
    resposne = client.get('/sub/tier/1')
    assert resposne.status_code == 404
