class PipelineError(Exception):
    """Base exception for pipeline errors"""
    pass

class DataValidationError(PipelineError):
    """Raised when data validation fails"""
    pass

class TransformationError(PipelineError):
    """Raised when data transformation fails"""
    pass

class IOError(PipelineError):
    """Raised when input/output operations fail"""
    pass