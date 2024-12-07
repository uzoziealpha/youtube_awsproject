import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the merged user and video data
data_path = "data/processed/merged_user_video_data.csv"
try:
    df = pd.read_csv(data_path)
    print("Data loaded successfully.")
except Exception as e:
    print(f"Error loading data: {e}")

# Preprocessing the data
def preprocess_data(df):
    # Fill missing values directly
    df['view_count'] = df['view_count'].fillna(df['view_count'].mean())
    df['like_count'] = df['like_count'].fillna(df['like_count'].mean())
    df['category_id'] = df['category_id'].fillna(df['category_id'].mode()[0])
    df['description'] = df['description'].fillna("")  # Handle missing description
    
    return df

# Feature Engineering: Textual data from description and numeric data (view_count, like_count)
def feature_engineering(df):
    # TF-IDF Vectorizer for the 'description' column (to handle text-based features)
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['description'])
    
    # Combine numerical features (view_count and like_count) with TF-IDF matrix
    numeric_features = df[['view_count', 'like_count']].values
    return tfidf_matrix, numeric_features

# Recommendation Model using Cosine Similarity
def build_recommendation_system(df):
    tfidf_matrix, numeric_features = feature_engineering(df)

    # Compute cosine similarity for the description (TF-IDF)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Normalize the cosine similarity matrix by including view_count and like_count
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
    recommended_video_ids = set()  # To track already recommended video IDs
    for idx, score in recommended_videos:
        video_id = df.iloc[idx]["video_id"]
        
        # Skip if video_id is already recommended
        if video_id not in recommended_video_ids:
            recommendations.append({
                "video_id": video_id,
                "title": df.iloc[idx]["title"],
                "similarity_score": score
            })
            recommended_video_ids.add(video_id)
    
    return recommendations

# Testing the recommendation system
def test_recommendation_system():
    try:
        df = preprocess_data(pd.read_csv(data_path))
    
        # Choose a sample video index (e.g., 0, you can change it to test other videos)
        video_index = 0
        print(f"Recommendations for Video: {df.iloc[video_index]['title']}")
        
        recommendations = get_recommendations(df, video_index, num_recommendations=10)
        
        # Convert the recommendations to a DataFrame and save as CSV
        recommendations_df = pd.DataFrame(recommendations)
        recommendations_df.to_csv('data/processed/recommendations.csv', index=False)
        print("Recommendations saved to 'data/processed/recommendations.csv'.")
        
        # Print recommendations
        for rec in recommendations:
            print(f"Recommended Video: {rec['title'].encode('utf-8', 'ignore').decode('utf-8')}, Similarity Score: {rec['similarity_score']}")
    
    except Exception as e:
        print(f"Error in recommendation system: {e}")

if __name__ == "__main__":
    test_recommendation_system()
