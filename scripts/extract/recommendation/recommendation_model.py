import pandas as pd
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split, accuracy

# Load the merged data from CSV
merged_data_path = 'data/processed/merged_data.csv'
merged_data = pd.read_csv(merged_data_path)

# Check if the merged data was loaded correctly
if merged_data is None or merged_data.empty:
    raise ValueError("Merged data is empty or not loaded correctly.")

# Create an interaction matrix
# Here, using 'watch_time' as the interaction score, adjust as necessary
merged_data['interaction_score'] = merged_data['watch_time']

# Prepare data for the 'surprise' library
interaction_data = merged_data[['user_id', 'video_id', 'interaction_score']]
reader = Reader(rating_scale=(0, 100))  # Adjust scale based on your data range
data = Dataset.load_from_df(interaction_data, reader)

# Train-test split
trainset, testset = train_test_split(data, test_size=0.2)

# Collaborative filtering model using SVD (Singular Value Decomposition)
model = SVD()
model.fit(trainset)

# Make predictions and evaluate the model
predictions = model.test(testset)
rmse = accuracy.rmse(predictions)
print(f"RMSE of the collaborative filtering model: {rmse:.2f}")

# Example prediction: estimating interaction score for a user and video pair
predicted_score = model.predict('user123', 'abc123')
print(f"Predicted interaction score for user123 and video abc123: {predicted_score.est:.2f}")
