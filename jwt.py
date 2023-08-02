# authentication logic
# ----------------------------------------------------------------------
from base64 import b64encode, b64decode
import hmac
import json
from hashlib import sha256
from typing import Callable
from datetime import timedelta, datetime
from functools import wraps
from fastapi import HTTPException, Request

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_SECRET_KEY = "secret"
JWT_ALGORITHM = "HS256"

def create_access_token(data: dict):
    """
    Create access token
    :param data: data to be encoded
    :return: access token
    """
    header = {
        "alg": JWT_ALGORITHM,
        "typ": "JWT",
            }
    data["exp"] = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    encoded_header = b64encode(json.dumps(header).encode("utf-8")).decode("utf-8")
    encoded_payload = b64encode(json.dumps(data).encode("utf-8")).decode("utf-8")
    to_sign = f"{encoded_header}.{encoded_payload}".encode("utf-8")
    signature = hmac.new(JWT_SECRET_KEY.encode("utf-8"), to_sign, sha256).hexdigest()
    token = f"{encoded_header}.{encoded_payload}.{signature}"

    return token

def verify_token(token: str, **payload: datetime) -> bool:
    encoded_header, encoded_payload, received_signature = token.split(".")

    to_sign = f"{encoded_header}.{encoded_payload}".encode("utf-8")
    expected_signature = hmac.new(JWT_SECRET_KEY.encode("utf-8"), to_sign, sha256).hexdigest()

    if received_signature != expected_signature:
        raise Exception("Invalid token")

    payload = json.loads(b64decode(encoded_payload).decode("utf-8"))

    if payload["exp"] < datetime.utcnow():
        raise Exception("Token expired")
    return True

def require_auth(func: Callable) -> Callable:
    """
    Decorator to require authentication
    :param func: function to be decorated
    :return: decorated function
    """
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        if "Authorization" not in request.headers:
            raise HTTPException(status_code=401, detail="Not authenticated")
        token = request.headers["Authorization"].split(" ")[1]
        if not verify_token(token):
            raise HTTPException(status_code=401, detail="Not authenticated")
        return await func(request, *args, **kwargs)
    return wrapper
