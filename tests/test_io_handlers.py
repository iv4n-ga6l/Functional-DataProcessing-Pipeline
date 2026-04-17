import pytest
import pandas as pd
from pipeline.io_handlers import read_xml, write_xml
import os

def test_read_xml():
    # Sample XML content
    xml_content = """<root>
    <record><A>1</A><B>5</B></record>
    <record><A>2</A><B>6</B></record>
    </root>"""

    # Write to a temporary file
    with open('test.xml', 'w') as f:
        f.write(xml_content)

    # Read XML
    df = read_xml('test.xml')

    # Expected DataFrame
    expected_data = {
        'A': ['1', '2'],
        'B': ['5', '6']
    }
    expected_df = pd.DataFrame(expected_data)

    # Assert
    pd.testing.assert_frame_equal(df, expected_df)

    # Cleanup
    os.remove('test.xml')

def test_write_xml():
    # Sample DataFrame
    data = {
        'A': [1, 2],
        'B': [5, 6]
    }
    df = pd.DataFrame(data)

    # Write XML
    write_xml(df, 'test_output.xml')

    # Read back the file
    with open('test_output.xml', 'r') as f:
        content = f.read()

    # Expected XML content
    expected_content = """<root><record><A>1</A><B>5</B></record><record><A>2</A><B>6</B></record></root>"""

    # Assert
    assert content.replace('\n', '').replace(' ', '') == expected_content.replace('\n', '').replace(' ', '')

    # Cleanup
    os.remove('test_output.xml')