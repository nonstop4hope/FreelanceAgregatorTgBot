from telegram.ext import Updater, CommandHandler, InlineQueryHandler, CallbackQueryHandler, MessageHandler, Filters, \
    Dispatcher

from TgBotAPI.TgBotAPI import start, help_command, callback_start_menu, unexpected_message
from TgBotAPI.config import BOT_TOKEN as token


def main() -> None:

    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_start_menu))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.all, unexpected_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
