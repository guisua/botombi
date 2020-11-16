import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class Logger:

    # logger singleton
    _logger = None

    def __init__(self):
        if Logger._logger is not None:
            Logger.error("Can't init more than one logger")
            return None

        self._logger = logging.getLogger()

    @staticmethod
    def shared():
        if Logger._logger is None:
            Logger._logger = Logger()
        return Logger._logger

    @staticmethod
    def info(msg):
        Logger.shared()._logger.info(msg)

    @staticmethod
    def warning(msg):
        Logger.shared()._logger.warning(msg)

    @staticmethod
    def error(msg):
        Logger.shared()._logger.error(msg)