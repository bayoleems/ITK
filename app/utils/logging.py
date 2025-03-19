import logging
from typing import Optional

def get_logger(name: Optional[str] = None) -> logging.Logger:

    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Configure logging format
        formatter = logging.Formatter(
            '%(levelname)s: %(asctime)s.0 - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Set default level
        logger.setLevel(logging.INFO)
        
    return logger 

logger = get_logger(__name__)

