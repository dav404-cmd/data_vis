import pandas as pd
import re
from pathlib import Path

# Start from the current script dir
script_dir = Path(__file__).resolve().parent
print(f"script dir {script_dir}")
# Move up one level to the project root
project_root = script_dir.parent

# Build correct path
path = project_root / "data" / "raw" / "jobs_raw_zip_losangeles.csv"
print("Resolved path:", path)
# Load data
df = pd.read_csv(path)

# Assume scrape delay was 18 days
SCRAPE_DELAY_DAYS = 18

# Parse "Posted X days ago" into float (days ago + scrape delay)
def extract_days_ago(post_text):
    match = re.search(r'Posted (\d+) days ago', post_text)
    if match:
        return float(int(match.group(1)) + SCRAPE_DELAY_DAYS)
    return None

df['days_ago'] = df['post_date'].apply(extract_days_ago)

print(df.head(10))