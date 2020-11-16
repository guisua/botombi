import os

from error import ErrorHandler


class EnvironmentVariables:

    TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
    TELEGRAM_BOT_NAME = "TELEGRAM_BOT_NAME"


class Environment:

    _environment = None

    def __init__(self):
        if Environment._environment is not None:
            _logger.error("Can't init more than one environment")
            return None

        self._telegram_bot_token = os.getenv(EnvironmentVariables.TELEGRAM_BOT_TOKEN)
        self._telegram_bot_name = os.getenv(EnvironmentVariables.TELEGRAM_BOT_NAME)
        self._validate_environment()

    def _validate_environment(self):
        if not self._telegram_bot_token:
            ErrorHandler.environment_var_missing(
                EnvironmentVariables.TELEGRAM_BOT_TOKEN
            )

        if not self._telegram_bot_name:
            ErrorHandler.environment_var_missing(EnvironmentVariables.TELEGRAM_BOT_NAME)

    @staticmethod
    def shared():
        if Environment._environment is None:
            Environment._environment = Environment()
        return Environment._environment

    @staticmethod
    def telegram_bot_token():
        return Environment.shared()._telegram_bot_token
