from decouple import config

DEBUG = config('debug', default=False, cast=bool)

REDIS_HOST = config("redis_host", default="localhost")
REDIS_PORT = config("redis_port", cast=int, default=6379)
REDIS_PASS = config("redis_pass", default=None)

JWT_SECRET = config("jwt_secret")
JWT_ALGORITHM = config("jwt_algorithm")
JWT_ACCESS_EXP = config("jwt_access_token_time", cast=int)
JWT_REFRESH_EXP = config("jwt_refresh_token_time", cast=int)
JWT_REDIS_INDEX = config("jwt_redis_index", cast=int, default=0)

RATE_LIMITER_REDIS_INDEX = config("rate_limiter_redis_index", cast=int, default=1)
