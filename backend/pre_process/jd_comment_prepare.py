# from pyspark.sql import SparkSession
# from pyspark.sql.functions import udf
# from pyspark.sql.types import ArrayType, StringType
# from pyspark.ml.feature import HashingTF, IDF, Tokenizer, Word2Vec
# from pyspark.ml.linalg import Vectors
# from pyspark.ml.pipeline import Pipeline
# from pyspark.ml.feature import StringIndexer
# from pyspark.ml.feature import IndexToString
# from pyspark.ml import PipelineModel
# from elasticsearch import Elasticsearch
# import pymongo
# import re
# from pyspark.ml.feature import StopWordsRemover
# from spacy.lang.zh import STOP_WORDS
#
# from pre_process.config import es_hosts
#
# # 创建SparkSession
# spark = SparkSession.builder.appName("JDCommentProcessing").getOrCreate()
# mongo_database = "jd"
# mongo_collection = "87772ddb-2c6c-4ae9-9b15-790d82b61bb4"
# # MongoDB连接参数
# mongo_uri = "mongodb://localhost:27017/{}/{}".format(mongo_database, mongo_collection)
#
# # Elasticsearch连接参数
#
# es_index = "jd_comments"
# es_type = "comment"
#
# # MongoDB数据读取
# df = spark.read.format("com.mongodb.spark.sql.DefaultSource").option("uri", mongo_uri).load()
#
# # 数据清洗
# udf_remove_html_tags = udf(lambda content: re.sub(r'<[^>]+>', '', content), StringType())
# udf_remove_stop_words = udf(lambda words: [word for word in words if word not in STOP_WORDS], ArrayType(StringType()))
# tokenizer = Tokenizer(inputCol="content", outputCol="words")
# remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")
# df = df.withColumn("cleaned_content", udf_remove_html_tags(df.content))
# df = tokenizer.transform(df)
# df = remover.transform(df)
# df = df.withColumn("filtered_words", udf_remove_stop_words(df.filtered_words))
#
# # 特征提取
# hashing_tf = HashingTF(inputCol="filtered_words", outputCol="raw_features")
# idf = IDF(inputCol="raw_features", outputCol="features")
# word2vec = Word2Vec(inputCol="filtered_words", outputCol="w2v_features", vectorSize=100, minCount=1)
#
# # 数据转换
# indexer = StringIndexer(inputCol="name", outputCol="label")
# reverse_indexer = IndexToString(inputCol="prediction", outputCol="product_name", labels=indexer.labels)
#
# # 构建机器学习流水线
# pipeline = Pipeline(stages=[hashing_tf, idf, word2vec, indexer])
# model = pipeline.fit(df)
# df_transformed = model.transform(df)
# df_transformed = reverse_indexer.transform(df_transformed)
#
# # 将处理后的评价数据存储到Elasticsearch中
# es = Elasticsearch(es_hosts)
# es.indices.create(index=es_index, ignore=400)
# es_data = df_transformed.select("product_name", "w2v_features").rdd.map(lambda x: {"product_name": x[0], "w2v_features": Vectors.dense(x[1].toArray())})
# es_data.saveAsNewAPIHadoopFile(
#     path="-",
#     outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
#     keyClass="org.apache.hadoop.io.NullWritable",
#     valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
#     conf={
#         "es.nodes": ",".join(es_hosts),
#         "es.resource": "{}/{}".format(es_index, es_type),
#         "es.input.json": "yes",
#         "es.mapping.id": "product_name"
#     }
# )
