import pandas as pd
from pathlib import Path

def extract_job_id(df:pd.DataFrame,url_column:str = 'url') -> pd.DataFrame:
    # lvk=gMIe8AQ66YrKWuI--JTexQ.--Nss0hYO6g
    df['job_id'] = df[url_column].str.extract(r"lvk=([^&]+)")
    return df

def deduplicate_jobs(df:pd.DataFrame) -> pd.DataFrame:
    df.sort_values('days_ago',ascending=False)
    df.drop_duplicates(subset='job_id',keep='first')
    return df

def main():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    print(f"project root : {project_root}")

    data_dir = project_root / "data" / "data_cleaned"
    file_path = data_dir / "fix_date_jobs.csv"

    df = pd.read_csv(file_path)

    df = extract_job_id(df)
    df = deduplicate_jobs(df)

    print(df)

if __name__ == "__main__":
    main()