from config import FileFormat, PipelineConfig
from pipeline import DataPipeline
from pycache_handler.handler import py_cache_handler

@py_cache_handler
def main():
    config = PipelineConfig(
        input_path='input.csv',
        output_path='output.json',
        input_format=FileFormat.CSV,
        output_format=FileFormat.JSON,
        batch_size=1000,
        required_columns=['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked'],
        column_mappings={
            'survived': 'has_survived'
        },
        filter_conditions={
            'embarked': 'C'
        }
    )
    
    pipeline = DataPipeline(config)
    pipeline.process()

if __name__ == "__main__":
    main()