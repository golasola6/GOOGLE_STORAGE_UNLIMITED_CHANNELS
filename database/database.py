import motor.motor_asyncio
from config import DB_URI, DB_NAME, URL_SHORTENR_WEBSITE, URL_SHORTNER_WEBSITE_API

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.user
        self.lazyshortner = self.db.lazyshortner
        self.locked_files = self.db.locked_files
        self.user_joins = self.db.user_joins

    def new_user(self, id):
        return dict(
            _id=int(id),                                   
            file_id=None,
            caption=None
        )
    
    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'_id': int(user_id)})
    
    async def set_thumbnail(self, id, file_id):
        await self.col.update_one({'_id': int(id)}, {'$set': {'file_id': file_id}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('file_id', None)

    async def set_caption(self, id, caption):
        await self.col.update_one({'_id': int(id)}, {'$set': {'caption': caption}})

    async def get_caption(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('caption', None)
        
    async def set_forward(self, id, forward):
        print(forward)
        z = await self.col.update_one({'_id': int(id)}, {'$set': {'forward_id': forward}})
        print(z)

    async def get_forward(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('forward_id', None)
    
    async def set_lazy_target_chat_id(self, id, target_chat_id):
        z = await self.col.update_one({'_id': int(id)}, {'$set': {'lazy_target_chat_id': target_chat_id}})
        print(z)

    async def get_lazy_target_chat_id(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('lazy_target_chat_id', None)
    
    async def update_settings(self, id, settings):
        await self.lazyshortner.update_one({'id': int(id)}, {'$set': {'settings': settings}})
    
    async def get_settings(self, id):
        default = {
            'shortlink': URL_SHORTENR_WEBSITE,
            'shortlink_api': URL_SHORTNER_WEBSITE_API,
        }
        chat = await self.lazyshortner.find_one({'id':int(id)})
        if chat:
            return chat.get('settings', default)
        return default

    # async def save_locked_file(self, file_id, channel_id):
    #     data = {
    #         "file_id" : file_id,
    #         "channel_id" : channel_id,
    #     }
    #     await self.locked_files.insert_one(data)

    # async def get_locked_files(self, file_id):
    #     lazy_file = await self.locked_files.find_one({"file_id" : file_id})
    #     return lazy_file.get("channel_id", None)

# -----------------------------------------------------------
# -----------------------------------------------------------
    # async def save_locked_file(self, file_id, channel_id):
    #     data = {
    #         "file_id": file_id,
    #         "channel_id": channel_id,
    #     }
    #     await self.locked_files.insert_one(data)  # simple insert


    # async def get_locked_files(self, file_id):
    #     lazy_file = await self.locked_files.find_one({"file_id": file_id})

    #     if not lazy_file:
    #         return None  # safe fallback

    #     return lazy_file.get("channel_id")
    
    # async def get_locked_channels(self):
    #     cursor = self.locked_files.find({}, {"channel_id": 1, "_id": 0})
    #     channels = []
    #     async for doc in cursor:
    #         channels.append(doc["channel_id"])
    #     return channels

# ------------------------------------------------------------
# ------------------------------------------------------------
    async def save_locked_file(self, file_id, channel_ids: list):
        await self.locked_files.update_one(
            {"file_id": file_id},
            {
                "$addToSet": {
                    "channel_ids": {"$each": channel_ids}
                }
            },
            upsert=True
        )
        
    async def get_locked_files(self, file_id):
        doc = await self.locked_files.find_one(
            {"file_id": file_id},
            {"_id": 0, "channel_ids": 1}
        )

        if not doc:
            return []

        return doc.get("channel_ids", [])

    async def get_locked_channels(self):
        cursor = self.locked_files.find({}, {"_id": 0, "channel_ids": 1})
        channels = set()

        async for doc in cursor:
            channels.update(doc.get("channel_ids", []))

        return list(channels)
    async def save_user_join(self, user_id, channel_id):
        await self.user_joins.update_one(
            {"user_id": user_id},
            {
                "$addToSet": {
                    "channels": channel_id
                }
            },
            upsert=True
        )
    async def get_user_joins(self, user_id):
        doc = await self.user_joins.find_one(
            {"user_id": user_id},
            {"_id": 0, "channels": 1}
        )
        if not doc:
            return []
        return doc.get("channels", [])

db = Database(DB_URI, DB_NAME)






# import motor.motor_asyncio
# from config import DB_URI, DB_NAME

# class Database:

#     def __init__(self, uri, database_name):
#         self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
#         self.db = self._client[database_name]
#         self.col = self.db.user
            
#     # async def present_user(user_id : int):
#     #     found = user_data.find_one({'_id': user_id})
#     #     return bool(found)

#     # async def add_user(user_id: int):
#     #     user_data.insert_one({'_id': user_id})
#     #     return
    
#     def new_user(self, id):
#         return dict(
#             _id=int(id),                                   
#             file_id=None,
#             caption=None
#         )

#     async def add_user(self, user_id: int):
#         self.col.insert_one({'_id': user_id})
#         return
    
#     async def is_user_exist(self, id):
#         user = await self.col.find_one({'_id': int(id)})
#         return bool(user)
    
#     async def present_user(self, user_id : int):
#         found = self.col.find_one({'_id': user_id})
#         return bool(found)

#     async def total_users_count(self):
#         count = await self.col.count_documents({})
#         return count
    
    
#     async def get_all_users(self):
#         all_users = self.col.find({})
#         return all_users
    
#     async def full_userbase(self):
#         user_docs = self.col.find({})
#         user_ids = []
        
#         async for doc in user_docs:  # Correctly iterating over the async cursor
#             user_ids.append(doc['_id'])
        
#         return user_ids
    
#     async def delete_user(self, user_id):
#         await self.col.delete_many({'_id': int(user_id)})
    
    
#     async def set_thumbnail(self, id, file_id):
#         await self.col.update_one({'_id': int(id)}, {'$set': {'file_id': file_id}})

#     async def get_thumbnail(self, id):
#         user = await self.col.find_one({'_id': int(id)})
#         return user.get('file_id', None)

#     async def set_caption(self, id, caption):
#         await self.col.update_one({'_id': int(id)}, {'$set': {'caption': caption}})

#     async def get_caption(self, id):
#         user = await self.col.find_one({'_id': int(id)})
#         return user.get('caption', None)

#     # async def full_userbase():
#     #     user_docs = user_data.find()
#     #     user_ids = []
#     #     for doc in user_docs:
#     #         user_ids.append(doc['_id'])
            
#     # return user_ids

#     async def delete_user(self, user_id):
#         await self.col.delete_many({'_id': int(user_id)})
    
#     # def addthumb(chat_id, file_id):
#     #     user_data.update_one({"_id": chat_id}, {"$set": {"file_id": file_id}})


#     # def set_thumbnail(id, file_id):
#     #     user_data.update_one({'id': int(id)}, {'$set': {'file_id': file_id}})


#     # async def get_thumbnail(id):
#     #     try:
#     #         thumbnail = user_data.find_one({'id': int(id)})
#     #         if thumbnail:
#     #             return thumbnail.get('file_id')
#     #         else:
#     #             return None
#     #     except Exception as e:
#     #         print(e)
#     # # Born to make history @LazyDeveloper ! => Remember this name forever <=

#     # async def set_caption(id, caption):
#     #     user_data.update_one({'id': int(id)}, {'$set': {'caption': caption}})

#     # async def get_caption(id):
#     #     user = user_data.find_one({'id': int(id)})
#     #     return user.get('caption', None)

#     # async def get_lazy_thumbnail(id):
#     #     user = user_data.find_one({'id': int(id)})
#     #     return user.get('thumbnail', None)

#     # async def get_lazy_caption(id):
#     #     user = user_data.find_one({'id': int(id)})
#     #     return user.get('lazy_caption', None)

#     # async def set_lazy_thumbnail(id, thumbnail):
#     #     user_data.update_one({'id': id}, {'$set': {'thumbnail': thumbnail}})

#     # Born to make history @LazyDeveloper ! => Remember this name forever <=
# db = Database(DB_URI, DB_NAME)
