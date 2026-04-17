import pytest
import pandas as pd
from pipeline.transformations import filter_rows
from pipeline.io_handlers import read_xml, write_xml

def test_pipeline_edge_case_empty_file():
    # Test handling of an empty DataFrame
    empty_df = pd.DataFrame()

    # Apply a transformation
    condition = lambda df: df['A'] > 2 if 'A' in df.columns else pd.Series(dtype=bool)
    result = filter_rows(empty_df, condition)

    # Assert the result is still an empty DataFrame
    pd.testing.assert_frame_equal(result, empty_df)

def test_pipeline_integration():
    # Sample DataFrame
    data = {
        'A': [1, 2, 3, 4],
        'B': [5, 6, 7, 8]
    }
    df = pd.DataFrame(data)

    # Apply transformation
    condition = lambda df: df['A'] > 2
    filtered_df = filter_rows(df, condition)

    # Write to XML
    write_xml(filtered_df, 'test_pipeline_output.xml')

    # Read back the XML
    result_df = read_xml('test_pipeline_output.xml')

    # Expected DataFrame
    expected_data = {
        'A': ['3', '4'],
        'B': ['7', '8']
    }
    expected_df = pd.DataFrame(expected_data)

    # Assert
    pd.testing.assert_frame_equal(result_df, expected_df)

    # Cleanup
    import os
    os.remove('test_pipeline_output.xml')