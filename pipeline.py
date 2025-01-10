import transformers as t
import readers as r
import writers as w
from config import PipelineConfig, FileFormat
from logger import log_execution_time, setup_logger
from exceptions import PipelineError

class DataPipeline:
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.logger = setup_logger(config.log_level, config.log_file)
        
    def _get_reader(self):
        readers = {
            FileFormat.CSV: r.read_csv,
            FileFormat.JSON: r.read_json,
            FileFormat.PARQUET: r.read_parquet,
            FileFormat.EXCEL: r.read_excel
        }
        return readers[self.config.input_format]
    
    def _get_writer(self):
        writers = {
            FileFormat.CSV: w.write_csv,
            FileFormat.JSON: w.write_json,
            FileFormat.PARQUET: w.write_parquet,
            FileFormat.EXCEL: w.write_excel
        }
        return writers[self.config.output_format]

    @log_execution_time
    def process(self):
        """Execute the data processing pipeline"""
        try:
            self.logger.info("Starting data pipeline processing")
            
            # Get appropriate reader and writer
            reader = self._get_reader()
            writer = self._get_writer()
            
            processed_data = []
            for batch in reader(self.config.input_path, self.config.batch_size):
                batch = t.validate_data(batch, self.config.required_columns)
                batch = t.clean_column_names(batch)
                batch = t.apply_column_mappings(batch, self.config.column_mappings)
                batch = t.filter_rows(batch, self.config.filter_conditions)
                processed_data.extend(batch)
            
            # Write results
            writer(processed_data, self.config.output_path)
            
            self.logger.info("Pipeline processing completed successfully")
            return processed_data
            
        except Exception as e:
            self.logger.error(f"Pipeline processing failed: {str(e)}")
            raise PipelineError(f"Pipeline processing failed: {str(e)}")