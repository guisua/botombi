import telegram
import re


class Messages:
    class Setup:
        START_WELCOME = "I'm up and running!"

    class Errors:
        SEARCH_UNAVAILABLE = "The search is currently unavailable."

    class Search:
        SEARCH_RESULT_MOVIE = "{}"


class MessageDecorator:
    @staticmethod
    def search_result(result: dict):
        return Messages.Search.SEARCH_RESULT_MOVIE.format(
            result.get("title"),
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
        poster_url = result.get("poster")
        if poster_url:
            bot.send_photo(
                chat_id=chat_id,
                caption=text,
                photo=f"https://image.tmdb.org/t/p/w300{poster_url}",
                reply_markup=telegram.InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            telegram.InlineKeyboardButton(
                                text="Dummy button", url="https://google.com"
                            )
                        ]
                    ]
                ),
            )
        else:
            bot.send_message(
                chat_id=chat_id,
                text=text,
            )
