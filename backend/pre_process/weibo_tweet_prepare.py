import re

import pandas as pd
from snownlp import SnowNLP

from app.db.weibo_db import db as weibo_db
import matplotlib.pyplot as plt
import io

from app.redis_client import redis_client

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文显示字体


def analyze_weibo_data(task_id):
    # Get Weibo data from database
    collection = weibo_db[task_id]
    weibo_data = list(collection.find())
    # Extract engagement metrics
    reposts_list = []
    comments_list = []
    likes_list = []
    for d in weibo_data:
        if 'reposts_count' in d:
            reposts_list.append(d['reposts_count'])
        if 'comments_count' in d:
            comments_list.append(d['comments_count'])
        if 'attitudes_count' in d:
            likes_list.append(d['attitudes_count'])
    # Convert lists of engagement metrics into DataFrame
    engagement_df = pd.DataFrame({'转发数': reposts_list, '评论数': comments_list, '点赞数': likes_list})
    # Create a boxplot of the engagement metrics
    plt.figure(figsize=(8, 6))
    engagement_df.boxplot()
    plt.title('微博用户参与度分布')
    plt.ylabel('数量')
    buf = io.BytesIO()
    plt.savefig(f'{task_id}_engagement_boxplot.png')
    plt.savefig(buf, format='png')
    buf.seek(0)
    redis_client.set(f'{task_id}_engagement_boxplot', buf.getvalue())
    plt.close()

    # Perform sentiment analysis
    sentiment_list = []
    for d in weibo_data:
        if 'content' in d:
            content = d['content']
            blob = SnowNLP(content)
            sentiment_list.append(blob.sentiments)
    # Convert list of sentiment scores into DataFrame
    sentiment_df = pd.DataFrame(sentiment_list, columns=['情感得分'])
    # Create a histogram of the sentiment scores
    plt.figure(figsize=(6, 4))
    plt.hist(sentiment_df['情感得分'], bins=20)
    plt.title('微博情感分布')
    plt.xlabel('情感得分')
    plt.ylabel('微博数量')
    buf = io.BytesIO()
    plt.savefig(f'{task_id}_sentiment_histogram.png')
    plt.savefig(buf, format='png')
    buf.seek(0)
    redis_client.set(f'{task_id}_sentiment_histogram', buf.getvalue())
    plt.close()

    # Extract hashtag information
    hashtag_list = []
    for d in weibo_data:
        if 'content' in d:
            content = d['content']
            hashtags = re.findall(r'#(\w+)#', content)
            hashtag_list.extend(hashtags)
    # Count number of posts per hashtag
    hashtag_counts = pd.Series(hashtag_list).value_counts()
    # Select top N hashtags
    top_hashtags = hashtag_counts.nlargest(10)
    # Create a bar chart of the top hashtags
    plt.figure(figsize=(8, 6))
    plt.bar(top_hashtags.index, top_hashtags.values)
    plt.title('微博热门话题')
    plt.xlabel('话题标签')
    plt.ylabel('微博数量')
    plt.xticks(rotation=45, ha='right')
    buf = io.BytesIO()
    plt.savefig(f'{task_id}_top_hashtags.png')
    plt.savefig(buf, format='png')
    buf.seek(0)
    redis_client.set(f'{task_id}_top_hashtags', buf.getvalue())
    plt.close()

    # Extract time information
    time_list = []
    for d in weibo_data:
        if 'created_at' in d:
            time_list.append(pd.to_datetime(d['created_at']))
    # Count number of posts per hour
    hourly_post_count = pd.Series(time_list).dt.hour.value_counts().sort_index()
    # Create a bar chart of the hourly post count
    plt.figure(figsize=(8, 6))
    plt.bar(hourly_post_count.index, hourly_post_count.values)
    plt.title('微博发布时间分布')
    plt.xlabel('小时')
    plt.ylabel('微博数量')
    buf = io.BytesIO()
    plt.savefig('hourly_post_count.png')
    plt.savefig(buf, format='png')
    buf.seek(0)
    redis_client.set('hourly_post_count', buf.getvalue())
    plt.close()

def run_weibo_tweet_analyze(task_id):
    analyze_weibo_data(task_id)

run_weibo_tweet_analyze('4c17f1cb-ebf2-443e-95bb-fb0e373f9f9f')