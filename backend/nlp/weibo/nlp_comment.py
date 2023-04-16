# import spacy
# from collections import Counter
# import spacy
#
# nlp = spacy.load("zh_core_web_sm")
#
# text = "她在北京工作，是一名软件工程师。"
# doc = nlp(text)
#
# # Tokenization
# for token in doc:
#     print(token.text)
#
# # Part-of-speech tagging
# for token in doc:
#     print(token.text, token.pos_)
#
# # Named entity recognition
# for ent in doc.ents:
#     print(ent.text, ent.label_)


# # Tokenization using jieba
# import jieba
#
# text = "我爱吃北京烤鸭"
# tokens = jieba.cut(text)
#
# for token in tokens:
#     print(token)
#
# # Part-of-speech tagging using jieba
# import jieba.posseg as pseg
#
# text = "我爱吃北京烤鸭"
# words = pseg.cut(text)
#
# for word, flag in words:
#     print(word, flag)
#
# # Named entity recognition using jieba
# import jieba
#
# text = "李白是唐代著名诗人"
# words = jieba.posseg.cut(text)
#
# for word, flag in words:
#     if flag == "nr":
#         print(word, "PERSON")
#
#
# from textblob import TextBlob
#
# text = "这个餐厅的食物很好吃"
# blob = TextBlob(text)
#
# if blob.sentiment.polarity > 0:
#     print("Positive sentiment")
# elif blob.sentiment.polarity < 0:
#     print("Negative sentiment")
# else:
#     print("Neutral sentiment")
#
#
# # Topic modeling using jieba
# import jieba.analyse
#
# text = "这是一段关于人工智能的文章。人工智能是未来的趋势，将会深刻改变我们的生活。"
# keywords = jieba.analyse.extract_tags(text, topK=3, withWeight=True)
#
# for keyword, weight in keywords:
#     print(keyword)
#
# # Text classification using TextBlob
# from textblob import TextBlob
#
# text = "这是一篇关于机器学习的文章"
# blob = TextBlob(text)
#
# if "机器学习" in blob.lower():
#     print("This is an article about machine learning")
# else:
#     print("This is not an article about machine learning")
#
#
# # Dependency parsing using jieba:
# import jieba
# from jieba import posseg
#
# text = "小明去上学，路上看到了一只小狗。"
# words = posseg.cut(text)
#
# for word, flag in words:
#     print(word, flag)


# # Text generation using OpenAI's GPT-3
# import openai
#
# openai.api_key = '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'
#
# prompt = "请根据以下提示写一篇科技类的短文：AI技术的发展现状及未来展望。"
#
# model = "text-davinci-003"
# response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=512)
#
# print(response.choices[0].text)


from ltp import LTP
ltp = LTP() # 默认加载 LTP/Small 模型