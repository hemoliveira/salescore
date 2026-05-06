import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler


class Logger:

    BASE_DIR = Path(__file__).resolve().parent.parent
    LOG_DIR = BASE_DIR / "logs"
    LOG_FILE = LOG_DIR / "app.log"

    LOG_FORMAT = "%(asctime)s | %(levelname)s-8s | %(name)s | %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    BACKUP_COUNT = 7

    @classmethod
    def get_logger(cls, name: str = "APP", level: int = logging.INFO) -> logging.Logger:
        """
        Configure and return a logger instance.
        """
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger(name)

        if logger.handlers:
            logger.setLevel(level)
            for handler in logger.handlers:
                handler.setLevel(level)
            return logger

        logger.setLevel(level)
        logger.propagate = False

        formatter = logging.Formatter(
            cls.LOG_FORMAT,
            datefmt=cls.DATE_FORMAT,
        )

        file_handler = TimedRotatingFileHandler(
            filename=cls.LOG_FILE,
            when="midnight",
            interval=1,
            backupCount=cls.BACKUP_COUNT,
            encoding="utf-8",
            delay=True,
        )

        file_handler.suffix = "%Y-%m-%d"
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger
