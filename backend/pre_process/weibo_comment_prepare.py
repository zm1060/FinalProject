import io
import os

import pandas as pd
import numpy as np
import jieba
import matplotlib.pyplot as plt
import seaborn as sns
import re
from wordcloud import WordCloud

from app.db.weibo_db import db as weibo_db
from app.redis_client import redis_client

# Set the font family to "SimHei"
plt.rcParams['font.family'] = 'SimHei'
# Get the absolute path of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Use the script directory to construct the path to the font file
font_path = os.path.join(script_dir, 'SimHei.ttf')

def remove_emoticons(text):
    return re.sub(r'\[.*?\]', '', text)


def preprocess_weibo_comment_data(data):
    # 将数据转化为Pandas DataFrame
    df = pd.DataFrame(data)
    # 对created_at列进行日期解析
    df['created_at'] = pd.to_datetime(df['created_at'])
    # 将like_counts列中的字符串转化为整数
    df['like_counts'] = df['like_counts'].astype(int)
    # 对content列进行分词和词频统计
    df['content'] = df['content'].apply(remove_emoticons)
    df['content'] = df['content'].apply(lambda x: jieba.lcut(x))  # Use jieba for Chinese word segmentation
    word_counts = pd.Series(np.concatenate(df['content'].values)).value_counts()
    # 返回处理后的数据和词频统计结果
    return df, word_counts[:50]  # Return only the top 50 most frequent words


def generate_weibo_comment_charts(df, word_counts, task_id):


    # Create a line chart of like counts over time
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['created_at'], df['like_counts'])
    ax.set_xlabel('日期')
    ax.set_ylabel('点赞数')
    ax.set_title('点赞数变化')
    buf = io.BytesIO()
    # plt.savefig(f'{task_id}_line_chart.png')
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_line_chart", image_bytes)
    plt.close()

    # Create a bar chart of word counts
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(word_counts.index, word_counts.values)
    ax.set_xticklabels(word_counts.index, rotation=45, ha='right')
    ax.set_xlabel('词')
    ax.set_ylabel('数量')
    ax.set_title('热点词')
    buf = io.BytesIO()
    # plt.savefig(f'{task_id}_bar_chart.png')
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_bar_chart", image_bytes)
    plt.close()

    # Create a word cloud of the most common words
    wordcloud = WordCloud(
        background_color='white',
        max_words=50,
        font_path=font_path
    ).generate_from_frequencies(word_counts)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_wordcloud", image_bytes)
    plt.close()

    # Create a heatmap of like counts by day and hour
    df['day'] = df['created_at'].dt.date
    df['hour'] = df['created_at'].dt.hour
    pivot_df = df.pivot_table(index='day', columns='hour', values='like_counts', aggfunc='mean')
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(pivot_df, cmap='coolwarm', ax=ax)
    ax.set_title('平均点赞量(时分)')
    buf = io.BytesIO()
    # plt.savefig(f'{task_id}_heatmap.png')
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f'{task_id}_heatmap', image_bytes)
    plt.close()


def run_weibo_comment_analyze(task_id):
    collection = weibo_db[task_id]
    # Find the data that matches the query
    data = list(collection.find())
    df, word_counts = preprocess_weibo_comment_data(data)
    generate_weibo_comment_charts(df, word_counts, task_id)


# run_weibo_comment_analyze('4dc92e7d-1152-4fdf-b105-ba1401dedce8')
