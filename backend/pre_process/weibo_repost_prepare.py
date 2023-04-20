import re

import pandas as pd
from snownlp import SnowNLP

from app.db.weibo_db import db as weibo_db
import matplotlib.pyplot as plt
import io

from app.redis_client import redis_client

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文显示字体


def analyze_post_sources(task_id):
    collection = weibo_db[task_id]
    # Find the data that matches the query
    data = list(collection.find())
    # Extract source information from each data entry
    source_list = []
    for d in data:
        if 'source' in d:
            source_list.append(d['source'])
    clean_source_list = []
    for source in source_list:
        clean_source = re.sub('<.*?>', '', source)  # replace HTML tags with empty string
        if clean_source:
            clean_source_list.append(clean_source)

    # print(clean_source_list)
    # Count number of posts by source
    source_counts = pd.Series(clean_source_list).value_counts()
    # Create a pie chart of the source counts
    plt.figure(figsize=(8, 6))
    plt.pie(source_counts.values, labels=source_counts.index)
    plt.title('分布博文的使用设备分布')
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_post_sources")
    plt.savefig(buf, format='png')
    buf.seek(0)
    source_counts_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_post_sources", source_counts_bytes)
    plt.close()

    # Extract text content from each data entry
    content_list = []
    for d in data:
        if 'content' in d:
            content_list.append(d['content'])
    # Perform sentiment analysis on the text content
    sentiment_list = []
    for content in content_list:
        blob = SnowNLP(content)
        sentiment_list.append(blob.sentiments)
    # Convert list of sentiment scores into DataFrame
    sentiment_df = pd.DataFrame(sentiment_list, columns=['sentiment'])
    # Create a histogram of the sentiment scores
    plt.figure(figsize=(6, 4))
    plt.hist(sentiment_df['sentiment'], bins=20)
    plt.title('博文的情感分布')
    plt.xlabel('情感分数(0:消极  1:积极)')
    plt.ylabel('数量')
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_sentiment_histogram")
    plt.savefig(buf, format='png')
    buf.seek(0)
    sentiment_histogram_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_sentiment_histogram", sentiment_histogram_bytes)
    plt.close()

    # Extract posting time from each data entry
    time_list = []
    for d in data:
        if 'created_at' in d:
            time_list.append(pd.to_datetime(d['created_at']))
    # Convert list of posting times into DataFrame
    time_df = pd.DataFrame({'time': time_list})
    # Group posting times by day and count number of posts per day
    daily_post_count = time_df.groupby(pd.Grouper(key='time', freq='D')).size()
    # Create a line chart of the daily post count
    plt.figure(figsize=(8, 6))
    plt.plot(daily_post_count)
    plt.title('博文发布频率')
    plt.xlabel('日期')
    plt.ylabel('博文数量')
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_posting_frequency")
    plt.savefig(buf, format='png')
    buf.seek(0)
    posting_frequency_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_posting_frequency", posting_frequency_bytes)
    plt.close()

    # Extract engagement metrics from each data entry
    reposts_list = []
    comments_list = []
    likes_list = []
    for d in data:
        if 'reposts_count' in d:
            reposts_list.append(d['reposts_count'])
        if 'comments_count' in d:
            comments_list.append(d['comments_count'])
        if 'attitudes_count' in d:
            likes_list.append(d['attitudes_count'])
    # Convert lists of engagement metrics into DataFrame
    engagement_df = pd.DataFrame({'Reposts': reposts_list, 'Comments': comments_list, 'Likes': likes_list})
    # Create a boxplot of the engagement metrics
    plt.figure(figsize=(8, 6))
    engagement_df.boxplot()
    plt.title('博文用户参与度')
    plt.ylabel('数量')
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_user_engagement")
    plt.savefig(buf, format='png')
    buf.seek(0)
    user_engagement_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_user_engagement", user_engagement_bytes)
    plt.close()

    # Extract hashtags from each data entry
    hashtag_list = []
    for d in data:
        if 'content' in d:
            content = d['content']
            hashtags = re.findall(r'#(\w+)#', content)
            hashtag_list.extend(hashtags)
    print(hashtag_list)
    # Count number of posts by hashtag
    hashtag_counts = pd.Series(hashtag_list).value_counts()
    # Select the top 10 most frequently used hashtags
    top_hashtags = hashtag_counts.nlargest(10)
    # Create a bar chart of the top hashtags
    plt.figure(figsize=(8, 6))
    plt.bar(top_hashtags.index, top_hashtags.values)
    plt.title('Top 10 hashtags')
    plt.xlabel('Hashtag')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_top_hashtags")
    plt.savefig(buf, format='png')
    buf.seek(0)
    top_hashtags_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_top_hashtags", top_hashtags_bytes)
    plt.close()


def run_weibo_post_analyze(task_id):
    analyze_post_sources(task_id)


run_weibo_post_analyze('06aa4ec5-bdcc-455f-970b-f2c43aeec47d')
