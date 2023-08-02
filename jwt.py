# authentication logic
# ----------------------------------------------------------------------
from base64 import b64encode, urlsafe_b64encode, urlsafe_b64decode
import hmac
import json
import time
from hashlib import sha256
from typing import Callable, Optional
from datetime import timedelta
from functools import wraps
from fastapi import HTTPException, Request

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_SECRET_KEY = "secret"
JWT_ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create access token
    :param data: data to be encoded
    :param expires_delta: expiration time
    :return: access token
    """
    header = {
        "alg": JWT_ALGORITHM,
        "typ": "JWT",
            }
    data["exp"] = time.time() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES).total_seconds()

    encoded_header = b64encode(json.dumps(header).encode("utf-8")).decode("utf-8")
    encoded_payload = b64encode(json.dumps(data).encode("utf-8")).decode("utf-8")
    to_sign = f"{encoded_header}.{encoded_payload}".encode("utf-8")
    signature = hmac.new(JWT_SECRET_KEY.encode("utf-8"), to_sign, sha256).hexdigest()
    token = f"{encoded_header}.{encoded_payload}.{signature}"

    return token

def verify_token(token: str):
    encoded_header, encoded_payload, signature = token.split(".")

    to_sign = f"{encoded_header}.{encoded_payload}".encode("utf-8")
    signature_check = hmac.new(JWT_SECRET_KEY.encode("utf-8"), to_sign, sha256).hexdigest()
    expected_signature = urlsafe_b64encode(signature_check.encode("utf-8")).decode("utf-8").rstrip("=")

    if signature != expected_signature:
        raise Exception("Invalid token")

    payload = json.loads(urlsafe_b64decode(encoded_payload + "==="))

    if time.time() > payload["exp"]:
        raise Exception("Token expired")
    return payload

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
