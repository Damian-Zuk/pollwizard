import time
import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")
ACCESS_TOKEN_EXPIRY = config("access_token_time", default=600, cast=int)
REFRESH_TOKEN_EXPIRY = config("refresh_token_time", default=86400, cast=int)


def generate_token(token_type: str, user_email: str, token_expiry: int):
    payload = {
        "user_email": user_email,
        "token_type": token_type,
        "expiry": time.time() + token_expiry
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def generate_access_token(user_email: str):
    return generate_token("access", user_email, ACCESS_TOKEN_EXPIRY)


def generate_refresh_token(user_email: str):
    return generate_token("refresh", user_email, REFRESH_TOKEN_EXPIRY)


def signJWT(user_email: str):
    return {
        "access_token": generate_access_token(user_email),
        "refresh_token": generate_refresh_token(user_email)
    }


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decode_token if decode_token['expiry'] >= time.time() else None
    except:
        return {}
