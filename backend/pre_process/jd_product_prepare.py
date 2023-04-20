from app.db.jd_db import db as jd_db
import jieba
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from wordcloud import WordCloud
import io
import redis

from app.redis_client import redis_client

# font_path = '../SimHei.ttf'  # 根据实际字体文件路径进行调整
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文显示字体
#
# task_id = 'ed44f3ac-3a7d-4897-b05b-e59005dbba3b'
#
# products = jd_db[task_id].find_one()
# name = products['name']
# content = products['content']
# attributes = dict(zip(name, content))
#
# # 分词处理
# with open('common_stopwords.txt', 'r', encoding='utf-8') as f:
#     stopwords = [line.strip() for line in f.readlines()]
#
# # 从数据库中读取产品数据
# all_words = []
# for content_value in content:
#     # 分词处理
#     words = []
#     for word in jieba.cut(content_value):
#         if word not in stopwords and word != ' ':
#             words.append(word)
#     all_words.extend(words)
#
# # 统计每个属性值出现的次数，并绘制柱状图和热力图
# attributes_counts = {}
# for attribute, value in attributes.items():
#     if attribute != '_id' and attribute != 'url':
#         if attribute not in attributes_counts:
#             attributes_counts[attribute] = {}
#         if isinstance(value, list):
#             for v in value:
#                 if v in attributes_counts[attribute]:
#                     attributes_counts[attribute][v] += 1
#                 else:
#                     attributes_counts[attribute][v] = 1
#         else:
#             if value in attributes_counts[attribute]:
#                 attributes_counts[attribute][value] += 1
#             else:
#                 attributes_counts[attribute][value] = 1
#
# for attribute, values in attributes_counts.items():
#     if len(values) > 1:
#         sorted_values = sorted(values.items(), key=lambda x: x[1], reverse=True)
#         top_values = dict(sorted_values[:10])
#         labels = list(top_values.keys())
#         counts = list(top_values.values())
#         plt.figure(figsize=(10, 6))
#         plt.bar(labels, counts)
#         plt.title(attribute)
#         plt.xlabel('Value')
#         plt.ylabel('Count')
#         plt.xticks(rotation=45)
#         plt.savefig(f'{task_id}_{attribute}.png')
#         plt.close()
#
# df = pd.DataFrame(attributes_counts)
# sns.heatmap(df, cmap='YlGnBu')
# plt.title('产品属性热力图')
# buf = io.BytesIO()
# plt.savefig(buf, format='png')
# buf.seek(0)
# heatmap_bytes = buf.getvalue()
# buf.close()
# # Store the bytes in Redis
# redis_client.set(f"{task_id}_heatmap", heatmap_bytes)
# plt.close()
#
# products = list(jd_db[task_id].find())
#
# # 从数据库中读取产品数据
# all_words = []
# for product in products:
#     content = product.get('content', [])
#     # 分词处理
#     words = []
#     for c in content:
#         for word in jieba.cut(c):
#             if word not in stopwords and word != ' ':
#                 words.append(word)
#     all_words.extend(words)
#
# # 统计每个词出现的次数
# word_counts = {}
# for word in all_words:
#     if word in word_counts:
#         word_counts[word] += 1
#     else:
#         word_counts[word] = 1
# # 绘制词云图
# wordcloud = WordCloud(font_path=font_path, background_color="white", width=800, height=400).generate_from_frequencies(
#     word_counts)
# plt.figure(figsize=(12, 6))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# buf = io.BytesIO()
# plt.savefig(buf, format='png')
# buf.seek(0)
# heatmap_bytes = buf.getvalue()
# buf.close()
# redis_client.set(f"{task_id}_wordcloud", heatmap_bytes)
# plt.close()
#
# # 统计每个属性值出现的次数，并绘制柱状图
# attributes_counts = {}
# for product in products:
#     for attribute, value in zip(product['name'], product['content']):
#         if attribute not in attributes_counts:
#             attributes_counts[attribute] = {}
#         if isinstance(value, list):
#             for v in value:
#                 if v in attributes_counts[attribute]:
#                     attributes_counts[attribute][v] += 1
#                 else:
#                     attributes_counts[attribute][v] = 1
#         else:
#             if value in attributes_counts[attribute]:
#                 attributes_counts[attribute][value] += 1
#             else:
#                 attributes_counts[attribute][value] = 1
#
# for attribute, values in attributes_counts.items():
#     if len(values) > 1:
#         sorted_values = sorted(values.items(), key=lambda x: x[1], reverse=True)
#         top_values = dict(sorted_values[:10])
#         labels = list(top_values.keys())
#         counts = list(top_values.values())
#         plt.figure(figsize=(10, 6))
#         plt.bar(labels, counts)
#         plt.title(attribute)
#         plt.xlabel('Value')
#         plt.ylabel('Count')
#         plt.xticks(rotation=45)
#         buf = io.BytesIO()
#         plt.savefig(buf, format='png')
#         buf.seek(0)
#         heatmap_bytes = buf.getvalue()
#         buf.close()
#         # Store the bytes in Redis
#         redis_client.set(f"{task_id}_{attribute}_bar", heatmap_bytes)
#         plt.close()

