from telegram import InlineKeyboardButton


class Keyboards:

    @staticmethod
    def start_menu(subscribe):
        if subscribe:
            keyboard = [
                [
                    InlineKeyboardButton("Последние новости", callback_data='last_tasks'),
                    InlineKeyboardButton("Выбрать интересующие категории", callback_data='categories'),
                ],
                [InlineKeyboardButton("Подписаться на рассылку", callback_data='subscribe')],
            ]
        else:
            keyboard = [
                [
                    InlineKeyboardButton("Последние новости", callback_data='last_tasks'),
                    InlineKeyboardButton("Выбрать интересующие категории", callback_data='categories'),
                ],
                [InlineKeyboardButton("Отписаться от рассылки", callback_data='unsubscribe')],
            ]
        return keyboard

    @staticmethod
    def categories_menu():
        keyboard = [
            [
                InlineKeyboardButton("👨‍💻 Разработка", callback_data='development'),
                InlineKeyboardButton("⚙️ Тестирование", callback_data='testing'),
            ],
            [
                InlineKeyboardButton("🌐 Администрирование", callback_data='administration'),
                InlineKeyboardButton("🧑‍🎨 Дизайн", callback_data='design'),
            ],
            [
                InlineKeyboardButton("⌨️ Контент", callback_data='content'),
                InlineKeyboardButton("💶 Маркетинг", callback_data='marketing'),
            ],
            [
                InlineKeyboardButton("🧠 Разное", callback_data='various'),
                InlineKeyboardButton("✅ Подтвердить", callback_data='save_change'),
            ]
        ]
        return keyboard


