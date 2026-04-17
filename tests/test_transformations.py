import pytest
import pandas as pd
from pipeline.transformations import filter_rows

def test_filter_rows():
    # Sample DataFrame
    data = {
        'A': [1, 2, 3, 4],
        'B': [5, 6, 7, 8]
    }
    df = pd.DataFrame(data)

    # Condition: Filter rows where column 'A' > 2
    condition = lambda df: df['A'] > 2

    # Apply transformation
    result = filter_rows(df, condition)

    # Expected DataFrame
    expected_data = {
        'A': [3, 4],
        'B': [7, 8]
    }
    expected_df = pd.DataFrame(expected_data)

    # Assert
    pd.testing.assert_frame_equal(result, expected_df)