import pandas as pd
import re
from pathlib import Path

pd.set_option('display.max_columns',None)

# Start from the current script dir
script_dir = Path(__file__).resolve().parent
# Move up one level to the project root
project_root = script_dir.parent

# Build correct path
los_path = project_root / "data" / "raw" / "jobs_raw_zip_losangeles.csv"
new_york_path = project_root / "data" / "raw" / "jobs_raw_zip_newyork.csv"
remote_path = project_root / "data" / "raw" / "jobs_raw_zip_remote.csv"

print("Resolved path:", los_path)


# Assume collection delay was 18 days
SCRAPE_DELAY_DAYS = 19

# Parse "Posted X days ago" into float (days ago + scrape delay)
def extract_days_ago(post_text):
    match = re.search(r'Posted (\d+) days ago', post_text)
    match2 = re.search(r'Posted (\d+) hours ago', post_text)
    if match:
        return float(int(match.group(1)) + SCRAPE_DELAY_DAYS)
    if match2:
        return float(SCRAPE_DELAY_DAYS)
    return None

def load_and_clean(path):
    df = pd.read_csv(path)
    df['days_ago'] = df['post_date'].apply(extract_days_ago)
    return df

los_df = load_and_clean(los_path)
new_york_df = load_and_clean(new_york_path)
remote_df = load_and_clean(remote_path)

#remove the old post_date
los_df = los_df.drop(columns=['post_date'])
new_york_df = new_york_df.drop(columns=['post_date'])
remote_df = remote_df.drop(columns=['post_date'])



print("los dataframe")
print(los_df.head(10))
print("new_york dataframe")
print(new_york_df.head(10))
print("remote dataframe")
print(remote_df.head(10))