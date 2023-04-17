import pandas as pd
import numpy as np
import jieba

import matplotlib.pyplot as plt
import pymongo
import seaborn as sns

import re

from wordcloud import WordCloud


def remove_emoticons(text):
    return re.sub(r'\[.*?\]', '', text)


def preprocess_data(data):
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


def generate_charts(df, word_counts, task_id):
    # Set the font family to "SimHei"
    plt.rcParams['font.family'] = 'SimHei'

    # Create a line chart of like counts over time
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['created_at'], df['like_counts'])
    ax.set_xlabel('日期')
    ax.set_ylabel('点赞数')
    ax.set_title('点赞数变化')
    plt.savefig(f'{task_id}_line_chart.png')
    plt.close()

    # Create a bar chart of word counts
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(word_counts.index, word_counts.values)
    ax.set_xticklabels(word_counts.index, rotation=45, ha='right')
    ax.set_xlabel('Words')
    ax.set_ylabel('Count')
    ax.set_title('Word Count')
    plt.savefig(f'{task_id}_bar_chart.png')
    plt.close()

    # Create a word cloud of the most common words
    font_path = "C:/Windows/Fonts/SimHei.ttf"
    wordcloud = WordCloud(
        background_color='white',
        max_words=50,
        font_path=font_path
    ).generate_from_frequencies(word_counts)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(f'{task_id}_word_cloud.png')
    plt.close()

    # Create a heatmap of like counts by day and hour
    df['day'] = df['created_at'].dt.date
    df['hour'] = df['created_at'].dt.hour
    pivot_df = df.pivot_table(index='day', columns='hour', values='like_counts', aggfunc='mean')
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(pivot_df, cmap='coolwarm', ax=ax)
    ax.set_title('Average Like Counts by Day and Hour')
    plt.savefig(f'{task_id}_heatmap.png')
    plt.close()


# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['weibo']
task_id = '4dc92e7d-1152-4fdf-b105-ba1401dedce8'
collection = db[task_id]

# Find the data that matches the query
data = list(collection.find())
print(data)

df, word_counts = preprocess_data(data)
print(df)
print(word_counts)
generate_charts(df, word_counts, task_id)

