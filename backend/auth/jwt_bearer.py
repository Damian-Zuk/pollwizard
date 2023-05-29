from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .jwt_handler import decodeJWT


class JWTBearer(HTTPBearer):
    
    def __init__(self, auto_error: bool = True, token_type: str = "access"):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.token_type = token_type


    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(self.token_type, credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")


    def verify_jwt(self, token_type: str, jwtoken: str) -> bool:
        is_token_valid = False
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload and payload["token_type"] == token_type:
            is_token_valid = True

        return is_token_valid
