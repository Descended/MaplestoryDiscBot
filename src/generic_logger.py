# Logger Module
# Business logic obtained from https://www.toptal.com/python/in-depth-python-logging
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from src.settings import Config
FORMATTER = logging.Formatter(Config.LOG_FORMAT)


def get_console_handler():
	console_handler = logging.StreamHandler(sys.stdout)
	console_handler.setFormatter(FORMATTER)
	return console_handler


def get_file_handler():
	file_handler = TimedRotatingFileHandler(Config.LOG_FILE, when='midnight')
	file_handler.setFormatter(FORMATTER)
	return file_handler


class NullHandler(logging.Handler):
	def emit(self, record):
		pass


def get_logger(logger_name):
	logger = logging.getLogger(logger_name)
	logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
	h = NullHandler()  # Instantiate with a silent handler that doesn't return anything, since
	logger.addHandler(h)  # the logger object from the logging module REQUIRES at least ONE handler
	return logger


def shutdown_logger():
	logging.shutdown()
