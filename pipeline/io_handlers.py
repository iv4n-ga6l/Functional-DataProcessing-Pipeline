import pandas as pd
import xml.etree.ElementTree as ET
from io import StringIO

def read_xml(file_path: str) -> pd.DataFrame:
    """
    Reads an XML file and converts it into a pandas DataFrame.

    Args:
        file_path (str): Path to the XML file.

    Returns:
        pd.DataFrame: The parsed DataFrame.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    all_records = []
    for child in root:
        record = {elem.tag: elem.text for elem in child}
        all_records.append(record)

    return pd.DataFrame(all_records)

def write_xml(dataframe: pd.DataFrame, file_path: str):
    """
    Writes a pandas DataFrame to an XML file.

    Args:
        dataframe (pd.DataFrame): The DataFrame to write.
        file_path (str): Path to the output XML file.
    """
    root = ET.Element("root")

    for _, row in dataframe.iterrows():
        record = ET.SubElement(root, "record")
        for field, value in row.items():
            elem = ET.SubElement(record, field)
            elem.text = str(value)

    tree = ET.ElementTree(root)
    tree.write(file_path)