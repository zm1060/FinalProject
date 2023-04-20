import re
from datetime import datetime
import numpy as np
from nltk import TweetTokenizer
import gensim
from gensim import corpora, models
import pandas as pd
import matplotlib.pyplot as plt
from snownlp import SnowNLP
from textblob import TextBlob
import io

from app.db.weibo_db import db as weibo_db
from app.redis_client import redis_client

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文显示字体


def analyze_sentiment(task_id):
    collection = weibo_db[task_id]
    # Find the data that matches the query
    data = list(collection.find())
    # Extract text content from each data entry
    content_list = []
    for d in data:
        if 'content' in d:
            content_list.append(d['content'])
    # Perform sentiment analysis on the text content
    sentiment_list = []
    for content in content_list:
        blob = TextBlob(content)
        sentiment_list.append(blob.sentiment.polarity)
    # Convert list of sentiment scores into DataFrame
    sentiment_df = pd.DataFrame(sentiment_list, columns=['sentiment'])
    # Create a histogram of the sentiment scores
    plt.figure(figsize=(6, 4))
    plt.hist(sentiment_df['sentiment'], bins=20)
    plt.title('Sentiment distribution of posts')
    plt.xlabel('Sentiment score')
    plt.ylabel('Count')
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_sentiment_histogram")
    plt.savefig(buf, format='png')
    buf.seek(0)
    sentiment_histogram_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_sentiment_histogram", sentiment_histogram_bytes)
    plt.close()


def analyze_time_series(task_id):
    collection = weibo_db[task_id]
    data = list(collection.find())
    # Create a list of timestamps for each post
    timestamp_list = []
    for d in data:
        timestamp = datetime.strptime(d['created_at'], '%Y-%m-%d %H:%M:%S')
        timestamp_list.append(timestamp)
    # Convert timestamp list into Pandas Series and resample by hour
    ts = pd.Series([1] * len(timestamp_list), index=timestamp_list)
    ts = ts.resample('H').sum().fillna(0)
    # Create a line chart of the post frequency over time
    plt.figure(figsize=(12, 6))
    plt.plot(ts)
    plt.title('Post frequency over time')
    plt.xlabel('Date')
    plt.ylabel('Number of posts')
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_time_series")
    plt.savefig(buf, format='png')
    buf.seek(0)
    time_series_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_time_series", time_series_bytes)
    plt.close()


def analyze_user_engagement(task_id):
    collection = weibo_db[task_id]
    data = list(collection.find())
    # Create a list of engagement metrics for each post
    reposts_list = []
    comments_list = []
    likes_list = []
    for d in data:
        reposts_list.append(d['reposts_count'])
        comments_list.append(d['comments_count'])
        likes_list.append(d['attitudes_count'])
    # Convert engagement metric lists into Pandas Series
    reposts = pd.Series(reposts_list)
    comments = pd.Series(comments_list)
    likes = pd.Series(likes_list)
    # Create a stacked bar chart of the engagement metrics
    plt.figure(figsize=(10, 6))
    plt.bar(reposts.index, reposts, label='Reposts')
    plt.bar(comments.index, comments, bottom=reposts, label='Comments')
    plt.bar(likes.index, likes, bottom=reposts + comments, label='Likes')
    plt.title('User engagement with posts')
    plt.xlabel('Post index')
    plt.ylabel('Number of engagements')
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_user_engagement")
    plt.savefig(buf, format='png')
    buf.seek(0)
    user_engagement_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_user_engagement", user_engagement_bytes)
    plt.close()


def analyze_hashtags(task_id):
    collection = weibo_db[task_id]
    data = list(collection.find())
    # Create a list of hashtags for each post
    hashtag_list = []
    for d in data:
        if 'content' in d:
            content = d['content']
            hashtags = re.findall(r'#(\w+)#', content)
            hashtag_list.extend(hashtags)
    # Count number of posts by hashtag
    hashtag_counts = pd.Series(hashtag_list).value_counts()
    # Create a bar chart of the hashtag counts
    plt.figure(figsize=(10, 6))
    plt.bar(hashtag_counts.index[:10], hashtag_counts.values[:10])
    plt.title('Hashtag frequency in posts')
    plt.xlabel('Hashtag')
    plt.ylabel('Frequency')
    plt.xticks(rotation=90)
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_hashtag_frequency")
    plt.savefig(buf, format='png')
    buf.seek(0)
    hashtag_counts_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_hashtag_frequency", hashtag_counts_bytes)
    plt.close()


