import logging


def setup_logging():
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # File handler to log to a file
    file_handler = logging.FileHandler("/app/logs/application.log")
    file_handler.setLevel(logging.INFO)

    # Console handler to log to the screen
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter to define log message format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Set the formatter for both handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
