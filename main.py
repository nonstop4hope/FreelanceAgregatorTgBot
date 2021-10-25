from telegram.ext import Updater, CommandHandler, InlineQueryHandler, CallbackQueryHandler, MessageHandler, Filters, \
    Dispatcher

from TgBotAPI.TgBotAPI import start, help_command, callback_start_menu, unexpected_message
from TgBotAPI.config import BOT_TOKEN as token


def main() -> None:

    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start, run_async=True))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_start_menu, run_async=True))
    dispatcher.add_handler(CommandHandler("help", help_command, run_async=True))

    dispatcher.add_handler(MessageHandler(Filters.all, unexpected_message, run_async=True))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
