import uuid
from datetime import datetime

from app.config import settings
from app.crud.mongodb.mongo_crud import delete_api_call_logs


def compare_date_from_string_to_today(date_str: str) -> bool:
    datetime_object = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
    today = datetime.utcnow().date()
    print(today)
    print(datetime_object.date())
    return today == datetime_object.date()


def is_valid_uuid(uuid_string: str) -> bool:
    try:
        uuid_obj = uuid.UUID(uuid_string)
        return str(uuid_obj) == uuid_string
    except ValueError:
        return False


def test_login_records(client):
    response = client.get("/sudo/login-records")
    data = response.json()[0]
    assert response.status_code == 200
    assert data
    assert data["createdAt"]
    assert data["updatedAt"] is None
    assert data["userId"] == 1
    assert data["id"] == 1
    assert data["ipAddress"] == "testclient"
    assert data["fresh"] is True


def test_read_refresh_tokens(client):
    response = client.get("/sudo/refresh-tokens")
    data = response.json()[0]
    print(data)
    createdAt, userId, jti = data["createdAt"], data["userId"], data["jti"]
    assert response.status_code == 200
    assert compare_date_from_string_to_today(createdAt)
    assert userId == 1
    assert is_valid_uuid(jti)


def test_revoke_refresh_tokens(client):
    new_login = client.post(
        "/auth/login",
        json={"email": "tim.schoonewille@gmail.com", "password": "random_ass_password"},
    )
    print(new_login.json())
    assert new_login.status_code == 200

    response = client.get("/sudo/refresh-tokens")
    assert response.json()[1]["consumed"] is False

    response = client.post("/sudo/refresh-token/revoke", params={"user_id": 1})
    assert response.status_code == 200
    assert response.json()["succes"] == "Tokens revoked."

    response = client.get("/sudo/refresh-tokens")
    assert response.json()[1]["consumed"] is True


def test_update_sudo(client):
    actions = [
        {"action": "revoke", "response_boolean": False},
        {"action": "assign", "response_boolean": True},
    ]

    for action_info in actions:
        action = action_info["action"]
        response_boolean = action_info["response_boolean"]

        response = client.patch("/sudo/user/update-sudo/1", params={"action": action})
        assert response.status_code == 200

        response = client.get("/sudo/user/1")
        assert response.json()["sudo"] is response_boolean


def test_update_active_status(client):
    actions = [
        {"action": "disable", "response_boolean": False},
        {"action": "enable", "response_boolean": True},
    ]

    for action in actions:
        response = client.patch(
            "/sudo/user/active/1", params={"action": action["action"]}
        )
        assert response.status_code == 200

        response = client.get("/sudo/user/1")
        print(response.json())
        assert response.status_code == 200
        assert response.json()["active"] is action["response_boolean"]


def test_sudo_read_all_users(client):
    response = client.get("/sudo/user")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["id"] == 1
    assert compare_date_from_string_to_today(data[0]["createdAt"]) is True


def test_sudo_read_specific_user(client):
    response = client.get("/sudo/user/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert compare_date_from_string_to_today(data["createdAt"]) is True


def test_sudo_read_user_wrong_parameter(client):
    response = client.get("/sudo/user/abcdefgh")
    print(response.json())
    expected_output = {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["path", "user_id", "int"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",  # noqa
                "input": "abcdefgh",
                "url": "https://errors.pydantic.dev/2.0.3/v/int_parsing",
            },
            {
                "type": "is_instance_of",
                "loc": [
                    "path",
                    "user_id",
                    "lax-or-strict[lax=json-or-python[json=function-after[uuid_validator(), union[str,bytes]],python=union[is-instance[UUID],function-after[uuid_validator(), union[str,bytes]]]],strict=json-or-python[json=function-after[uuid_validator(), union[str,bytes]],python=is-instance[UUID]]]",  # noqa
                    "is-instance[UUID]",
                ],  # noqa
                "msg": "Input should be an instance of UUID",
                "input": "abcdefgh",
                "ctx": {"class": "UUID"},
                "url": "https://errors.pydantic.dev/2.0.3/v/is_instance_of",
            },
            {
                "type": "uuid_parsing",
                "loc": [
                    "path",
                    "user_id",
                    "lax-or-strict[lax=json-or-python[json=function-after[uuid_validator(), union[str,bytes]],python=union[is-instance[UUID],function-after[uuid_validator(), union[str,bytes]]]],strict=json-or-python[json=function-after[uuid_validator(), union[str,bytes]],python=is-instance[UUID]]]",  # noqa
                    "function-after[uuid_validator(), union[str,bytes]]",
                ],  # noqa
                "msg": "Input should be a valid UUID, unable to parse string as an UUID",  # noqa
                "input": "abcdefgh",
            },
        ]
    }
    assert response.status_code == 422
    assert response.json() == expected_output


def test_sudo_read_user_invalid_user_id(client):
    response = client.get("/sudo/user/9999")
    print(response.json())
    assert response.status_code == 404
    assert response.json()["detail"] == "USER_NOT_FOUND"


def test_sudo_user_api_call_logs(client):
    response = client.get("/sudo/user-api-call-log")
    data = response.json()[0]
    print(data["apicalls"])
    assert response.status_code == 200
    assert data["userId"] == 1
    assert data["apicalls"][0]["date"] == str(datetime.utcnow().date())
    assert data["apicalls"][0]["amount"] == 9


def test_sudo_user_api_call_log(client):
    response = client.get("/sudo/user-api-call-log/1")
    data = response.json()
    assert response.status_code == 200
    assert data["userId"] == 1
    assert data["apicalls"][0]["date"] == str(datetime.utcnow().date())
    assert data["apicalls"][0]["amount"] == 9


def test_sudo_user_api_call_log_no_log(client):
    response = client.get("/sudo/user-api-call-log/99999")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "LOGS_NOT_FOUND"


async def test_api_call_log_limit(client):
    delete_api_call_logs()
    for i in range(100):
        response = client.get(f"{settings.URL_PREFIX}/test/api-call-log-limit")
        if i == 3:
            assert response.status_code == 200
        if i == 11:
            assert response.status_code == 403
