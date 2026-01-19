"""
Author: Damian Żuk
License: MIT

FastAPI Extension for secure bearer token management with Redis cache.

Main features:
    1. Generating and refreshing JWT tokens (with refresh token rotation).
    2. Token revocation (invalidation).
    3. Refresh token misuse detection (can be used only once).
    4. `JwtBearer` class to handle authentication in FastAPI routes.

The role of Redis is to store:
    1. Links between access and refresh tokens (for better token revocation).
    2. Refresh token uses (for misuse detection).
    3. Token blacklist (revoked tokens identifiers).

Usage:
    1. Initialize `JwtManager` by calling `configure` class method.
    2. Generate token pairs for users.
    3. Authenticate API calls using the custom `JwtBearer` class.
    4. Handle token refresh and revocation in API endpoints.
"""
import jwt
import redis
import time
import uuid
import logging

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError
from jwt.algorithms import get_default_algorithms
from redis.client import Pipeline
from typing import Optional, Literal, Union, Tuple, List, Dict, Any
from enum import IntEnum


class TokenType(IntEnum):
    ACCESS = 0
    REFRESH = 1


class TokenTypeError(Exception):
    pass


class AuthCredentials:
    """
    Authorization credentials to be included in token payload.

    Attributes:
    - `subject` (`Dict[str, Union[str, int, float]]`): Contains claims about the subject e.g. user_id or username.
    - `token_type` (`TokenType`): Type of the token (`TokenType.ACCESS` or `TokenType.REFRESH`).
    - `exp` (`int`): Token expiration time after which the token must not be accepted. It's a UNIX timestamp.
    - `nbf` (`int`): Token creation time as well as time before which the token must not be accepted. It's a UNIX timestamp.
    - `jti` (`str`): Unique identifier for the JWT (`uuid.uuid4().hex`).

    Note:
        You can use [] operator to get specific value of a key from `subject` dictionary.
    """

    subject: Dict[str, Union[str, int, float]]
    token_type: TokenType 
    exp: int
    nbf: int
    jti: str

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getitem__(self, item: str) -> Union[str, int, float]:
        return self.subject[item]


