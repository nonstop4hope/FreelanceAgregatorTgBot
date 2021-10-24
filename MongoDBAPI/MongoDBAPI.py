import logging

from pymongo import MongoClient
from MongoDBAPI.models import TgUser

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class Mongod(MongoClient):

    db_name = 'FreelanceAgregator'
    tg_users_collection_name = 'TgBotUsers'
    habr_data_collection_name = 'HabrData'

    def __init__(self):
        super().__init__()

    def check_existing(self, user_id) -> None:
        collection = self[Mongod.db_name][Mongod.tg_users_collection_name]
        if collection.find_one({'_id': user_id}):
            return True

    def get_last_task(self, limit):
        if isinstance(limit, int):
            collection = self[Mongod.db_name][Mongod.habr_data_collection_name]
            tasks = collection.find().sort('_id', -1).limit(limit)
            result_list = []
            for task in tasks:
                result_list.append(task)
            return reversed(result_list)

    def add_user_to_db(self, user_data: TgUser) -> None:

        collection = self[Mongod.db_name][Mongod.tg_users_collection_name]

        json_to_db = {
            '_id': user_data.id,
            'development': user_data.development,
            'testing': user_data.testing,
            'administration': user_data.administration,
            'design': user_data.design,
            'content': user_data.content,
            'marketing': user_data.marketing,
            'various': user_data.various
        }

        if collection.find_one({'_id': user_data.id}):
            return False
        else:
            return collection.insert_one(json_to_db)

    def delete_user(self, user_id) -> None:
        collection = self[Mongod.db_name][Mongod.tg_users_collection_name]
        collection.delete_one({'_id': user_id})

    def get_current_state(self, user_id):
        collection = self[Mongod.db_name][Mongod.tg_users_collection_name]
        current_state = collection.find_one({'_id': user_id})
        true_items = []
        if current_state:
            for item in current_state.keys():
                if current_state.get(item) == True:
                    true_items.append(item)
            result = []
            for item in true_items:
                if item == 'development':
                    result.append('Разработка')
                if item == 'testing':
                    result.append('Тестирование')
                if item == 'administration':
                    result.append('Администрирование')
                if item == 'design':
                    result.append('Дизайн')
                if item == 'marketing':
                    result.append('Маркетинг')
                if item == 'various':
                    result.append('Разное')
                if item == 'content':
                    result.append('Контект')
            return result

    def update_state(self, user_id, item_name) -> None:
        collection = self[Mongod.db_name][Mongod.tg_users_collection_name]
        current_state = collection.find_one({'_id': user_id})
        if current_state.get(item_name):
            collection.update(
                {'_id': user_id},
                {"$set": {item_name: False}}
            )
        else:
            collection.update(
                {'_id': user_id},
                {"$set": {item_name: True}}
            )


