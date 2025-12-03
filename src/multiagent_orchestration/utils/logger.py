"""Logging utility for the orchestration system."""

import logging
import sys
from typing import Optional
from pythonjsonlogger import jsonlogger


def setup_logger(
    name: str = "multiagent_orchestration",
    level: int = logging.INFO,
    json_format: bool = True
) -> logging.Logger:
    """
    Set up a logger for the orchestration system.
    
    Args:
        name: Logger name
        level: Logging level
        json_format: Whether to use JSON formatting
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Set formatter
    if json_format:
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s"
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