def analyze_topics(task_id):
    collection = weibo_db[task_id]
    # Find the data that matches the query
    data = list(collection.find())
    # Extract text content from each data entry
    content_list = []
    for d in data:
        if 'content' in d:
            content_list.append(d['content'])
    # Tokenize the text content using TweetTokenizer
    tokenizer = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=True)
    tokenized_content = [tokenizer.tokenize(content) for content in content_list]
    # Create dictionary and corpus
    dictionary = corpora.Dictionary(tokenized_content)
    corpus = [dictionary.doc2bow(tokens) for tokens in tokenized_content]
    # Perform LDA topic modeling
    lda_model = gensim.models.LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=5, passes=10, workers=2)
    # Print the top 5 topics and their keywords
    topics = lda_model.show_topics(num_topics=5, num_words=10)
    for topic in topics:
        print(topic)
    # Create a scatter plot of the topic distribution of the posts
    topic_distribution = np.zeros((len(data), 5))
    for i, doc in enumerate(corpus):
        topic_probs = lda_model.get_document_topics(doc)
        for j, prob in topic_probs:
            topic_distribution[i][j] = prob
    plt.figure(figsize=(8, 6))
    plt.scatter(np.arange(len(data)), topic_distribution[:, 0], label='Topic 1')
    plt.scatter(np.arange(len(data)), topic_distribution[:, 1], label='Topic 2')
    plt.scatter(np.arange(len(data)), topic_distribution[:, 2], label='Topic 3')
    plt.scatter(np.arange(len(data)), topic_distribution[:, 3], label='Topic 4')
    plt.scatter(np.arange(len(data)), topic_distribution[:, 4], label='Topic 5')
    plt.title('博文的话题分布')
    plt.xlabel('Post index')
    plt.ylabel('Topic probability')
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_topic_distribution")
    plt.savefig(buf, format='png')
    buf.seek(0)
    topic_distribution_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_topic_distribution", topic_distribution_bytes)
    plt.close()



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
    # Count number of posts by source
    source_counts = pd.Series(clean_source_list).value_counts()
    # Only keep top 30 sources
    source_counts = source_counts[:20]
    # Create a pie chart of the source counts
    plt.figure(figsize=(8, 6))
    plt.pie(source_counts.values, labels=source_counts.index)
    plt.title('博文发布源分布')
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_post_sources")
    plt.savefig(buf, format='png')
    buf.seek(0)
    source_counts_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_post_sources", source_counts_bytes)
    plt.close()


def analyze_sentiment(task_id):
    collection = weibo_db[task_id]
    # Find the data that matches the query
    data = list(collection.find())
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
    plt.title('博文情感分布')
    plt.xlabel('情感分数')
    plt.ylabel('数量')
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_sentiment_histogram")
    plt.savefig(buf, format='png')
    buf.seek(0)
    sentiment_histogram_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_sentiment_histogram", sentiment_histogram_bytes)
    plt.close()


def analyze_time_series(task_id):
    collection = weibo_db[task_id]
    data = list(collection.find())
    # Create a list of timestamps for each post
    timestamp_list = []
    for d in data:
        timestamp = datetime.strptime(d['created_at'], '%Y-%m-%d %H:%M:%S')
        timestamp_list.append(timestamp)
    # Convert timestamp list into Pandas Series and resample by hour
    ts = pd.Series([1] * len(timestamp_list), index=timestamp_list)
    ts = ts.resample('H').sum().fillna(0)
    # Create a line chart of the post frequency over time
    plt.figure(figsize=(12, 6))
    plt.plot(ts)
    plt.title('博文发布频率')
    plt.xlabel('日期')
    plt.ylabel('博文数量')
    buf = io.BytesIO()
    plt.savefig(f"{task_id}_time_series")
    plt.savefig(buf, format='png')
    buf.seek(0)
    time_series_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_time_series", time_series_bytes)
    plt.close()


def run_weibo_search_analyze(task_id):
    analyze_time_series(task_id)
    analyze_user_engagement(task_id)
    analyze_hashtags(task_id)
    analyze_topics(task_id)
    analyze_sentiment(task_id)
    analyze_post_sources(task_id)


if __name__ == '__main__':
    run_weibo_search_analyze('d98447f6-9c4a-47e2-80ea-23cb5b08b9e2')
