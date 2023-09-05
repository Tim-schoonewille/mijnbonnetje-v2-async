from functools import wraps
from uuid import UUID

from fastapi import Request

# from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore

from app import models
from app.config import settings
from app.mongodb import database as mongo_db


def log_traffic():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            if settings.TRAFFIC_LOGGING:
                user = kwargs.get("user")
                traffic_log_create_schema = create_traffic_log_object(request, user)
                collection = mongo_db[settings.API_TRAFFIC_COLLECTION]
                await collection.insert_one(traffic_log_create_schema.model_dump())
            result = await func(*args, **kwargs)
            return result

        return wrapper

    return decorator


def create_traffic_log_object(request: Request, user) -> models.TrafficLogCreate:
    path = request.scope.get("path")
    client = request.scope.get("client")
    server = request.scope.get("server")
    method = request.scope.get("method")
    path_params = request.scope.get("path_params")
    type_ = request.scope.get("type")
    http_version = request.scope.get("http_version")

    query_string = request.scope.get("query_string")
    if query_string:
        query_string = query_string.decode("utf-8")
    if user:
        user_id = user.id
        if isinstance(user_id, UUID):
            user_id = str(user_id)
    else:
        user_id = None
    query_parameters = convert_query_params_to_dict(query_string)

    traffic_log_data = {
        "path": path,
        "client": client,
        "server": server,
        "method": method,
        "path_params": path_params,
        "type_": type_,
        "http_version": http_version,
        "user_id": str(user_id),
        "query_parameters": query_parameters,
    }
    schema = models.TrafficLogCreate(**traffic_log_data)  # type: ignore
    return schema


def convert_query_params_to_dict(query_parameters: str) -> dict[str, str] | None:
    if not query_parameters:
        return None

    param_dict = {
        key: value
        for param in query_parameters.split("&")
        if (key_value := param.split("=")) and len(key_value) == 2
        for key, value in [key_value]
    }
    return param_dict


# async def get_api_traffic(mongodb: AsyncIOMotorClient):
#     collection = mongodb[settings.API_TRAFFIC_COLLECTION]
