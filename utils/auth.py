import os
from jwt import DecodeError, InvalidSignatureError, decode
from typing import Callable

from flask import jsonify, request


def authorized(f: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        headers = request.headers
        bearer_token = headers.get("Authorization")
        if not bearer_token:
            return jsonify({"message": "Unauthorized"}), 401
        try:
            token = bearer_token.split()[1]
            user_id = int(decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"]).get("user_id"))
            return f(*args, **kwargs, user_id=user_id)
        except InvalidSignatureError as e:
            return jsonify({"message": "Invalid token"}), 419
        except DecodeError as e:
            print('Ошибка расшифровки токена', e)
            return jsonify({"message": "Ошибка расшифровки токена - Not enough segments"}), 419

    return wrapper