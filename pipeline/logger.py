import logging

def setup_logger(name: str, log_file: str, level: int = logging.INFO):
    """
    Sets up a logger for the pipeline.

    Args:
        name (str): Name of the logger.
        log_file (str): File path to save the log.
        level (int): Logging level (default: logging.INFO).

    Returns:
        logging.Logger: Configured logger instance.
    """
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger