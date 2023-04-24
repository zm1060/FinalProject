from app.db.jd_db import db
from app.es_client import es

collection = db['83654950-0420-40f6-b83b-8b436666d190']
results = []
for result in collection.find():
    result['_id'] = str(result['_id'])  # convert ObjectId to string
    results.append(result)
print(results)

import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)
redis_client.flushdb()



if es.indices.exists(index="jd_comments"):
    es.indices.delete(index="jd_comments")