from logger import Logger


class ErrorMessages:
    ENV_VAR_MISSING = "Environment variable '{}' is not set correctly."


class ErrorHandler:
    @staticmethod
    def environment_var_missing(var):
        msg = ErrorMessages.ENV_VAR_MISSING.format(var)
        Logger.error(msg)
        raise Exception(msg)
