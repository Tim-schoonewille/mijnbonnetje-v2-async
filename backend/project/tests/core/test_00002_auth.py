from app import models
from app.models import UserCreate
from app.utilities.core.auth import verify_password_hash
from app.utilities.core.token import create_email_verification_token
from app.utilities.core.token import extract_payload

mock_user = UserCreate(email="tim.schoonewille@gmail.com", password="!testTEST69")


def test_auth_signup(client):
    response = client.post("/auth/signup", json={**mock_user.model_dump()})
    data = response.json()
    assert response.status_code == 201
    assert data["email"] == mock_user.email
    assert data["id"] == 1

    response = client.post("/auth/signup", json={**mock_user.model_dump()})
    assert response.status_code == 400
    assert response.json()["detail"] == "DUPLICATE_EMAIL"

    email_verification_token = create_email_verification_token(data["email"])
    response = client.get(
        "/auth/email/verify/", params={"token": email_verification_token}
    )
    assert response.status_code == 200


def test_auth_signin_invalid_email(client):
    response = client.post(
        "/auth/signup", json={"email": "no-email-addres.com", "password": "password"}
    )
    assert response.status_code == 422


def test_auth_login_success(client):
    response = client.post("auth/login", json={**mock_user.model_dump()})
    data = response.json()
    assert response.status_code == 200
    assert data["access_token"]
    assert data["refresh_token"]


def test_auth_login_failure(client):
    response = client.post(
        "auth/login", json={"email": "asdfsaf@gaymail.com", "password": "asdfasdfsaf"}
    )
    data = response.json()
    assert response.status_code == 400
    assert data["detail"] == "INVALID_CREDENTIALS"


def test_auth_login_invalid_fields(client):
    response = client.post("/auth/login", json={"asdfaf": "asdfsaf"})
    assert response.status_code == 422


def test_verify_token(client):
    response = client.get("auth/verify-token/")
    assert response.status_code == 200


async def test_request_new_password(client):
    invalid_email = "invalid@emailaddress.uk"
    response = client.post("auth/password/reset", json={"email": invalid_email})
    assert response.status_code == 404
    assert response.json() == {"detail": "INVALID_EMAIL"}

    get_user_response = client.get("sudo/user/1")
    user = get_user_response.json()
    assert get_user_response.status_code == 200

    response = client.post("auth/password/reset", json={"email": user["email"]})
    assert response.status_code == 200
    token = response.json()["token"]
    assert token is not None
    token_payload = extract_payload(models.Token(jwt=token))
    assert token_payload["sub"] == str(user["id"])

    # verify
    new_password = "random_ass_password"
    response = client.post(
        "auth/password/reset/verify",
        json={"new_password": new_password},
        params={"token": token},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated!"

    updated_user = client.get("sudo/user/1").json()
    updated_user_password = updated_user["password"]
    assert verify_password_hash(new_password, updated_user_password)


# This needs to be at the end
# This locks out the user for 5 minutes
# def test_max_login_attempts(client):
#     for i in range(6):
#         response = client.post(
#             'auth/login',
#             json={
#                 'email': mock_user.email,
#                 'password': 'SDFKj24lvl23'
#             }
#         )
#         if i == 1:
#             assert response.status_code == 400
#         if i == 5:
#             print(response.json())
#             assert response.status_code == 401
