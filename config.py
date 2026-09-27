import os

import redis

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
DEBUG = os.getenv("DEBUG", "False").lower() in {"1", "true", "yes"}
SESSION_PERMANENT = False
SESSION_USE_SIGNER = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = not DEBUG

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_SSL = os.getenv("REDIS_SSL", "false").lower() in {"1", "true", "yes"}

if REDIS_HOST:
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        ssl=REDIS_SSL,
        decode_responses=True,
    )
else:
    SESSION_TYPE = "filesystem"
    SESSION_REDIS = None