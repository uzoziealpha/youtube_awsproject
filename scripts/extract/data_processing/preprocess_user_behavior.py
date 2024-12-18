import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def preprocess_user_behavior(data_path, output_path):
    """
    Preprocess user behavior data: handle missing values, normalize, and scale features.

    Args:
        data_path (str): Path to the user behavior data CSV file.
        output_path (str): Path to save the preprocessed user behavior data.
    """
    try:
        # Load the user behavior data
        df = pd.read_csv(data_path)
        print("User behavior data loaded successfully.")
        if df.empty:
            raise ValueError("User behavior data file is empty.")
        print(f"Columns available in the dataset: {df.columns.tolist()}")

        # Convert percentage columns to numeric by removing the '%' and handling errors
        percentage_columns = ['watch_time', 'average_view_duration', 'CTR', 'audience_retention']
        for col in percentage_columns:
            if col in df.columns:
                # Convert the column to strings first, then replace '%' and convert to numeric
                df[col] = pd.to_numeric(df[col].astype(str).str.replace('%', ''), errors='coerce')

        # Fill missing values with the median for numeric columns
        numeric_cols = ['watch_time', 'average_view_duration', 'likes', 'dislikes',
                        'comments', 'CTR', 'shares', 'audience_retention']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())

        # Normalize and scale features
        scaler = MinMaxScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

        # Save the preprocessed data
        df.to_csv(output_path, index=False)
        print("Preprocessed data saved to", output_path)

        print("User behavior data preprocessing completed.")
        return df

    except Exception as e:
        print(f"Error preprocessing user behavior data: {e}")
        return None

# Example usage of the function
if __name__ == "__main__":
    data_path = 'data/raw/user_behavior_data.csv'  # Path to raw data
    output_path = 'data/processed/preprocessed_user_behavior_data.csv'  # Path to save preprocessed data

    preprocess_user_behavior(data_path, output_path)
