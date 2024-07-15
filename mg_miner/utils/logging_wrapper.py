import logging

class LoggingWrapper:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.logger = logging.getLogger()

    def set_trace_id(self, trace_id: str):
        self.trace_id = trace_id
        for handler in self.logger.handlers:
            handler.addFilter(lambda record: setattr(record, 'trace_id', trace_id))

    def set_global_level(self, level: str):
        self.logger.setLevel(level)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def log(self, level: str, message: str):
        getattr(self.logger, level.lower())(message)
