import pymongo
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['jd']
task_id = 'ed44f3ac-3a7d-4897-b05b-e59005dbba3b'
collection = db[task_id]
