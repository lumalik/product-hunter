"""This script handles the upload of the data to huggingface datasets."""
import datasets
from datasets import Dataset
import os 
import pandas as pd 

data_path = "data"
filepath = os.path.join(data_path, "product_hunt_data.csv")
df = pd.read_csv(filepath)
dataset = Dataset.from_pandas(df)
dataset.push_to_hub("lumalik/Product-Hunt-Data")