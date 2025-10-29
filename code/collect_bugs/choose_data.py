import pandas as pd
import random
from datetime import datetime

# Read the original CSV file
df = pd.read_csv('fdroid_data.csv', sep=',')

# Convert date strings to datetime objects
df['Last Updated'] = pd.to_datetime(df['Last Updated'], format='%d-%m-%y')

# Filter data after January 1, 2023
start_date = pd.to_datetime('2023-01-01')
filtered_df = df[df['Last Updated'] >= start_date]

# Check if filtered data is sufficient
if len(filtered_df) < 90:
    raise ValueError(f"Data after January 1, 2023 is less than 90 rows, currently {len(filtered_df)} rows")

# Randomly sample 90 rows
sample_df = filtered_df.sample(n=90, random_state=42)

# Convert date format back to original
sample_df['Last Updated'] = sample_df['Last Updated'].dt.strftime('%d-%m-%y')

# Save to a new CSV file
sample_df.to_csv('90.csv', index=False)