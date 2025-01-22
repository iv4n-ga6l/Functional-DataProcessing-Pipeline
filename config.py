from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, List, Optional, Union
from pathlib import Path

class FileFormat(Enum):
    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"
    EXCEL = "excel"

@dataclass
class PipelineConfig:
    input_path: Union[str, Path]
    output_path: Union[str, Path]
    input_format: FileFormat
    output_format: FileFormat
    batch_size: int = 1000
    required_columns: Optional[List[str]] = None
    column_mappings: Optional[Dict[str, str]] = None
    filter_conditions: Optional[Dict[str, Any]] = None
    log_level: str = "INFO"
    log_file: Optional[str] = "pipeline.log"


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'secret-key'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class DevelopmentConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}