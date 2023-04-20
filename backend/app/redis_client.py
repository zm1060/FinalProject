import os


import redis
from redis.client import Redis

redis_host = os.getenv('REDIS_HOST', 'localhost')
# Create a Redis client
redis_client = Redis(redis_host, port=6379, db=0)