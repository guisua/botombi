class Messages:
    class Setup:
        START_WELCOME = "I'm up and running!"

    class Errors:
        SEARCH_UNAVAILABLE = "The search is currently unavailable."


class Messenger:
    @staticmethod
    def send_message(bot, chat_id, msg, *args):
        bot.send_message(chat_id=chat_id, text=msg.format(args))