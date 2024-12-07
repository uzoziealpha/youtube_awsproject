import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the combined data
data_path = "data/processed/merged_user_video_data.csv"
try:
    df = pd.read_csv(data_path)
    print("Data loaded successfully.")
except Exception as e:
    print(f"Error loading data: {e}")

# Inspect the first few rows of the data
print(df.head())

# Check the data types and basic statistics
print(df.info())
print(df.describe())

# Visualization of views count distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['view_count'], bins=20, kde=True)
plt.title('Distribution of Video Views')
plt.xlabel('Views')
plt.ylabel('Frequency')
plt.show()

# Top 10 most liked videos
top_liked_videos = df.sort_values(by='like_count', ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x='title', y='like_count', data=top_liked_videos)
plt.title('Top 10 Most Liked Videos')
plt.xlabel('Video Title')
plt.ylabel('Like Count')
plt.xticks(rotation=90)
plt.show()

# Correlation heatmap (if numeric columns exist)
corr = df[['view_count', 'like_count', 'comment_count']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap between Views, Likes, and Comments')
plt.show()
