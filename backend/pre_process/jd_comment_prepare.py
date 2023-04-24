import os

from app.db.jd_db import db as jd_db
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from collections import Counter
import io
from app.redis_client import redis_client

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文显示字体

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


def clean_data(data):
    # Clean and preprocess data
    cleaned_data = []
    for item in data:
        content = item['content']
        # Remove HTML tags and special characters
        content = re.sub('<[^<]+?>', '', content)
        content = re.sub('[^\w\s]', '', content)
        cleaned_data.append(content)

    return cleaned_data


def tokenize_data(cleaned_data):
    # Tokenize the cleaned data
    words_list = []
    for content in cleaned_data:
        # Filter out stopwords
        words = [word for word in jieba.cut(content) if word not in stopwords]
        # Adjust the granularity of the words
        words = [word for word in words if len(word) >= 2]
        words_list.append(' '.join(words))

    return words_list


def count_words(words_list):
    # Count the word frequencies
    words_count = Counter(' '.join(words_list).split())

    return words_count


def generate_wordcloud(task_id, words_count):
    # Generate the wordcloud
    wordcloud = WordCloud(font_path=font_path, background_color='white', max_words=100, contour_width=3,
                          contour_color='steelblue')
    wordcloud.generate_from_frequencies(words_count)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    # Convert the image to bytes and store in Redis
    buf = io.BytesIO()
    # plt.savefig('1.png')
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_wordcloud", image_bytes)
    plt.close()


def run_jd_comment_analyze(task_id):
    data = load_data(task_id)
    cleaned_data = clean_data(data)
    words_list = tokenize_data(cleaned_data)
    words_count = count_words(words_list)
    generate_wordcloud(task_id, words_count)
