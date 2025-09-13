import logging
import sys
from typing import Optional
from datetime import datetime


class Logger:
    """Logger wrapper for the application"""

    def __init__(self, name: str, level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not self.logger.handlers:
            self._setup_handler()

    def _setup_handler(self):
        """Setup console handler with custom format"""
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(message, extra=kwargs)

    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(message, extra=kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(message, extra=kwargs)

    def error(self, message: str, **kwargs):
        """Log error message"""
        self.logger.error(message, extra=kwargs)

    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.logger.critical(message, extra=kwargs)

    def log_exception(self, message: str, exception: Exception, **kwargs):
        """Log exception with traceback"""
        self.logger.error(f"{message}: {str(exception)}", exc_info=True, extra=kwargs)


class LoggerFactory:
    """Factory for creating logger instances"""

    _loggers = {}

    @classmethod
    def get_logger(cls, name: str, level: int = logging.INFO) -> Logger:
        """Get or create logger instance"""
        if name not in cls._loggers:
            cls._loggers[name] = Logger(name, level)
        return cls._loggers[name]

    @classmethod
    def get_default_logger(cls) -> Logger:
        """Get default application logger"""
        return cls.get_logger("rocketbot", logging.INFO)


def get_logger(name: str = "rocketbot") -> Logger:
    """Get logger instance"""
    return LoggerFactory.get_logger(name)
