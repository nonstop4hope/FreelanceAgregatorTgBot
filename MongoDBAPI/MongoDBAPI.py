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
            '_id': user_data.id
        }

        if collection.find_one({'_id': user_data.id}):
            return False
        else:
            return collection.insert_one(json_to_db)

    def get_current_state(self, user_id) -> None:
        collection = self[Mongod.db_name][Mongod.tg_users_collection_name]
        return collection.find_one({'_id': user_id})
