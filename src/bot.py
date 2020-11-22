import json
import threading

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
from search import MultiQuery, Search, MovieSearchResult, TvSearchResult
from strings import Strings
from messages import Messenger


def launch(env: Environment):
    Logger.info("Starting Plexy...")
    bot = Bot(environment=env)
    bot.startup()


class Command:
    def __init__(self, name, description, callback):
        self.name = name
        self.description = description
        self.callback = callback


class Bot:
    def __init__(self, environment):
        self.updater = Updater(token=environment.telegram_bot_token())
        self.max_search_results = environment.max_search_results(default_max=100)
        self.search_result_delete_delay = environment.search_result_delete_delay()
        Ombi.initialize(
            host=environment.ombi_host(),
            api_key=environment.ombi_api_key(),
            ombi_user_name=environment.ombi_user_name(),
        )

    def startup(self):
        if self.updater is None:
            return None

        self.updater.dispatcher.add_handler(
            CallbackQueryHandler(self.handle_callback_query, pass_user_data=True)
        )

        self._register_default_commands()
        self.updater.start_polling()
        Logger.info("Plexy started correctly and is ready for battle!")

    def register_command(self, command: Command):
        handler = CommandHandler(command=command.name, callback=command.callback)
        self.updater.dispatcher.add_handler(handler)

    def _register_default_commands(self):
        commands = [
            Command(name="start", description="Starts the bot", callback=self.start),
            Command(
                name="search",
                description="Performs a search for movies and TV shows.",
                callback=self.search,
            ),
        ]

        for command in commands:
            self.register_command(command)

        self.updater.dispatcher.add_handler(
            MessageHandler(Filters.command, self.unknown)
        )

    def start(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        Messenger.send_message(
            bot=context.bot,
            chat_id=update.effective_chat.id,
            msg=Strings.Setup.START_WELCOME,
        )

    def search(self, update: telegram.Update, context: telegram.ext.CallbackContext):

        query = MultiQuery(update, context)
        Logger.info(f"Received search command with: '{query.text}'")

        if query.text == "":
            for i, msg in enumerate(
                [
                    Strings.Error.Command.COMMAND_USAGE_HELP_INTRO,
                    Strings.Error.Command.SEARCH_COMMAND_USAGE_HELP,
                    Strings.Error.Command.COMMAND_USAGE_EXAMPLE_INTRO,
                    Strings.Error.Command.SEARCH_COMMAND_USAGE_EXAMPLE,
                ]
            ):
                threading.Timer(
                    i / 2,
                    Messenger.send_message,
                    [context.bot, update.effective_chat.id, msg],
                ).start()
            return
        results = Search.execute(query)
        for result in results:
            if result.mediaType == "movie":
                detailed_result = MovieSearchResult(Ombi.fetch_movie(result.id))
            elif result.mediaType == "tv":
                detailed_result = TvSearchResult(Ombi.fetch_tv(result.id))
            detailed_result.poster_url = Ombi.Images.Poster.format(result.poster)
            msg = Messenger.send_search_result(
                bot=context.bot,
                chat_id=update.effective_chat.id,
                result=detailed_result,
            )
            threading.Timer(self.search_result_delete_delay, msg.delete).start()

    def handle_callback_query(
        self, update: telegram.Update, context: telegram.ext.CallbackContext
    ):
        Logger.info(update.to_json())
        callback_data = CallbackData.from_str(update.callback_query.data)
        if Ombi.process_callback_data(callback_data):
            Logger.info(f"Callback was processed correctly: {callback_data.__dict__}")
            context.bot.delete_message(
                chat_id=int(update.callback_query.message.chat.id),
                message_id=int(update.callback_query.message.message_id),
            )
        else:
            Logger.error("Callback could not be processed correctly")

    def unknown(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=Strings.Errors.UNKNOWN_COMMAND,
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
