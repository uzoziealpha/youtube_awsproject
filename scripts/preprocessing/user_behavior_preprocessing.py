import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def preprocess_user_behavior(data_path, save_path):
    """
    Preprocess user behavior data: handle missing values, normalize, and scale features.

    Args:
        data_path (str): Path to the user behavior data CSV file.
        save_path (str): Path to save the preprocessed user behavior data.

    Returns:
        pd.DataFrame: Preprocessed user behavior DataFrame.
    """
    try:
        # Load the user behavior data
        df = pd.read_csv(data_path)
        print("User behavior data loaded successfully.")
        
        # Display the columns
        print(f"Columns available in the dataset: {df.columns.tolist()}")

        # Handle missing values
        numeric_cols = ['watch_time', 'average_view_duration', 'likes', 'dislikes',
                        'comments', 'CTR', 'shares', 'audience_retention']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())

        # Normalize and scale features
        scaler = MinMaxScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

        # Save the preprocessed data
        df.to_csv(save_path, index=False)
        print(f"Preprocessed data saved to {save_path}")

        print("User behavior data preprocessing completed.")
        return df

    except Exception as e:
        print(f"Error preprocessing user behavior data: {e}")
        return None

# Example usage
if __name__ == "__main__":
    data_path = "data/processed/user_behavior_data.csv"
    save_path = "data/processed/preprocessed_user_behavior_data.csv"
    preprocess_user_behavior(data_path, save_path)
