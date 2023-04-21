import os

import jieba
import matplotlib.pyplot as plt
import io
from wordcloud import WordCloud

from app.db.weibo_db import db as weibo_db
from app.redis_client import redis_client

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文显示字体

# Get the absolute path of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Use the script directory to construct the path to the font file
font_path = os.path.join(script_dir, 'SimHei.ttf')
def generate_user_profile(task_id):
    collection = weibo_db[task_id]
    weibo_data = list(collection.find())
    # Extract relevant data from the Weibo data
    nickname = weibo_data[0]['nick_name']
    location = weibo_data[0]['location']
    followers_count = weibo_data[0]['followers_count']
    friends_count = weibo_data[0]['friends_count']
    statuses_count = weibo_data[0]['statuses_count']
    verified_type = weibo_data[0]['verified_type']
    verified_reason = weibo_data[0]['verified_reason']
    mbrank = weibo_data[0]['mbrank']
    mbtype = weibo_data[0]['mbtype']
    sunshine_credit = weibo_data[0]['sunshine_credit']
    label_desc = weibo_data[0]['label_desc']
    company = weibo_data[0]['company']
    education = weibo_data[0]['education']

    # Create a bar chart of label description distribution
    plt.figure(figsize=(8, 6))
    labels = []
    values = []
    for desc in label_desc:
        if '分' in desc:
            labels.append(desc.split(' ')[1])
            values.append(float(desc.split(' ')[2].replace('分', '')))
        else:
            labels.append(desc)
            values.append(1)
    plt.barh(labels, values)
    plt.title('微博标签描述分布')
    plt.xlabel('数量')
    buf = io.BytesIO()
    # plt.savefig(f"{task_id}label_desc_barchart.png")
    plt.savefig(buf, format='png')
    buf.seek(0)
    label_desc_barchart_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_label_desc_barchart", label_desc_barchart_bytes)
    plt.close()


    # concatenate the text from different fields
    # 将需要生成词云的文本合并成一个字符串
    text = ' '.join([data['nick_name'] + ' ' + data['location'] + ' ' + data['description'] + ' ' + data[
        'verified_reason'] + ' ' + data['birthday'] + ' ' + data['created_at'] + ' ' + data['desc_text'] + ' ' + data[
                         'ip_location'] + ' ' + data['sunshine_credit'] + ' '.join(data['label_desc']) + ' ' + data[
                         'company'] + ' ' + data['education']['school'] for data in weibo_data])

    # split text into words
    words = jieba.cut(text)

    # generate word frequency dictionary
    word_freq_dict = {}
    for word in words:
        if len(word) > 1:
            word_freq_dict[word] = word_freq_dict.get(word, 0) + 1

    wordcloud = WordCloud(background_color='white', font_path=font_path, max_words=2000)
    wordcloud.generate_from_frequencies(word_freq_dict)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title('用户画像')
    buf = io.BytesIO()
    # plt.savefig(f"{task_id}company_wordcloud.png")
    plt.savefig(buf, format='png')
    buf.seek(0)
    company_wordcloud_bytes = buf.getvalue()
    buf.close()
    redis_client.set(f"{task_id}_company_wordcloud", company_wordcloud_bytes)
    plt.close()

def run_weibo_user_analyze(task_id):
    generate_user_profile(task_id)

# run_weibo_user_analyze('fa963f68-3d23-422a-bc31-cf22e504eebf')