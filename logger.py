import logging
from functools import wraps
from typing import Callable, Optional
import time

def setup_logger(log_level: str, log_file: Optional[str] = None):
    logger = logging.getLogger("pipeline")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

def log_execution_time(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger("pipeline")
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(
                f"Function {func.__name__} executed in {execution_time:.2f} seconds"
            )
            return result
        except Exception as e:
            logger.error(
                f"Function {func.__name__} failed after {time.time() - start_time:.2f} seconds"
            )
            raise
    return wrapper