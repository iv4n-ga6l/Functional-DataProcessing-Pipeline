# Functional Data Processing Pipeline

This project is a functional data processing pipeline written in Python. It supports reading, transforming, and writing data in various formats, including CSV, JSON, Parquet, Excel, and now XML.

![app](dataprocessing.png)

## Features

- **Input Formats**: CSV, JSON, Parquet, Excel, XML
- **Output Formats**: CSV, JSON, Parquet, Excel, XML
- **Transformations**:
  - Filter rows based on custom conditions

## New Features

- **XML Support**: The pipeline now supports reading from and writing to XML files.
- **Row Filtering Transformation**: A new transformation function allows filtering rows based on user-defined conditions.
- **Logging**: A logging utility has been added to track the pipeline's execution steps.

## Usage

### Reading and Writing XML

```python
from pipeline.io_handlers import read_xml, write_xml

# Read XML
df = read_xml('input.xml')

# Write XML
write_xml(df, 'output.xml')
```

### Filtering Rows

```python
from pipeline.transformations import filter_rows

# Sample DataFrame
data = {
    'A': [1, 2, 3, 4],
    'B': [5, 6, 7, 8]
}
df = pd.DataFrame(data)

# Filter rows where column 'A' > 2
filtered_df = filter_rows(df, lambda df: df['A'] > 2)
```

## Testing

Run the tests using `pytest`:

```bash
pytest tests/
```