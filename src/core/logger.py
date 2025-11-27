"""
Logger Module
Configures application logging
"""
import logging
import colorlog
from pathlib import Path


def setup_logger(config: dict = None):
    """
    Setup application logger with color support
    
    Args:
        config: Logging configuration dictionary
    """
    if config is None:
        config = {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'file': 'logs/elt.log'
        }
    
    # Create logs directory if it doesn't exist
    log_file = config.get('file', 'logs/elt.log')
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Console handler with colors
    console_handler = colorlog.StreamHandler()
    console_handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    ))
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(
        config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.get('level', 'INFO')))
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    return root_logger
