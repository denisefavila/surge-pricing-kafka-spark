import json
import logging


def setup_logging():

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("/app/logs/application.log")
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = record.__dict__.copy()
        if "structured_data" in log_record:
            log_record.update(log_record.pop("structured_data"))
        return json.dumps(log_record)


def setup_structured_logger(file_name):
    logger = logging.getLogger("structured_logger")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(f"/app/logs/{file_name}.log")
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = JSONFormatter()

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
