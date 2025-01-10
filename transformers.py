from typing import Dict, List, Any, Union, Callable
from exceptions import DataValidationError

def validate_data(data: List[Dict], required_columns: List[str]) -> List[Dict]:
    """Validate data structure and required columns"""
    missing_columns = [
        col for col in required_columns 
        if not all(col in row for row in data)
    ]
    if missing_columns:
        raise DataValidationError(
            f"Missing required columns: {missing_columns}"
        )
    return data

def clean_column_names(data: List[Dict]) -> List[Dict]:
    """Clean column names by removing spaces and special characters"""
    return [
        {k.lower().replace(' ', '_').replace('-', '_'): v 
         for k, v in row.items()}
        for row in data
    ]

def apply_column_mappings(data: List[Dict], mappings: Dict[str, str]) -> List[Dict]:
    """Rename columns based on provided mappings"""
    if not mappings:
        return data
    return [
        {mappings.get(k, k): v for k, v in row.items()}
        for row in data
    ]

def filter_rows(data: List[Dict], conditions: Dict[str, Any]) -> List[Dict]:
    """Filter rows based on conditions"""
    if not conditions:
        return data
    
    def meets_conditions(row):
        return all(
            row.get(col) == value 
            for col, value in conditions.items()
        )
    
    return [row for row in data if meets_conditions(row)]

def handle_missing_values(
    data: List[Dict],
    strategy: Dict[str, Union[str, int, float]]
) -> List[Dict]:
    """Handle missing values using different strategies"""
    def apply_strategy(value, col, strategy_type):
        if value is None or (isinstance(value, str) and not value.strip()):
            if strategy_type == "mean":
                values = [row[col] for row in data if row[col] is not None]
                return sum(values) / len(values)
            elif strategy_type == "mode":
                values = [row[col] for row in data if row[col] is not None]
                return max(set(values), key=values.count)
            else:
                return strategy_type
        return value

    return [
        {col: apply_strategy(val, col, strategy.get(col, val))
         for col, val in row.items()}
        for row in data
    ]

def add_computed_columns(
    data: List[Dict],
    computations: Dict[str, Callable]
) -> List[Dict]:
    """Add new columns based on computed values"""
    return [
        {**row, **{name: func(row) for name, func in computations.items()}}
        for row in data
    ]

def normalize_numeric_columns(
    data: List[Dict],
    columns: List[str]
) -> List[Dict]:
    """Normalize numeric columns to range [0,1]"""
    if not columns:
        return data
    
    # Calculate min and max for each column
    mins = {col: min(row[col] for row in data) for col in columns}
    maxs = {col: max(row[col] for row in data) for col in columns}
    
    def normalize(value, col):
        if col in columns:
            return (value - mins[col]) / (maxs[col] - mins[col])
        return value
    
    return [
        {col: normalize(val, col) for col, val in row.items()}
        for row in data
    ]
