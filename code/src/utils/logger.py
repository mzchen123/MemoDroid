import logging
from pathlib import Path
from src.config.config import LOG_FORMAT, LOG_LEVEL

def setup_logger(name: str, log_file: str, log_dir: str = "output") -> logging.Logger:
    """Setup logger"""
    # Create log directory
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Create file handler
    file_handler = logging.FileHandler(log_path / log_file)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(file_handler)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(console_handler)
    
    return logger 