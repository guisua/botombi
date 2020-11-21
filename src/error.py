from logger import Logger
from strings import Strings


class ErrorHandler:
    @staticmethod
    def environment_var_missing(var):
        msg = Strings.Error.Environment.ENV_VAR_MISSING.format(var)
        Logger.error(msg)
        raise Exception(msg)
