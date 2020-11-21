import json

import telegram
from messages import Messenger, Strings
from search import MovieQuery, Search
from logger import Logger
from ombi import Ombi


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

        query = MovieQuery(update, context)
        Logger.info(f"Received search command with: '{query.text}'")
        results = Search.execute(query)
        for result in results:
            Messenger.send_search_result(
                bot=context.bot, chat_id=update.effective_chat.id, result=result
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
