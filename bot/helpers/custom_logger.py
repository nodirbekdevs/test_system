from logging import Logger, FileHandler, StreamHandler, Formatter
from sys import stderr


def custom_logger(name: str, level: str):
    _logger = Logger(name, level)
    file_handler = FileHandler("log.log", encoding="utf-8")
    stream_handler = StreamHandler(stderr)
    row_format = "{'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s'}"
    file_handler.setFormatter(Formatter(row_format, datefmt='%d/%m/%Y %I:%M:%S %p'))
    stream_handler.setFormatter(Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
    _logger.addHandler(file_handler)
    _logger.addHandler(stream_handler)
    return _logger