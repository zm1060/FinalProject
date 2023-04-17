import json
import pandas as pd
import matplotlib.pyplot as plt
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['users']
collection = db['tasks']

# 检索数据
data = []
for doc in collection.find():
    data.append(doc)

# 将数据转换为pandas DataFrame对象
df = pd.DataFrame.from_dict(data)

# 提取stats指标
stats = df['stats'].apply(pd.Series)
df = pd.concat([df.drop('stats', axis=1), stats], axis=1)

# 将时间戳转换为DateTimeIndex对象
df.index = pd.to_datetime(df['task_time'])

# 绘制指标随时间的变化趋势
fig, ax = plt.subplots(figsize=(10, 6))
df.plot(y=['downloader/request_count', 'downloader/response_count'], ax=ax)
ax.set_xlabel('Time')
ax.set_ylabel('Count')
ax.set_title('Request and Response Count over Time')
plt.show()
