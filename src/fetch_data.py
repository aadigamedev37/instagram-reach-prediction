import pandas as pd
import urllib.request
import os

os.makedirs('data/raw', exist_ok=True)
url = 'https://raw.githubusercontent.com/amankharwal/Website-data/master/instagram_reach.csv'
file_path = 'data/raw/instagram_reach.csv'

urllib.request.urlretrieve(url, file_path)
df = pd.read_csv(file_path)
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head())
