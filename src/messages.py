import telegram
import re
import json

from logger import Logger
from search import SearchResult
from strings import Strings


class MessageDecorator:
    @staticmethod
    def result_title(result: SearchResult, year=True):
        if year and result.year:
            return Strings.Search.SEARCH_RESULT_MOVIE_TITLE_AND_YEAR.format(
                result.title, result.year
            )

        return result.title

    @staticmethod
    def result_caption(result: SearchResult, status=True):
        title = MessageDecorator.result_title(result, year=True)
        result_status = MessageDecorator.result_status(result)
        if status and result_status:
            return Strings.Search.SEARCH_RESULT_MOVIE_CAPTION.format(
                title, result_status
            )

        return title

    @staticmethod
    def result_status(result: SearchResult):
        status = ""
        if result.requested:
            status = Strings.MovieStatus.REQUESTED
        if result.approved:
            status = Strings.MovieStatus.APPROVED
        if result.denied:
            status = Strings.MovieStatus.DENIED
        if result.available:
            status = Strings.MovieStatus.AVAILABLE

        if status:
            return status

        return None


class KeyboardFactory:
    @staticmethod
    def inline_keyboard_markup(buttons: list):
        return telegram.InlineKeyboardMarkup(inline_keyboard=[buttons])


class ButtonFactory:
    @staticmethod
    def inline_request_button(result: SearchResult):
        return telegram.InlineKeyboardButton(
            text=Strings.Requests.REQUEST_ACTION,
            callback_data=json.dumps(result.callback_data()),
        )


class MarkupFactory:
    @staticmethod
    def reply_markup_from_result(result: SearchResult):
        reply_markup = KeyboardFactory.inline_keyboard_markup(
            buttons=[ButtonFactory.inline_request_button(result)]
        )
        if not result.requestable():
            return None
        return reply_markup


class Messenger:
    @staticmethod
    def send_message(bot, chat_id, msg, *args):
        text = msg
        if args:
            text = msg.format(args)

        bot.send_message(chat_id=chat_id, text=text)

    @staticmethod
    def send_search_result(bot: telegram.Bot, chat_id, result):
        if result.poster_url:
            return bot.send_photo(
                chat_id=chat_id,
                caption=MessageDecorator.result_caption(
                    result, status=not result.requestable()
                ),
                photo=result.poster_url,
                reply_markup=MarkupFactory.reply_markup_from_result(result),
            )
        else:
            return bot.send_message(
                chat_id=chat_id,
                text=MessageDecorator.result_caption(result),
                reply_markup=MarkupFactory.reply_markup_from_result(result),
            )