class JwtManager:
    """
    Utility class for managing JSON Web Tokens (JWT).
    
    Usage:
    - The class must be initialized using `configure` function.
    - Tokens can be generated with `generate_token_pair` and refreshed using `refresh_token_pair`.
    - Use `revoke_token` to invalidate token when user logs out.
    """

    _secret: str
    _algorithm: str
    _access_exp: int
    _refresh_exp: int
    _cache_exp: int
    _redis_conn: redis.Redis
    _redis_conn_pool: redis.ConnectionPool


    @classmethod
    def configure(cls,
            secret: str,
            algorithm: str = "HS256",
            access_expiration: int = 600,
            refresh_expiration: int = 600,
            redis_host: str = "localhost",
            redis_port: int = 6379,
            redis_pass: Optional[str] = None,
            redis_db_index: int = 0,
        ):
        """
        Required parameter: `secret` key for signing JWTs.
        The unit of token expiration time is seconds.
        """
        # Check if algorithm is supported
        jwt_algorithms = list(get_default_algorithms().keys())
        if algorithm not in jwt_algorithms:
            raise NotImplementedError(f"Algorithm not supported. Use: {jwt_algorithms}")

        cls._access_exp = access_expiration
        cls._refresh_exp = refresh_expiration
        cls._algorithm = algorithm
        cls._secret = secret

        cls._redis_conn_pool = redis.ConnectionPool(
            host=redis_host,
            port=redis_port,
            password=redis_pass,
            db=redis_db_index
        )
        cls._redis_conn = redis.Redis(connection_pool=cls._redis_conn_pool)
        cls._cache_exp = refresh_expiration


    @classmethod
    def generate_token_pair(cls, subject: Dict[str, Union[str, int, float]]) -> Dict[Literal["access", "refresh"], str]:
        """
        Generate a pair of JWT tokens (access & refresh) for the specified subject.
        
        :param `subject`: Dictionary containing claims to be included in the token's payload.
            e.g. `{"user_id": 679, "username": "bob", "role": "admin"}.`
        :return: Dictionary containing generated access and refresh tokens.
        """
        # Generate tokens
        access_token, access_jti = cls._encode_token(TokenType.ACCESS, subject)
        refresh_token, refresh_jti = cls._encode_token(TokenType.REFRESH, subject)

        cls._redis_create_token_link(access_jti, refresh_jti)
        cls._redis_create_token_link(refresh_jti, access_jti)

        return {"access": access_token, "refresh": refresh_token}


    @classmethod
    def refresh_token_pair(cls, credentials: AuthCredentials) -> Dict[Literal["access", "refresh"], str]:
        """
        Generate a new token pair using the provided refresh token.
        
        :param `credentials`: Decoded payload of JWT refresh token.
        :return: Dictionary containing new access and refresh tokens.
        :raises: `HTTPException` if the provided token is already used.
        """
        if credentials.token_type != TokenType.REFRESH:
            raise TokenTypeError("Wrong token type. Expected refresh token.")

        refresh_jti, subject = credentials.jti, credentials.subject

        # Check if refresh token has been used already
        if cls._redis_check_refresh_token_reuse(refresh_jti):
            logging.error(f"<JwtManger::refresh_token_pair> Refresh Token Reuse Error! {subject=}")
            cls.revoke_token(credentials)
            raise HTTPException(status_code=401, detail="Invalid bearer token.")

        cls._redis_mark_refresh_token(refresh_jti)

        # Generate new tokens
        new_access_token, new_access_jti = cls._encode_token(TokenType.ACCESS, subject)
        new_refresh_token, new_refresh_jti = cls._encode_token(TokenType.REFRESH, subject)

        cls._redis_create_token_link(new_access_jti, new_refresh_jti, refresh_jti)
        cls._redis_create_token_link(new_refresh_jti, new_access_jti, refresh_jti)
        cls._redis_add_token_link(refresh_jti, new_access_jti, new_refresh_jti)

        return {"access": new_access_token, "refresh": new_refresh_token}


    @classmethod
    def revoke_token(cls, credentials: AuthCredentials):
        """
        Revoke the provided token and all linked tokens.
        
        :param `credentials`: Decoded payload of JWT token.
        """

        def revoke_recursively(jti: str, redis_pipeline: Pipeline, revoked: set[str] = set()):
            tokens_revoked_count = 1
            cls._redis_blacklist_token(jti, redis_pipeline)
            token_links = cls._redis_get_links(jti)
            if token_links:
                to_revoke = set(token_links) - revoked
                revoked.update([jti], to_revoke)
                for jti in to_revoke:
                    tokens_revoked_count += revoke_recursively(jti, redis_pipeline)
            return tokens_revoked_count
        
        # Start token revocation
        redis_pipeline = cls._redis_conn.pipeline()
        tokens_revoked = revoke_recursively(credentials.jti, redis_pipeline)
        redis_pipeline.execute()
        logging.info(f"<JwtManager::revoke_token> {tokens_revoked=} subject={credentials.subject}")


    @classmethod
    def _redis_create_token_link(cls, jti_key: str, *jti_args: str):
        cache_value = ';'.join(jti_args)
        cls._redis_conn.setex(f"link_{jti_key}", cls._cache_exp, cache_value)


    @classmethod
    def _redis_add_token_link(cls, jti_key: str, *jti_args: str):
        current_value = cls._redis_conn.get(f"link_{jti_key}")
        if current_value:
            new_cache_value = f"{current_value.decode('utf-8')};{';'.join(jti_args)}"
        else:
            new_cache_value = ';'.join(jti_args)
            logging.warning(f"<JwtManager::_redis_add_token_link> Missing token link entry. {jti_key=}")
        cls._redis_conn.setex(f"link_{jti_key}", cls._cache_exp, new_cache_value)


    @classmethod
    def _redis_get_links(cls, jti: str) -> Optional[List[str]]:
        token_links = cls._redis_conn.get(f"link_{jti}")
        if token_links:
            return token_links.decode("utf-8").split(';')
        return None


    @classmethod
    def _redis_blacklist_token(cls, jti: str, redis_pipeline: Pipeline):
        redis_pipeline.setex(f"blacklist_{jti}", cls._cache_exp, 1)


    @classmethod
    def _redis_check_blacklist(cls, jti: str) -> bool:
        return cls._redis_conn.exists(f"blacklist_{jti}")


    @classmethod
    def _redis_mark_refresh_token(cls, jti: str):
        cls._redis_conn.setex(f"refresh_{jti}", cls._cache_exp, 1)


    @classmethod
    def _redis_check_refresh_token_reuse(cls, jti: str) -> bool:
        return cls._redis_conn.exists(f"refresh_{jti}")
    

    @classmethod
    def _encode_token(cls, type: TokenType, subject: Dict[str, Union[str, int, float]]) -> Tuple[str, str]:
        """
        Encode a JWT token with the provided type and subject.
        
        :param `type`: Type of the token: `TokenType.ACCESS` or `TokenType.REFRESH`.
        :param `subject`: Dictionary containing claims to be included in the token payload.
            e.g. `{"user_id": 679, "username": "bob", "role": "admin"}.`
        :return: Generated token and its JTI (JWT unique identifier).
        """
        exp = cls._access_exp if type == TokenType.ACCESS else cls._refresh_exp
        jti = uuid.uuid4().hex
        payload = {
            "subject": subject,       # Subject claims
            "token_type": type.value, # Token type
            "exp": time.time() + exp, # Token expiration time
            "nbf": time.time(),       # Token start validity time
            "jti": jti,               # Token unique identifier
        }
        token = jwt.encode(payload, cls._secret, algorithm=cls._algorithm)
        return (token, jti)


    @classmethod
    def _decode_token(cls, token: str) -> Dict[str, Any]:
        """
        Decode the provided JWT token.
        
        :param `token`: JWT token string.
        :return: Decoded payload of the token.
        :raises: `HTTPException` for invalid or expired tokens.
        """
        try:
            return jwt.decode(token, cls._secret, algorithms=cls._algorithm)
        
        except DecodeError as e:
            logging.error(f"<JwtManager::decode_token> DecodeError: {str(e)}")
            raise HTTPException(status_code=401, detail="Invalid bearer token.")
        
        except ExpiredSignatureError as e:
            logging.error(f"<JwtManager::decode_token> ExpiredSignatureError: {str(e)}")
            raise HTTPException(status_code=401, detail="Invalid bearer token.")
        
        except InvalidTokenError as e:
            logging.error(f"<JwtManager::decode_token> InvalidTokenError: {str(e)}")
            raise HTTPException(status_code=401, detail="Invalid bearer token.")


