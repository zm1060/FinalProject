import os
from redis import ConnectionPool, Redis

# 获取 Redis 主机地址
redis_host = os.getenv('REDIS_HOST', 'localhost')

# 创建 Redis 连接池
redis_pool = ConnectionPool(host=redis_host, port=6379, db=0)

# 创建 Redis 客户端
redis_client = Redis(connection_pool=redis_pool)
