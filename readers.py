import csv
import json
import pandas as pd
from typing import List, Dict, Generator
from logger import log_execution_time

@log_execution_time
def read_csv(file_path: str, batch_size: int) -> Generator[List[Dict], None, None]:
    """Read CSV file in batches"""
    try:
        def batch_reader() -> Generator[List[Dict], None, None]:
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                batch = []
                for row in reader:
                    batch.append(row)
                    if len(batch) >= batch_size:
                        yield batch
                        batch = []
                if batch:
                    yield batch
        
        return batch_reader()
    except Exception as e:
        raise IOError(f"Error reading CSV file: {str(e)}")

@log_execution_time
def read_json(file_path: str, batch_size: int) -> Generator[List[Dict], None, None]:
    """Read JSON file in batches"""
    try:
        def batch_reader() -> Generator[List[Dict], None, None]:
            with open(file_path, 'r') as f:
                data = json.load(f)
                for i in range(0, len(data), batch_size):
                    yield data[i:i + batch_size]
        
        return batch_reader()
    except Exception as e:
        raise IOError(f"Error reading JSON file: {str(e)}")

@log_execution_time
def read_parquet(file_path: str, batch_size: int) -> Generator[List[Dict], None, None]:
    """Read Parquet file in batches"""
    try:
        def batch_reader() -> Generator[List[Dict], None, None]:
            df = pd.read_parquet(file_path)
            for i in range(0, len(df), batch_size):
                yield df.iloc[i:i + batch_size].to_dict('records')
        
        return batch_reader()
    except Exception as e:
        raise IOError(f"Error reading Parquet file: {str(e)}")

@log_execution_time
def read_excel(file_path: str, batch_size: int) -> Generator[List[Dict], None, None]:
    """Read Excel file in batches"""
    try:
        def batch_reader() -> Generator[List[Dict], None, None]:
            df = pd.read_excel(file_path)
            for i in range(0, len(df), batch_size):
                yield df.iloc[i:i + batch_size].to_dict('records')
        
        return batch_reader()
    except Exception as e:
        raise IOError(f"Error reading Excel file: {str(e)}")
