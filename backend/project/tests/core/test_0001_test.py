from app.config import settings
from app.crud.mongodb.mongo_crud import delete_api_call_logs


async def test_api_call_log_limit(client):
    delete_api_call_logs()
    for i in range(100):
        response = client.get(f"{settings.URL_PREFIX}/test/api-call-log-limit")
        if i == 9:
            assert response.status_code == 200
        if i == 11:
            assert response.status_code == 403