# df = pd.DataFrame(attributes_counts)
# # 使用Seaborn绘制热力图
# plt.figure(figsize=(10, 8))
# sns.heatmap(df, annot=True, cmap='coolwarm', fmt='.0f')
# plt.xticks(rotation=90)
# plt.yticks(rotation=0)
# buf = io.BytesIO()
# plt.savefig(buf, format='png')
# buf.seek(0)
# heatmap_bytes = buf.getvalue()
# buf.close()
# redis_client.set(f"{task_id}_heatmap.png", heatmap_bytes)


# Set font and stopwords
font_path = '../SimHei.ttf'  # 根据实际字体文件路径进行调整
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文显示字体

with open('common_stopwords.txt', 'r', encoding='utf-8') as f:
    stopwords = [line.strip() for line in f.readlines()]


def analyze_attributes(task_id):
    # Get products from database
    products = jd_db[task_id].find_one()
    name = products['name']
    content = products['content']
    attributes = dict(zip(name, content))

    # Count attribute values and create plots
    for attribute, values in get_attribute_counts(attributes).items():
        if len(values) > 1:
            sorted_values = sorted(values.items(), key=lambda x: x[1], reverse=True)
            top_values = dict(sorted_values[:10])
            labels = list(top_values.keys())
            counts = list(top_values.values())
            plt.figure(figsize=(10, 6))
            plt.bar(labels, counts)
            plt.title(attribute)
            plt.xlabel('Value')
            plt.ylabel('Count')
            plt.xticks(rotation=45)
            plt.savefig(f'{task_id}_{attribute}.png')
            plt.close()

    # Create heatmap of attribute values
    df = pd.DataFrame(get_attribute_counts(attributes))
    sns.heatmap(df, cmap='YlGnBu')
    plt.title('产品属性热力图')
    buf = io.BytesIO()
    # plt.savefig(f"{task_id}_heatmap")
    plt.savefig(buf, format='png')
    buf.seek(0)
    heatmap_bytes = buf.getvalue()
    buf.close()
    # Store the bytes in Redis
    redis_client.set(f"{task_id}_heatmap", heatmap_bytes)
    plt.close()


def get_attribute_counts(attributes):
    # Count occurrences of attribute values
    attributes_counts = {}
    for attribute, value in attributes.items():
        if attribute != '_id' and attribute != 'url':
            if attribute not in attributes_counts:
                attributes_counts[attribute] = {}
            if isinstance(value, list):
                for v in value:
                    if v in attributes_counts[attribute]:
                        attributes_counts[attribute][v] += 1
                    else:
                        attributes_counts[attribute][v] = 1
            else:
                if value in attributes_counts[attribute]:
                    attributes_counts[attribute][value] += 1
                else:
                    attributes_counts[attribute][value] = 1
    return attributes_counts


def create_wordcloud(task_id):
    # Get products from database
    products = list(jd_db[task_id].find())

    # Count word occurrences
    all_words = []
    for product in products:
        content = product.get('content', [])
        for c in content:
            for word in jieba.cut(c):
                if word not in stopwords and word != ' ':
                    all_words.append(word)

    word_counts = {}
    for word in all_words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    # Create wordcloud and save image to Redis
    wordcloud = WordCloud(font_path=font_path, background_color="white", width=800,
                          height=400).generate_from_frequencies(word_counts)
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    # plt.savefig(f"{task_id}_wordcloud")
    buf.seek(0)
    heatmap_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_wordcloud", heatmap_bytes)
    plt.close()


def analyze_attribute_bars(task_id):
    # Get products from database
    products = list(jd_db[task_id].find())
    # Count occurrences of attribute values
    attributes_counts = {}
    for product in products:
        for attribute, value in zip(product['name'], product['content']):
            if attribute not in attributes_counts:
                attributes_counts[attribute] = {}
            if isinstance(value, list):
                for v in value:
                    if v in attributes_counts[attribute]:
                        attributes_counts[attribute][v] += 1
                    else:
                        attributes_counts[attribute][v] = 1
            else:
                if value in attributes_counts[attribute]:
                    attributes_counts[attribute][value] += 1
                else:
                    attributes_counts[attribute][value] = 1

    # Create bar charts of top attribute values and save images to Redis
    for attribute, values in attributes_counts.items():
        if len(values) > 1:
            sorted_values = sorted(values.items(), key=lambda x: x[1], reverse=True)
            top_values = dict(sorted_values[:10])
            labels = list(top_values.keys())
            counts = list(top_values.values())
            plt.figure(figsize=(10, 6))
            plt.bar(labels, counts)
            plt.title(attribute)
            plt.xlabel('Value')
            plt.ylabel('Count')
            plt.xticks(rotation=45)
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            heatmap_bytes = buf.getvalue()
            buf.close()
            # Store the bytes in Redis
            redis_client.set(f"{task_id}_{attribute}_bar", heatmap_bytes)
            plt.close()


def run_jd_product_analyze(task_id):
    analyze_attributes(task_id)
    create_wordcloud(task_id)
    analyze_attribute_bars(task_id)
