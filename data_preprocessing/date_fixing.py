import os
import pandas as pd
import re
from pathlib import Path

pd.set_option('display.max_columns',None)

# Start from the current script dir
script_dir = Path(__file__).resolve().parent
# Move up one level to the project root
project_root = script_dir.parent

clean_dir = project_root / "data"
# Build correct path
los_path = clean_dir / "raw" / "jobs_raw_zip_losangeles.csv"
new_york_path = clean_dir / "raw" / "jobs_raw_zip_newyork.csv"
remote_path = clean_dir / "raw" / "jobs_raw_zip_remote.csv"

#path to store the cleaned and merged data
all_output_path = clean_dir / "data_cleaned" / "fix_date_jobs.csv"
os.makedirs(os.path.dirname(all_output_path),exist_ok=True)

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

def load_and_clean(path,source_name):
    df = pd.read_csv(path)
    df['days_ago'] = df['post_date'].apply(extract_days_ago)
    df["source"] = source_name
    return df

los_df = load_and_clean(los_path,"los_angleles")
new_york_df = load_and_clean(new_york_path,"new_york")
remote_df = load_and_clean(remote_path,"remote")

#remove the old post_date
los_df = los_df.drop(columns=['post_date'])
new_york_df = new_york_df.drop(columns=['post_date'])
remote_df = remote_df.drop(columns=['post_date'])

all_job_df = pd.concat([los_df,new_york_df,remote_df],ignore_index=True)

print("---ALL---")
print(all_job_df)
print("=========")


all_job_df.to_csv(all_output_path,index = False)
print(f"Stored {len(all_job_df)}jobs in path : {all_output_path}")

"""
print("los dataframe")
print(los_df.head(10))
print("new_york dataframe")
print(new_york_df.head(10))
print("remote dataframe")
print(remote_df.head(10))"""