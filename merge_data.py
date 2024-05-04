"""This script takes the data verified_products.csv and merges it with the data from producthunt_scraper.py  - {year}_producthunt.csv files."""
import pandas as pd
import os 

# load verified products.csv
data_path = "data"
filepath = os.path.join(data_path, "verified_products.csv")
verified_products = pd.read_csv(filepath)

# List of years to iterate over
years = [2015, 2016, 2017, 2018, 2019]

# List to store individual DataFrames
dataframes = []

# Iterate over each year and read the corresponding CSV file
for year in years:
    filepath = os.path.join(data_path, f"{year}_producthunt.csv")
    df = pd.read_csv(filepath)
    df['year'] = year
    dataframes.append(df)

# Concatenate all the individual DataFrames into a single DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)

# Merge the dataframes on the common column 'external_link'
merged_df = pd.merge(combined_df, verified_products, left_on='external_link', right_on='producthunt_url', how='left')

# Drop the 'producthunt_url' column as it is no longer needed
merged_df.drop('producthunt_url', axis=1, inplace=True)

# Save the merged dataframe to a new CSV file
merged_df.to_csv(os.path.join(data_path, "product_hunt_data.csv"), index=False)
