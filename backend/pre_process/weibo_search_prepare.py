import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt

# Connect to MongoDB and fetch data from the "task_id" collection
client = MongoClient()
db = client["weibo"]
task_id='2f40a5cc-bb8c-4faa-82e8-244b819901bc'
collection = db[task_id]
data = pd.DataFrame(list(collection.find()))
print(data)

# Convert created_at to datetime and set as index
data["created_at"] = pd.to_datetime(data["created_at"])
data.set_index("created_at", inplace=True)

# Count number of posts per day
daily_counts = data.resample("D").size()

# Plot daily post counts
fig, ax = plt.subplots()
daily_counts.plot(ax=ax, x="created_at", y="count", kind="bar")
ax.set_xlabel("Date")
ax.set_ylabel("Number of Posts")
plt.show()

# Compute average reposts, comments, and attitudes per post per day
daily_stats = data.resample("D").agg({"reposts_count": "mean", "comments_count": "mean", "attitudes_count": "mean"})

# Plot average reposts, comments, and attitudes per post per day
fig, ax = plt.subplots()
daily_stats.plot(ax=ax, y=["reposts_count", "comments_count", "attitudes_count"], kind="line")
ax.set_xlabel("Date")
ax.set_ylabel("Average Count per Post")
plt.show()

# Compute correlations between reposts, comments, and attitudes
corr = data[["reposts_count", "comments_count", "attitudes_count"]].corr()

# Plot correlation matrix
fig, ax = plt.subplots()
im = ax.imshow(corr, cmap="coolwarm")
ax.set_xticks(range(3))
ax.set_yticks(range(3))
ax.set_xticklabels(["Reposts", "Comments", "Attitudes"])
ax.set_yticklabels(["Reposts", "Comments", "Attitudes"])
for i in range(3):
    for j in range(3):
        text = ax.text(j, i, "{:.2f}".format(corr.iloc[i, j]), ha="center", va="center", color="black")
ax.set_title("Correlation Matrix")
fig.colorbar(im)
plt.show()