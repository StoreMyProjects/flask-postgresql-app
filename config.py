import redis
import os

SECRET_KEY = 'your_secret_key'
SESSION_PERMANENT = False
# SESSION_TYPE = "filesystem"
DEBUG = True
SESSION_TYPE = "redis"

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

SESSION_REDIS = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True,
)

SESSION_PERMANENT = False
SESSION_USE_SIGNER = True