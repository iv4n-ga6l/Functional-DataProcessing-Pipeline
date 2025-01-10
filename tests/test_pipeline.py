import csv
import pytest
import tempfile
import json
from config import PipelineConfig, FileFormat
from pipeline import DataPipeline
import transformers as t
from exceptions import DataValidationError, PipelineError

@pytest.fixture
def sample_data():
    return [
        {"id": 1, "name": "John Doe", "age": 30, "salary": 50000},
        {"id": 2, "name": "Jane Smith", "age": 25, "salary": 60000},
        {"id": 3, "name": "Bob Johnson", "age": 35, "salary": 70000}
    ]

@pytest.fixture
def temp_files():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as input_file, \
         tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as output_file:
        yield input_file.name, output_file.name

def test_clean_column_names():
    data = [{"First Name": "John", "Last-Name": "Doe"}]
    result = t.clean_column_names(data)
    assert "first_name" in result[0]
    assert "last_name" in result[0]

def test_filter_rows():
    data = [
        {"status": "active", "value": 1},
        {"status": "inactive", "value": 2}
    ]
    result = t.filter_rows(data, {"status": "active"})
    assert len(result) == 1
    assert result[0]["value"] == 1

def test_validate_data():
    data = [{"column1": "value"}]
    with pytest.raises(DataValidationError):
        t.validate_data(data, ["column2"])

def test_pipeline_execution(temp_files, sample_data):
    input_file, output_file = temp_files
    
    # Write sample data to input file
    with open(input_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=sample_data[0].keys())
        writer.writeheader()
        writer.writerows(sample_data)
    
    # Configure pipeline
    config = PipelineConfig(
        input_path=input_file,
        output_path=output_file,
        input_format=FileFormat.CSV,
        output_format=FileFormat.JSON,
        batch_size=2,
        required_columns=["id", "name", "age"],
        column_mappings={"name": "full_name"},
        # filter_conditions={"age": 30},
        log_level="INFO"
    )
    
    # Execute pipeline
    pipeline = DataPipeline(config)
    result = pipeline.process()
    
    # Verify results
    print(f"Result: {result}")
    assert len(result) == 3 
    assert result[0]["full_name"] == "John Doe"
    
    # Verify output file
    with open(output_file, 'r') as f:
        output_data = json.load(f)
        assert len(output_data) == 3
        assert output_data[0]["full_name"] == "John Doe"

def test_handle_missing_values():
    data = [
        {"id": 1, "value": 10, "category": "A"},
        {"id": 2, "value": None, "category": "B"},
        {"id": 3, "value": 20, "category": None}
    ]
    
    strategy = {
        "value": "mean",
        "category": "unknown"
    }
    
    result = t.handle_missing_values(data, strategy)
    assert result[1]["value"] == 15  # mean of 10 and 20
    assert result[2]["category"] == "unknown"

def test_normalize_numeric_columns():
    data = [
        {"id": 1, "value": 10, "text": "a"},
        {"id": 2, "value": 20, "text": "b"},
        {"id": 3, "value": 30, "text": "c"}
    ]
    
    result = t.normalize_numeric_columns(data, ["value"])
    assert result[0]["value"] == 0.0
    assert result[1]["value"] == 0.5
    assert result[2]["value"] == 1.0
    assert result[0]["text"] == "a"  # Non-numeric columns unchanged

def test_add_computed_columns():
    data = [
        {"value1": 10, "value2": 20},
        {"value1": 30, "value2": 40}
    ]
    
    computations = {
        "sum": lambda row: row["value1"] + row["value2"],
        "product": lambda row: row["value1"] * row["value2"]
    }
    
    result = t.add_computed_columns(data, computations)
    assert result[0]["sum"] == 30
    assert result[0]["product"] == 200
    assert result[1]["sum"] == 70
    assert result[1]["product"] == 1200

def test_pipeline_with_different_formats(temp_files):
    input_file, output_file = temp_files
    
    sample_data = [
        {"id": 1, "name": "John Doe", "age": 30},
        {"id": 2, "name": "Jane Smith", "age": 25}
    ]
    
    with open(input_file, 'w') as f:
        json.dump(sample_data, f)
    
    # Configure pipeline
    config = PipelineConfig(
        input_path=input_file,
        output_path=output_file,
        input_format=FileFormat.JSON,
        output_format=FileFormat.CSV,
        batch_size=2,
        required_columns=["id", "name", "age"],
        column_mappings={"name": "full_name"},
        log_level="INFO"
    )
    
    # Execute pipeline
    pipeline = DataPipeline(config)
    result = pipeline.process()
    
    # Verify results
    assert len(result) == 2
    assert result[0]["full_name"] == "John Doe"
    
    # Verify output file
    with open(output_file, 'r') as f:
        output_data = list(csv.DictReader(f))
        assert len(output_data) == 2
        assert output_data[0]["full_name"] == "John Doe"

def test_error_handling():
    # Test with non-existent file
    config = PipelineConfig(
        input_path="nonexistent.csv",
        output_path="output.json",
        input_format=FileFormat.CSV,
        output_format=FileFormat.JSON,
        batch_size=2
    )
    
    pipeline = DataPipeline(config)
    with pytest.raises(PipelineError):
        pipeline.process()