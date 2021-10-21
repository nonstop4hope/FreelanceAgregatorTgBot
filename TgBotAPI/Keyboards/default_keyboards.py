from telegram import InlineKeyboardButton


class Keyboards:

    @staticmethod
    def start_menu():
        keyboard = [
            [
                InlineKeyboardButton("Последние новости", callback_data='last_tasks'),
                InlineKeyboardButton("Какая-то кнопка", callback_data='something'),
            ],
            [InlineKeyboardButton("Подписаться на рассылку", callback_data='subscribe')],
        ]
        return keyboard


