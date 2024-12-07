import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load the data
def load_data(file_path):
    return pd.read_csv(file_path)

# Step 2: Preprocess data
def preprocess_data(df):
    # Combine relevant features into a single string for each video
    df['combined_features'] = df['title'].astype(str) + ' ' + df['description'].astype(str)
    return df

# Step 3: Create a function to recommend similar videos
def recommend_videos(df, video_id, top_n=5):
    # Vectorize the combined features using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['combined_features'])
    
    # Calculate cosine similarity between videos
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    # Find the index of the input video
    video_index = df[df['video_id'] == video_id].index[0]
    
    # Get similarity scores for the input video
    sim_scores = list(enumerate(cosine_sim[video_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the top_n similar videos
    top_similar = sim_scores[1:top_n+1]  # Skip the first one as it's the video itself
    recommended_indices = [x[0] for x in top_similar]
    recommended_videos = df.iloc[recommended_indices]
    
    return recommended_videos[['video_id', 'title', 'channel_title', 'published_at', 'view_count']]

# Step 4: Run the recommendation system
if __name__ == "__main__":
    # Load data from CSV
    df = load_data('data/raw/trending_videos.csv')
    
    # Preprocess the data
    df = preprocess_data(df)
    
    # Recommend videos based on a given video ID
    video_id = 'PtutVHfyBx8'  # Replace with an example video ID
    recommendations = recommend_videos(df, video_id)
    
    # Display the recommendations
    print("Recommended Videos:")
    print(recommendations)