class JwtBearer(HTTPBearer):
    """
    Custom JWT Bearer class for FastAPI to handle authentication.
    """
    
    def __init__(self, token_type: TokenType = TokenType.ACCESS, auto_error: bool = True):
        """
        Initialize the JwtBearer.
        
        :param `auto_error`: If `True`, automatically returns error responses.
        :param `token_type`: Type of the token to be accepted: `TokenType.ACCESS` | `TokenType.REFRESH`.
        """
        super(JwtBearer, self).__init__(auto_error=auto_error)
        self.token_type = token_type.value


    async def __call__(self, request: Request) -> AuthCredentials:
        """
        Override the default __call__ method to handle JWT token validation.
        
        :param `request`: FastAPI request object.
        :return: Decoded JWT token payload.
        :raises: `HTTPException` for invalid tokens.
        """
        credentials = await super(JwtBearer, self).__call__(request)     
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Missing or invalid token.")
        
        if credentials.scheme != "Bearer":
            raise HTTPException(status_code=401, detail="Expected authentication scheme 'Bearer'.")
                
        decoded_credentials = AuthCredentials(**JwtManager._decode_token(credentials.credentials))

        if self.token_type != decoded_credentials.token_type:
            logging.error("<JwtBearer> Invalid Token Type.")
            raise HTTPException(status_code=401, detail="Invalid bearer token.")
        
        if JwtManager._redis_check_blacklist(decoded_credentials.jti):
            logging.error(f'<JwtBearer> Revoked Token Error subject: {decoded_credentials.subject}.')
            raise HTTPException(status_code=401, detail="Invalid bearer token.")
        
        return decoded_credentials
