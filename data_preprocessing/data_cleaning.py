import pandas as pd
import numpy as np
import re
import os
from pathlib import Path

def extract_job_id(df:pd.DataFrame,url_column:str = 'url') -> pd.DataFrame:
    # lvk=gMIe8AQ66YrKWuI--JTexQ.--Nss0hYO6g
    df['job_id'] = df[url_column].str.extract(r"lvk=([^&]+)")
    return df

def deduplicate_jobs(df:pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values('days_ago',ascending=False)
    df = df.drop_duplicates(subset='job_id',keep='first')
    return df

def parse_salary(salary_str):
    if pd.isna(salary_str):
        return np.nan

    salary_str = salary_str.replace(',', '').replace('$', '').strip()

    is_hourly = '/ hr' in salary_str
    is_daily = '/ day' in salary_str
    is_weekly = '/ wk' in salary_str
    is_monthly = '/ mo' in salary_str

    # Remove unit ;output = 150K - 170K
    salary_str = re.sub(r'\s*/\s*(hr|day|yr|wk|mo)', '', salary_str)
    # Extract numbers ;output = ['150', '170']
    nums = re.findall(r'(\d+\.?\d*)K?', salary_str)

    # Convert K to thousands
    nums = [float(n) * 1000 if 'K' in part else float(n)
            for n, part in zip(nums, re.findall(r'\d+\.?\d*[K]?', salary_str))]

    if not nums:
        return np.nan

    avg = sum(nums) / len(nums)

    if is_hourly:
        return avg * 2080  # assume full-time hours/year ; 40hr/week * 52 weeks
    elif is_daily:
        return avg * 260   # assume 5 days/week * 52 weeks
    elif is_weekly:
        return avg * 52    # 52 wk/yr
    elif is_monthly:
        return avg * 12    # 12 mo/yr
    else:
        return avg         # assume fixed

def clean_salary_column(df: pd.DataFrame, column: str = 'salary') -> pd.DataFrame:
    df['salary_usd_yearly_avg'] = df[column].apply(parse_salary)
    return df

def fill_missing_salary(df: pd.DataFrame) -> pd.DataFrame:
    #fill salary nan with location based avg,fallback to global avg if it's not available
    location_salary_avg = df.groupby('location')['salary_usd_yearly_avg'].median()
    global_avg = df['salary_usd_yearly_avg'].median()
    #if location avg available fill missing salary; else keep original value.
    df['salary_filled'] = df.apply(lambda row: location_salary_avg[row['location']]
    if pd.isna(row['salary_usd_yearly_avg']) and row['location'] in location_salary_avg
    else row ['salary_usd_yearly_avg'],
    axis= 1)
    # fill remaining nans with global avg
    df['salary_filled'] = df['salary_filled'].fillna(global_avg)
    return df

#helpers

def remove_outliers(df:pd.DataFrame,col:str) -> pd.DataFrame:
    # remove extreme outliers .
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    return df[(df[col] >= lower) & (df[col] <= upper)].copy()

def drop_cols(df:pd.DataFrame,cols:list ) -> pd.DataFrame:
    return df.drop(columns=cols)

def shuffler(df:pd.DataFrame) -> pd.DataFrame:
    return df.sample(frac=1).reset_index(drop= True)

def main():

    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    print(f"project root : {project_root}")

    data_dir = project_root / "data" / "data_cleaned"
    file_path = data_dir / "fix_date_jobs.csv"
    output_path = data_dir / "processed_data.csv"
    os.makedirs(os.path.dirname(output_path),exist_ok=True)

    pd.set_option("display.max_columns",None)
    pd.set_option("display.max_colwidth",None)
    pd.set_option("display.max_rows",100)
    pd.set_option("display.expand_frame_repr",False)
    pd.options.display.float_format = '{:.2f}'.format

    df = pd.read_csv(file_path)
    df = extract_job_id(df)
    df = deduplicate_jobs(df)
    df = drop_cols(df,['url','job_id'])
    df = shuffler(df)
    df = clean_salary_column(df)
    df = drop_cols(df,['salary','source'])
    df = remove_outliers(df,'salary_usd_yearly_avg')
    df = fill_missing_salary(df)

    global_avg = df['salary_usd_yearly_avg'].mean()
    print(f"global_avg : {global_avg}")
    print(df.head(100))

    df.to_csv(output_path,index=False)

if __name__ == "__main__":
    main()