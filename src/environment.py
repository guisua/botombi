import os

from error import ErrorHandler


class EnvironmentVariables:

    TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
    TELEGRAM_BOT_NAME = "TELEGRAM_BOT_NAME"
    OMBI_HOST = "OMBI_HOST"
    OMBI_API_KEY = "OMBI_API_KEY"
    OMBI_USER_NAME = "OMBI_USER_NAME"


class Environment:

    _environment = None

    def __init__(self):
        if Environment._environment is not None:
            _logger.error("Can't init more than one environment")
            return None

        self._telegram_bot_token = os.getenv(EnvironmentVariables.TELEGRAM_BOT_TOKEN)
        self._telegram_bot_name = os.getenv(EnvironmentVariables.TELEGRAM_BOT_NAME)
        self._ombi_host = os.getenv(EnvironmentVariables.OMBI_HOST)
        self._ombi_api_key = os.getenv(EnvironmentVariables.OMBI_API_KEY)
        self._ombi_user_name = os.getenv(EnvironmentVariables.OMBI_USER_NAME)
        self._validate_environment()

    def _validate_environment(self):
        if not self._telegram_bot_token:
            ErrorHandler.environment_var_missing(
                EnvironmentVariables.TELEGRAM_BOT_TOKEN
            )

        if not self._telegram_bot_name:
            ErrorHandler.environment_var_missing(EnvironmentVariables.TELEGRAM_BOT_NAME)

        if not self._ombi_host:
            ErrorHandler.environment_var_missing(EnvironmentVariables.OMBI_HOST)

        if not self._ombi_api_key:
            ErrorHandler.environment_var_missing(EnvironmentVariables.OMBI_API_KEY)

        if not self._ombi_user_name:
            ErrorHandler.environment_var_missing(EnvironmentVariables.OMBI_USER_NAME)

    @staticmethod
    def shared():
        if Environment._environment is None:
            Environment._environment = Environment()
        return Environment._environment

    @staticmethod
    def telegram_bot_token():
        return Environment.shared()._telegram_bot_token

    @staticmethod
    def ombi_host():
        return Environment.shared()._ombi_host

    @staticmethod
    def ombi_api_key():
        return Environment.shared()._ombi_api_key

    @staticmethod
    def ombi_user_name():
        return Environment.shared()._ombi_user_name
