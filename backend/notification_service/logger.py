import logging
from logging.handlers import RotatingFileHandler
import os

# Set up log directory and log file
LOG_DIR = "logs"
LOG_FILE = "notification_service.log"

# Create log directory if it doesn't exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
#test

# Logger Configuration
def configure_logger():
    custom_logger = logging.getLogger("NotificationServiceLogger")
    custom_logger.setLevel(logging.DEBUG)  # Capture all log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    # Log to file with rotation
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, LOG_FILE), maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setLevel(logging.INFO)  # Log INFO level and above to file
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # Log to console (stdout)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Log DEBUG level and above to console
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    # Add handlers to the logger
    custom_logger.addHandler(file_handler)
    custom_logger.addHandler(console_handler)

    return custom_logger


# Instantiate the logger
logger = configure_logger()

# Example usage of logger in different parts of your service
logger.info("Logger configured successfully")
