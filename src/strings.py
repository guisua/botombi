class Strings:
    class Setup:
        START_WELCOME = "I'm up and running!"

    class Search:
        SEARCH_RESULT_MOVIE_TITLE_AND_YEAR = "{} ({})"
        SEARCH_RESULT_MOVIE_PHOTO_CAPTION = "{}\n{}"

    class MovieStatus:
        AVAILABLE = "🟢 Available"
        APPROVED = "🟡 Request approved"
        REQUESTED = "🟠 Requested"
        DENIED = "🔴 Denied"

    class Requests:
        REQUEST_ACTION = "Request"

    class Error:
        class Environment:
            ENV_VAR_MISSING = "Environment variable '{}' is not set correctly."

        class Command:
            UNKNOWN_COMMAND = "I don't know how to help with that yet.\n\nYou can type /search followed by the movie title."

        class Search:
            SEARCH_UNAVAILABLE = "The search is currently unavailable."