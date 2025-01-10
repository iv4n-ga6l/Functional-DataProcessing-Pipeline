import pytest
import logging

@pytest.fixture(autouse=True)
def setup_logging():
    """Setup logging for all tests"""
    logging.basicConfig(level=logging.INFO)
    yield
    logging.shutdown()