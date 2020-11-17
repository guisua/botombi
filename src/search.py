import telegram

from ombi import Ombi


class Query:
    def __init__(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        self.bot = context.bot
        self.chat_id = (update.effective_chat.id,)
        self.text = " ".join(context.args)

    def validate(self):
        return True if self.text else False


class Search:
    @staticmethod
    def execute(query: Query):
        if not query.validate():
            return None

        return Ombi.search(query_str=query.text)