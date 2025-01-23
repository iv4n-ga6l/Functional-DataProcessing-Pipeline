import csv
import json
import pandas as pd
from typing import List, Dict
from exceptions import IOError
from logger import log_execution_time

@log_execution_time
def write_csv(data: List[Dict], output_path: str):
    """Write data to CSV file"""
    try:
        if not data:
            return
        
        fieldnames = data[0].keys()
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        raise IOError(f"Error writing CSV file: {str(e)}")

@log_execution_time
def write_json(data: List[Dict], output_path: str):
    """Write data to JSON file"""
    try:
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        raise IOError(f"Error writing JSON file: {str(e)}")

@log_execution_time
def write_parquet(data: List[Dict], output_path: str):
    """Write data to Parquet file"""
    try:
        df = pd.DataFrame(data)
        df.to_parquet(output_path, index=False)
    except Exception as e:
        raise IOError(f"Error writing Parquet file: {str(e)}")

@log_execution_time
def write_excel(data: List[Dict], output_path: str):
    """Write data to Excel file"""
    try:
        df = pd.DataFrame(data)
        with pd.ExcelWriter(output_path) as writer:
            df.to_excel(writer, index=False)
    except Exception as e:
        raise IOError(f"Error writing Excel file: {str(e)}")