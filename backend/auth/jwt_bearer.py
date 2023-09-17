import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError
from decouple import config
from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


JWT_SECRET = config("jwt_secret")
JWT_ALGORITHM = config("jwt_algorithm")
JWT_ACCESS_EXP = config("jwt_access_token_time", cast=int)
JWT_REFRESH_EXP = config("jwt_refresh_token_time", cast=int)


def generate_token(token_type: str, user_email: str, token_expiry: int):
    payload = {
        "user_email": user_email,
        "token_type": token_type,
        "exp": datetime.utcnow() + timedelta(seconds=token_expiry),
        "nbf": datetime.utcnow(),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def generate_access_token(user_email: str):
    return generate_token("access", user_email, JWT_ACCESS_EXP)


def generate_refresh_token(user_email: str):
    return generate_token("refresh", user_email, JWT_REFRESH_EXP)


def signJWT(user_email: str):
    return {
        "access_token": generate_access_token(user_email),
        "refresh_token": generate_refresh_token(user_email)
    }


def decodeJWT(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
    except (DecodeError, ExpiredSignatureError, InvalidTokenError):
        raise HTTPException(status_code=401, detail="Authentication failed: Invalid bearer token.")


class JWTBearer(HTTPBearer):
    
    def __init__(self, auto_error: bool = True, token_type: str = "access"):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.token_type = token_type


    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)     
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Invalid authorization code.")
        if not credentials.scheme == "Bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
        
        payload = decodeJWT(credentials.credentials)
        if not payload or payload.get("token_type") != self.token_type:
            raise HTTPException(status_code=401, detail="Authentication failed: Invalid bearer token.")
        
        return credentials.credentials
