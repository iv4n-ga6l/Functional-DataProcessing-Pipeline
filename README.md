# Functional Data Processing Pipeline

This project is a data processing pipeline written in Python that reads data from a CSV file, transforms it, and writes the results to various formats(CSV|JSON|PARQUET|EXCEL) files. 


## Install
```bash
pip install -r requirements.txt
```

## Usage
1. **Ensure `input.csv` exists and is properly formatted.**
2. **Run the pipeline:**
```python
config = PipelineConfig(
    input_path=INPUT_PATH,
    output_path=OUTPUT_PATH,
    input_format=INPUT_FILE_FORMAT,
    output_format=OUTPUT_FILE_FORMAT,
    batch_size=BATH_NUMBER,
    required_columns=[REQUIRED_COLUMNS],
    column_mappings={
        // Column renaming, key : value
    },
    filter_conditions={
        // filter conditions, key : value
    }
)
```

```bash
python main.py
```

**Run the tests:**
```bash
pytest tests/ -v
```
