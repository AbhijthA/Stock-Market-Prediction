import requests
import csv
import pandas as pd

# Replace this with the actual scrip-id (e.g., NSE or BSE stock symbol)

url = f"https://indian-stock-exchange-api2.p.rapidapi.com/historical_data?stock_name=tcs&period=1m&filter=price"


headers = {
    'x-rapidapi-host' : 'indian-stock-exchange-api2.p.rapidapi.com',
    'x-rapidapi-key': '52f4be9546msh12730cac5041cdcp1d5436jsn2c757c217d45' 
}

response = requests.get(url, headers=headers)

# Parse response
try:
    data = response.json()
except Exception as e:
    print("Failed to parse JSON:", e)
    print("Raw response:", response.text)
    exit()

# Preview data structure
print("Sample data:", data)

data = response.json()

# Extract datasets
datasets = data['datasets']

# Initialize dictionary for DataFrames
dfs = {}

# Loop through each dataset and create a DataFrame
for dataset in datasets:
    metric = dataset['metric']
    values = dataset['values']

    # Handle Volume with nested delivery info
    if metric == 'Volume':
        dates, volumes, delivery = [], [], []
        for entry in values:
            dates.append(entry[0])
            volumes.append(entry[1])
            delivery.append(entry[2].get('delivery') if isinstance(entry[2], dict) else None)
        df = pd.DataFrame({
            'Date': dates,
            'Volume': volumes,
            'Delivery %': delivery
        })
    else:
        df = pd.DataFrame(values, columns=['Date', metric])

    # Convert date column to datetime for merging
    df['Date'] = pd.to_datetime(df['Date'])
    dfs[metric] = df

# Merge all DataFrames on 'Date'
from functools import reduce
merged_df = reduce(lambda left, right: pd.merge(left, right, on='Date', how='outer'), dfs.values())

# Sort by Date
merged_df.sort_values('Date', inplace=True)

# Save to CSV
merged_df.to_csv('tcs_stock_data.csv', index=False)
print("✅ Data saved to 'tcs_stock_data.csv'")


