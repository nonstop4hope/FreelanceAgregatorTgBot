import logging
from telegram import ParseMode, Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from MongoDBAPI.MongoDBAPI import Mongod
from MongoDBAPI.models import TgUser
from TgBotAPI.Keyboards.default_keyboards import Keyboards
import os
import random


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

category_list = ('development', 'testing', 'administration', 'design', 'marketing', 'various', 'content')


def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if Mongod().check_existing(user_id):
        subscribed = False
    else:
        subscribed = True

    reply_markup = InlineKeyboardMarkup(Keyboards.start_menu(subscribed))

    update.message.reply_text('Добро пожаловать!\nЭтот бот поможет Вам всегда оставаться в курсе событий.\n'
                              'Для продолжения работы выберите один из пунктов меню. При выборе пункта "Подписаться'
                              'на рассылку" бот в автоматическом режиме будет присылать Вам информацию с habr.com',
                              reply_markup=reply_markup)

    logger.info(f'User "{user_id}" called the start menu')


def subscribe(mongod, user_id: int):
    if isinstance(user_id, int):
        telegram_user = TgUser()
        telegram_user.id = user_id

        if mongod.add_user_to_db(telegram_user):
            return True
        else:
            return False


def callback_start_menu(update: Update, context: CallbackContext) -> None:
    global category_list
    query = update.callback_query
    query.answer()
    mongod = Mongod()
    user_id = query.from_user.id

    categories_from_db = mongod.get_current_state(user_id)

    if query.data == 'last_tasks':
        last_tasks = mongod.get_last_task(limit=5)
        query.edit_message_text(text=f"Последние новости для Вас, надеюсь они будут полезны")
        for task in last_tasks:
            description = task["description"]
            if len(description) > 300:
                description = description[:300] + '...'
            message = (
                f'🖥️\n'
                f'<b>╠Название:</b> <code>{task["name"]}</code>\n'
                f'<b>╠Дата размещения:</b> {task["date"]}\n'
                f'<b>╠Цена:</b> {task["price"]}\n'
                f'<b>╠Просмотры:</b> {task["views"]}\n'
                f'<b>╠Откликнулось:</b> {task["responses"]}\n'
                f'<b>╠Ссылка на задание:</b> {task["url"]}\n'
                f'<b>╚Описание:</b> {description}\n'
            )
            context.bot.send_message(chat_id=user_id, text=message, disable_web_page_preview=True,
                                     parse_mode=ParseMode.HTML)
        logger.info(f'User "{user_id}" has received the latest tasks')
    if query.data == 'categories':
        if mongod.check_existing(user_id):
            reply_markup = InlineKeyboardMarkup(Keyboards.categories_menu())
            query.edit_message_text(text=get_categories_text(categories_from_db), reply_markup=reply_markup,
                                    parse_mode=ParseMode.HTML)
        else:
            query.edit_message_text(text=f"Выбор категорий доступен только пользователям, подписанным на рассылку")
        logger.info(f'User "{user_id}" went to the categories menu')
    if query.data == 'unsubscribe':
        mongod.delete_user(user_id)
        query.edit_message_text(text=f"Нам было хорошо вместе! Пока! 😢")
        logger.info(f'User "{user_id}" has unsubscribed')
    if query.data == 'subscribe':
        if subscribe(mongod, user_id):
            username = query.from_user.username
            if not username:
                username = ''
            query.edit_message_text(text=f"Спасибо за подписку! Добро пожаловать {username}!")
        else:
            query.edit_message_text(text=f"Произошло недопонимание, Вы уже подписаны на рассылку!")
        logger.info(f'User "{user_id}" subscribed')
    if query.data in category_list:
        mongod.update_state(user_id, query.data)
        get_categories_window(mongod, user_id, query)
        logger.info(f'User "{user_id}" has selected a category "{query.data}"')
    if query.data == 'save_change':
        query.edit_message_text(text=f"Спасибо за выбор категорий!")
        logger.info(f'User "{user_id}" has finished selecting categories')


def get_categories_window(mongod, user_id, query):
    categories_from_db = mongod.get_current_state(user_id)
    reply_markup = InlineKeyboardMarkup(Keyboards.categories_menu())
    query.edit_message_text(text=get_categories_text(categories_from_db), reply_markup=reply_markup,
                            parse_mode=ParseMode.HTML)


def get_categories_text(categories_from_db):
    text = (
        f'Вы можете выбрать интересующие Вас категории для автоматической расслылки.\n'
        f'Выбрать избранные категории могут только пользователи, подписанные на рассылку!\n\n'
    )
    if categories_from_db:
        categories_from_db = ' '.join(categories_from_db)
        categories_part = (
            f'На данный момент в избранных категориях находятся: <b>{categories_from_db}</b>\n\n'
        )
    else:
        categories_part = (
            f'<b>На данный момент у Вас нет избранных категорий!</b>\n'
        )
    text = text + categories_part
    return text


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Используйте команду /start чтобы начать работу.")


def unexpected_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    logger.info(f'Message "{update.message.text}" from "{user_id}"')
    stickers_folder = os.path.join(os.path.curdir, 'TgBotAPI/stickers')
    sticker_list = os.listdir(stickers_folder)
    sticker = random.choice(sticker_list)
    with open(os.path.join(stickers_folder, sticker), 'rb') as s:
        context.bot.sendSticker(user_id, sticker=s)
    text = (
        f'Я не знаю что ответить на "{update.message.text}"!'
    )
    context.bot.send_message(user_id, text=text)
