import os
import json
import datetime
from functools import wraps
import inspect
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import uuid

load_dotenv(dotenv_path='../.env')
load_dotenv(dotenv_path='.env')

def is_running_in_docker():
    return os.path.exists('/.dockerenv')

if is_running_in_docker():
    host = 'mongo-db'
else:
    host = 'localhost'

db_url = f'mongodb://intim:intimpass@{host}:27017'
print('db_url', db_url)
client = AsyncIOMotorClient(db_url)
db = client['appdb']
image_caching_history_collection_mongodb = db['image_caching_history']


async def mogodb_get_image_uuids_for_user(user_id: int):
    """
    Query all img_uuid values for a specified user_id from the image_caching_history collection.

    :param db: MongoDB database object
    :param user_id: The user_id to filter by
    :return: List of img_uuid values
    """
    try:
        cursor = image_caching_history_collection_mongodb.find({'user_id': user_id}, {'img_uuid': 1})
        img_uuids = [doc['img_uuid'] for doc in await cursor.to_list(length=None)]
        return img_uuids
    except Exception as e:
        print(f"Error querying image UUIDs: {e}")
        return []
    
    
async def mongodb_add_image_usage_record(user_id: int, img_uuid: str, img_path=None,):
    """Insert record into MongoDB to mark the image as used"""
    await image_caching_history_collection_mongodb.insert_one({
        'user_id': user_id,
        'created_at': datetime.datetime.now(datetime.UTC),
        'img_uuid': img_uuid,
        'img_path': img_path,
    })
    
    print('Cached image is used, record added to mongodb:', user_id, img_uuid, img_path)
    

