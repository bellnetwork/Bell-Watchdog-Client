# custom_formatter.py
import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""
    
    custom_format = "%(levelname)s:%(name)s:%(message)s"

    FORMATS = {
        logging.DEBUG: Fore.CYAN + custom_format + Style.RESET_ALL,
        logging.INFO: Fore.GREEN + custom_format + Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW + custom_format + Style.RESET_ALL,
        logging.ERROR: Fore.RED + custom_format + Style.RESET_ALL,
        logging.CRITICAL: Fore.RED + Style.RESET_ALL + custom_format,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.custom_format)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)