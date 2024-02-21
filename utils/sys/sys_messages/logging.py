import os, logging
from colorama import Fore, Style, init

from utils.classes.config.color_render import CustomFormatter

def setup_custom_logging(log_type, title, message):
    # Load environment variables from .env file
    
    # Get DEBUG_MESSAGES value from .env, default to False if not set
    debug_messages = os.getenv('DEBUG_MESSAGES', 'False').lower() in ['true', '1', 't']

    # Configure the logging level
    logging_level = logging.DEBUG if debug_messages else logging.CRITICAL

    # Create or get a logger
    logger = logging.getLogger(title)
    logger.setLevel(logging_level)

    # Check if the logger already has a StreamHandler to prevent adding another
    if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        # Create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging_level)

        # Create formatter and add it to the handler
        ch.setFormatter(CustomFormatter())

        # Add the handler to the logger
        logger.addHandler(ch)

    # Dynamically call the logging method based on log_type
    if debug_messages:
        getattr(logger, log_type.lower(), logger.error)(message)
