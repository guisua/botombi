import telegram
import re


class Messages:
    class Setup:
        START_WELCOME = "I'm up and running!"

    class Errors:
        SEARCH_UNAVAILABLE = "The search is currently unavailable."

    class Search:
        SEARCH_RESULT_MOVIE = "{}"

    class MovieStatus:
        AVAILABLE = "🟢 Available"
        APPROVED = "🟡 Request approved"
        REQUESTED = "🟠 Requested"
        DENIED = "🔴 Denied"


class MessageDecorator:
    @staticmethod
    def search_result(result: dict):
        status = ""
        if result.requested:
            status = Messages.MovieStatus.REQUESTED
        if result.approved:
            status = Messages.MovieStatus.APPROVED
        if result.denied:
            status = Messages.MovieStatus.DENIED
        if result.available:
            status = Messages.MovieStatus.AVAILABLE

        return (
            Messages.Search.SEARCH_RESULT_MOVIE.format(result.title)
            + (" ({})".format(result.year) if result.year else "")
            + "\n{}".format(status)
        )


class Messenger:
    @staticmethod
    def send_message(bot, chat_id, msg, *args):
        text = msg
        if args:
            text = msg.format(args)

        bot.send_message(chat_id=chat_id, text=text)

    @staticmethod
    def send_search_result(bot: telegram.Bot, chat_id, result):
        text = MessageDecorator.search_result(result)
        reply_markup = (
            telegram.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        telegram.InlineKeyboardButton(
                            text="Request: {}".format(text), callback_data="test"
                        )
                    ]
                ]
            )
            if result.requestable()
            else None
        )
        if result.poster_url:
            bot.send_photo(
                chat_id=chat_id,
                caption=text if not result.requestable() else None,
                photo=result.poster_url,
                reply_markup=reply_markup,
            )
        else:
            bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
