import telegram
from telegram.ext import (
    Updater,
    CommandHandler,
    Filters,
    MessageHandler,
    CallbackQueryHandler,
)

from environment import Environment
from logger import Logger
from ombi import Ombi
from search import MultiQuery, Search, MovieSearchResult
from strings import Strings
from messages import Messenger


def launch(env: Environment):
    Logger.info("Starting Plexy...")
    bot = Bot(environment=env)
    bot.startup()


class CommandFactory:
    @staticmethod
    def start():
        return Command(
            name="start", description="Starts the bot", callback=Callbacks.start
        )

    @staticmethod
    def search():
        return Command(
            name="search",
            description="Performs a search for movies and TV shows.",
            callback=Callbacks.search,
        )


class Command:
    def __init__(self, name, description, callback):
        self.name = name
        self.description = description
        self.callback = callback


class Bot:
    def __init__(self, environment):
        self.updater = Updater(token=environment.telegram_bot_token())
        Ombi.initialize(
            host=environment.ombi_host(),
            api_key=environment.ombi_api_key(),
            ombi_user_name=environment.ombi_user_name(),
        )

        self.updater.dispatcher.add_handler(
            CallbackQueryHandler(Callbacks.handle_callback_query, pass_user_data=True)
        )

    def startup(self):
        if self.updater is None:
            return None

        self._register_default_commands()

        self.updater.start_polling()
        Logger.info("Plexy started correctly and is ready for battle!")

    def register_command(self, command: Command):
        handler = CommandHandler(command=command.name, callback=command.callback)
        self.updater.dispatcher.add_handler(handler)

    def _register_default_commands(self):
        commands = [
            CommandFactory.start(),
            CommandFactory.search(),
        ]

        for command in commands:
            self.register_command(command)

        self.updater.dispatcher.add_handler(
            MessageHandler(Filters.command, Callbacks.unknown)
        )


class CallbackData:
    def __init__(self, data: dict):
        self.action = data.get("action")
        self.type = data.get("type")
        self.id = data.get("id")

        if not (self.action and self.type and self.id):
            return None

    @staticmethod
    def from_str(data: str):
        return CallbackData(json.loads(data))


class Callbacks:
    @staticmethod
    def start(update: telegram.Update, context: telegram.ext.CallbackContext):
        Messenger.send_message(
            bot=context.bot,
            chat_id=update.effective_chat.id,
            msg=Strings.Setup.START_WELCOME,
        )

    @staticmethod
    def search(update: telegram.Update, context: telegram.ext.CallbackContext):

        query = MultiQuery(update, context)
        Logger.info(f"Received search command with: '{query.text}'")
        results = Search.execute(query)
        for result in results:
            if result.mediaType == "movie":
                movie_result = MovieSearchResult(Ombi.fetch_movie(result.id))
                Messenger.send_search_result(
                    bot=context.bot,
                    chat_id=update.effective_chat.id,
                    result=movie_result,
                )

    @staticmethod
    def handle_callback_query(
        update: telegram.Update, context: telegram.ext.CallbackContext
    ):
        Logger.info(update.to_json())
        callback_data = CallbackData.from_str(update.callback_query.data)
        Ombi.process_callback_data(callback_data)
        Logger.info(callback_data.__dict__)
        context.bot.delete_message(
            chat_id=int(update.callback_query.message.chat.id),
            message_id=int(update.callback_query.message.message_id),
        )

    @staticmethod
    def unknown(update: telegram.Update, context: telegram.ext.CallbackContext):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=Strings.Errors.UNKNOWN_COMMAND,
        )
