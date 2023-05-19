import io
import os

import jieba
import pandas as pd
from snownlp import SnowNLP
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

from app.db.jd_db import db as jd_db
from app.redis_client import redis_client

# Set the font family to "SimHei"
plt.rcParams['font.sans-serif'] = ['SimHei']

# Get the absolute path of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Use the script directory to construct the path to the font file
font_path = os.path.join(script_dir, 'SimHei.ttf')

# Get the directory of the current script
dirname = os.path.dirname(__file__)

# Construct the path to the stopwords file relative to the script directory
stopwords_path = os.path.join(dirname, 'common_stopwords.txt')

# Open the stopwords file using the relative path
with open(stopwords_path, 'r', encoding='utf-8') as f:
    stopwords = [line.strip() for line in f.readlines()]


def load_data(task_id):
    # Get data from database
    collection = jd_db[task_id]
    data = collection.find()
    return data


def tokenize_data(cleaned_data):
    # Tokenize the cleaned data
    words_list = []
    for product in cleaned_data:
        content = product.get('content', [])
        for c in content:
            for word in jieba.cut(c):
                if word not in stopwords and word != ' ':
                    words_list.append(word)

    return words_list


def count_words(words_list):
    # Count the word frequencies
    words_count = Counter(' '.join(words_list).split())

    return words_count


def generate_wordcloud(task_id):
    data = load_data(task_id)
    words_list = tokenize_data(data)
    words_count = count_words(words_list)
    # Generate the wordcloud
    wordcloud = WordCloud(font_path=font_path, background_color='white', max_words=100, contour_width=3,
                          contour_color='steelblue')
    wordcloud.generate_from_frequencies(words_count)
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(wordcloud, interpolation='bilinear')
    # Add a colorbar to the plot
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("词频", rotation=-90, va="bottom")
    ax.set_title("京东商品评论词云图", fontsize=16)
    ax.axis('off')

    # Convert the image to bytes and store in Redis
    buf = io.BytesIO()
    # plt.savefig(f"{task_id}_wordcloud.png")
    fig.savefig(buf, format='png')
    # fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    image_bytes = buf.getvalue()
    redis_client.set(f"{task_id}_wordcloud", image_bytes)
    plt.close()


def analyze_jd_comment_sentiment(task_id):
    data = load_data(task_id)
    sentiment_list = []
    for d in data:
        content = d['content'][0]
        blob = SnowNLP(content)
        sentiment_list.append(blob.sentiments)

    # Convert list of sentiment scores into DataFrame
    sentiment_df = pd.DataFrame(sentiment_list, columns=['情感得分'])
    # Create a histogram of the sentiment scores
    plt.figure(figsize=(6, 4))
    plt.hist(sentiment_df['情感得分'], bins=20)
    plt.title('京东产品评价情感分布')
    plt.xlabel('情感得分')
    plt.ylabel('评价数量')
    buf = io.BytesIO()
    # plt.savefig('x.png')
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.getvalue()
    redis_client.set(f"{task_id}_sentiment_histogram", image_bytes)
    plt.close()


def analyze_review_sentiment(task_id):
    data = load_data(task_id)
    # Convert reviews JSON to Pandas DataFrame
    df = pd.DataFrame(data)

    # Perform feature analysis
    feature_counts = Counter()
    for text in df['content'][0]:
        blob = SnowNLP(text)
        for feature in blob.words:
            if feature not in stopwords:  # Filter out personal pronouns
                feature_counts[feature] += 1

    # Get top 20 features and their counts
    top_features = pd.DataFrame(feature_counts.most_common(20), columns=['Feature', 'Count'])

    # Plot feature frequency
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(y=top_features['Feature'], width=top_features['Count'])
    ax.set_title('Top Features')
    ax.set_xlabel('Count')

    # Convert the image to bytes and store in Redis
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    image_bytes = buf.getvalue()
    redis_client.set(f"{task_id}_feature_analysis", image_bytes)
    plt.close()

def run_jd_comment_analyze(task_id):
    generate_wordcloud(task_id)
    analyze_jd_comment_sentiment(task_id)
    analyze_review_sentiment(task_id)


run_jd_comment_analyze('dcca51ae-a556-46bb-a1db-ef0dc1219fce')
