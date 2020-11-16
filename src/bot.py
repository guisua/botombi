from telegram.ext import Updater, CommandHandler

from environment import Environment
from logger import Logger
from commands import CommandFactory, Command


def launch(env: Environment):
    Logger.info("Starting Plexy...")
    bot = Bot(environment=env)
    bot.startup()


class Bot:
    def __init__(self, environment):
        self.updater = Updater(token=environment.telegram_bot_token())

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
