import re
from datetime import datetime

from app.db.weibo_db import db as weibo_db
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io

from app.redis_client import redis_client

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文显示字体

def analyze_fan_info(task_id):
    collection = weibo_db[task_id]
    # Find the data that matches the query
    data = list(collection.find())
    # Extract fan_info from each data entry
    fan_info_list = []
    for d in data:
        if 'fan_info' in d:
            fan_info_list.append(d['fan_info'])
    # Convert list of fan_info dictionaries into DataFrame
    fan_info_df = pd.DataFrame(fan_info_list)
    # Count number of fans by gender
    gender_counts = fan_info_df['gender'].value_counts()
    # Create a bar chart of the gender counts
    plt.figure(figsize=(6, 4))
    plt.bar(gender_counts.index, gender_counts.values)
    plt.title('粉丝性别分布')
    plt.xlabel('性别')
    plt.ylabel('数量')
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_gender_counts")
    plt.savefig(buf, format='png')
    buf.seek(0)
    gender_counts_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_gender_counts", gender_counts_bytes)
    plt.close()

    # Count number of fans by location
    location_counts = fan_info_df['location'].value_counts().head(10)

    # Create a bar chart of the location counts
    plt.figure(figsize=(12, 6))
    plt.bar(location_counts.index, location_counts.values)
    plt.title('粉丝分布位置 (top 10)')
    plt.xlabel('位置')
    plt.ylabel('数量')
    plt.xticks(rotation=45)
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_location_counts")
    plt.savefig(buf, format='png')
    buf.seek(0)
    location_counts_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_location_counts", location_counts_bytes)
    plt.close()

    # Create a heatmap of the number of fans by gender and location
    gender_location_counts = fan_info_df.groupby(['gender', 'location']).size().unstack()
    sns.heatmap(gender_location_counts, cmap='YlGnBu')
    plt.title('粉丝的性别和位置分布')
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_gender_location_counts")
    plt.savefig(buf, format='png')
    buf.seek(0)
    gender_location_counts_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_gender_location_counts", gender_location_counts_bytes)
    plt.close()

    # Age distribution of fans
    fan_info_df['account_age'] = (datetime.now() - pd.to_datetime(fan_info_df['created_at'])).apply(
        lambda x: x.days // 365)
    fan_info_df['account_age'].hist(bins=20)
    plt.title('粉丝年龄分布')
    plt.xlabel('年龄')
    plt.ylabel('数量')
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_age_distribution")
    plt.savefig(buf, format='png')
    buf.seek(0)
    age_distribution_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_age_distribution", age_distribution_bytes)
    plt.close()

    # Top interests of fans
    fan_desc = fan_info_df['description'].dropna().str.cat(sep='|')
    words = re.findall(r'\w+', fan_desc)
    word_count = pd.Series(words).value_counts()
    top_words = word_count[:20]
    plt.figure(figsize=(12, 6))
    plt.bar(top_words.index, top_words.values)
    plt.title('粉丝感兴趣话题')
    plt.xlabel('话题')
    plt.ylabel('数量')
    plt.xticks(rotation=45)
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_top_interests")
    plt.savefig(buf, format='png')
    buf.seek(0)
    top_interests_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_top_interests", top_interests_bytes)
    plt.close()

    # Influence of fans
    fan_info_df['influence'] = fan_info_df['followers_count']
    fan_info_df['influence'].hist(bins=20)
    plt.title('粉丝影响力')
    plt.xlabel('关注量')
    plt.ylabel('数量')
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_influence_distribution")
    plt.savefig(buf, format='png')
    buf.seek(0)
    influence_distribution_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_influence_distribution", influence_distribution_bytes)
    plt.close()

def run_weibo_fan_analyze(task_id):
    analyze_fan_info(task_id)

run_weibo_fan_analyze('19be4fe2-1205-4b1b-a657-fb82f5677dac')
