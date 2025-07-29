import pandas as pd
from pathlib import Path

def extract_job_id(df:pd.DataFrame,url_column:str = 'url') -> pd.DataFrame:
    # lvk=gMIe8AQ66YrKWuI--JTexQ.--Nss0hYO6g
    df['job_id'] = df[url_column].str.extract(r"lvk=([^&]+)")
    return df

def deduplicate_jobs(df:pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values('days_ago',ascending=False)
    df = df.drop_duplicates(subset='job_id',keep='first')
    return df

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

    pd.set_option("display.max_columns",None)
    pd.set_option("display.max_colwidth",None)
    pd.set_option("display.max_rows",100)
    pd.set_option("display.expand_frame_repr",False)

    df = pd.read_csv(file_path)

    df = extract_job_id(df)
    df = deduplicate_jobs(df)
    df = drop_cols(df,['url','job_id'])

    df = shuffler(df)
    print(df.head(100))

if __name__ == "__main__":
    main()