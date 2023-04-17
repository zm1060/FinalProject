import pymongo
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from nltk.sentiment import SentimentIntensityAnalyzer

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['jd']
task_id = 'ed44f3ac-3a7d-4897-b05b-e59005dbba3b'
collection = db[task_id]

# 读取所有商品数据
product_data = list(collection.find())

# 创建一个空的DataFrame
df_list = []

# 遍历所有商品数据
for product in product_data:
    # 将name和content转换为字典
    data_dict = dict(zip(product['name'], product['content']))
    # 将字典添加到DataFrame list中
    df_list.append(pd.DataFrame([data_dict]))

# 使用pd.concat合并DataFrame list
df = pd.concat(df_list, ignore_index=True)

# 转换数据类型
df = df.apply(pd.to_numeric, errors='ignore')

# 统计各个属性的缺失值数量
missing_values = df.isnull().sum()
plt.rcParams['font.family'] = 'SimHei'

# 绘制柱状图
plt.figure(figsize=(12, 6))
sns.barplot(x=missing_values.index, y=missing_values.values)
plt.xticks(rotation=90)
plt.xlabel('Property Name')
plt.ylabel('Number of Missing Values')
plt.show()

# Data visualization
sns.scatterplot(x=df.columns[0], y=df.columns[1], data=df)
plt.title(f'Scatter plot of {df.columns[0]} vs. {df.columns[1]}')
plt.show()

sns.histplot(df[df.columns[1]])
plt.title(f'Histogram of {df.columns[1]}')
plt.show()

sns.histplot(df[df.columns[4]])
plt.title(f'Histogram of {df.columns[4]}')
plt.show()
