import logging
from typing import Optional

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: The name for the logger. If None, returns the root logger.
        
    Returns:
        A configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Configure logging format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Set default level
        logger.setLevel(logging.INFO)
        
    return logger 

logger = get_logger(__name__)

