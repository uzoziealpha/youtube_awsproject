import os
import sys

# Dynamically add the project root directory to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Print the sys.path for debugging
print("Updated sys.path:")
for path in sys.path:
    print(path)

# Import modules from src
from src.data_preprocessing import preprocess_data
from src.recommendation import train_model, recommend

# Sample data to process (replace this with your actual data)
data = "raw data"

# Call the preprocessing function
processed_data = preprocess_data(data)
print("Data after preprocessing:", processed_data)

# Train the model
model = train_model(processed_data)
print("Model:", model)

# Make recommendations
recommendations = recommend(model, processed_data)
print("Recommendations:", recommendations)
