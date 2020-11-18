import telegram
from messages import Messenger, Messages
from search import MovieQuery, Search


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


class Callbacks:
    @staticmethod
    def start(update: telegram.Update, context: telegram.ext.CallbackContext):
        Messenger.send_message(
            bot=context.bot,
            chat_id=update.effective_chat.id,
            msg=Messages.Setup.START_WELCOME,
        )

    @staticmethod
    def search(update: telegram.Update, context: telegram.ext.CallbackContext):

        query = MovieQuery(update, context)
        results = Search.execute(query)
        for result in results[: min(len(results) - 1, 5)]:
            Messenger.send_search_result(
                bot=context.bot, chat_id=update.effective_chat.id, result=result
            )
