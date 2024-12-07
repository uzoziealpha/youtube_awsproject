import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Path to the user behavior data
user_behavior_data_path = 'data/processed/user_behavior_data.csv'

# Function to load user behavior data with error handling
def load_user_behavior_data(file_path):
    try:
        # Load CSV data
        df = pd.read_csv(file_path)
        
        # Check if the DataFrame is empty
        if df.empty:
            raise ValueError("The CSV file is empty.")
        
        print("User behavior data loaded successfully.")
        print("Columns available in the dataset:", df.columns.tolist())
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}. Please check the file path.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{file_path}' is empty.")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"Error loading data: {e}")

# Preprocessing the data
def preprocess_data(df):
    # Fill missing values directly
    df['watch_time'] = df['watch_time'].fillna(df['watch_time'].mean())
    df['average_view_duration'] = df['average_view_duration'].fillna(df['average_view_duration'].mean())
    df['likes'] = df['likes'].fillna(0)
    df['dislikes'] = df['dislikes'].fillna(0)
    df['comments'] = df['comments'].fillna(0)
    df['CTR'] = df['CTR'].fillna(0)
    df['shares'] = df['shares'].fillna(0)
    df['device_type'] = df['device_type'].fillna('Unknown')
    df['traffic_source'] = df['traffic_source'].fillna('Unknown')
    df['audience_retention'] = df['audience_retention'].fillna('0%')
    
    return df

# Feature Engineering: Textual data from description and numeric data (view_count, like_count)
def feature_engineering(df):
    # TF-IDF Vectorizer for the 'title' column (to handle text-based features)
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['title'])
    
    # Combine numerical features (watch_time, average_view_duration, likes, dislikes, etc.)
    numeric_features = df[['watch_time', 'average_view_duration', 'likes', 'dislikes', 'comments', 'CTR', 'shares']].values
    return tfidf_matrix, numeric_features

# Recommendation Model using Cosine Similarity
def build_recommendation_system(df):
    tfidf_matrix, numeric_features = feature_engineering(df)

    # Compute cosine similarity for the title (TF-IDF)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Normalize the numeric features using cosine similarity
    numeric_sim = cosine_similarity(numeric_features, numeric_features)

    # Combine both similarities
    combined_sim = (cosine_sim + numeric_sim) / 2  # Adjust the weight as necessary

    return combined_sim

# Get recommendations based on a video index
def get_recommendations(df, video_index, num_recommendations=10):
    combined_sim = build_recommendation_system(df)
    
    # Get similarity scores for the given video
    similarity_scores = list(enumerate(combined_sim[video_index]))
    
    # Sort the videos by similarity scores
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    # Get the top recommended videos (excluding the video itself)
    recommended_videos = sorted_scores[1:num_recommendations+1]
    
    recommendations = []
    for idx, score in recommended_videos:
        recommendations.append({
            "video_id": df.iloc[idx]["video_id"],
            "title": df.iloc[idx]["title"],
            "similarity_score": score
        })
    
    return recommendations

# Testing the recommendation system
def test_recommendation_system():
    df = load_user_behavior_data(user_behavior_data_path)
    
    if df is not None:
        df = preprocess_data(df)
        
        # Choose a sample video index (e.g., 0, you can change it to test other videos)
        video_index = 0
        print(f"Recommendations for Video: {df.iloc[video_index]['title']}")
        
        recommendations = get_recommendations(df, video_index, num_recommendations=10)
        
        for rec in recommendations:
            try:
                print(f"Recommended Video: {rec['title']}, Similarity Score: {rec['similarity_score']}")
            except UnicodeEncodeError:
                print(f"Recommended Video: {rec['title'].encode('utf-8', 'ignore').decode('utf-8')}, Similarity Score: {rec['similarity_score']}")

if __name__ == "__main__":
    test_recommendation_system()
