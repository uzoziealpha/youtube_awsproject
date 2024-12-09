from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
import pandas as pd

def train_model(data_file, model_output):
    # Load preprocessed data
    df = pd.read_csv(data_file)
    reader = Reader(rating_scale=(0, 1))
    data = Dataset.load_from_df(df[['user_id', 'video_id', 'rating']], reader)

    # Split data into train and test sets
    trainset, testset = train_test_split(data, test_size=0.25)

    # Train the SVD algorithm
    algo = SVD()
    algo.fit(trainset)

    # Evaluate model performance
    predictions = algo.test(testset)
    print("RMSE:", accuracy.rmse(predictions))

    # Save the trained model
    import joblib
    joblib.dump(algo, model_output)
    print(f"Model saved to {model_output}")

def recommend(user_id, video_id, model_path):
    # Load the trained model
    import joblib
    algo = joblib.load(model_path)

    # Make a prediction
    prediction = algo.predict(user_id, video_id)
    print(f"Predicted rating for user {user_id} and video {video_id}: {prediction.est}")

if __name__ == "__main__":
    train_model("data/processed_data.csv", "models/svd_model.pkl")
    recommend("user_123", "video_456", "models/svd_model.pkl")
