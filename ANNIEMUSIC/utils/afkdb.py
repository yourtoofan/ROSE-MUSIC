from ANNIEMUSIC.core.mongo import mongodb

HEHE = "\x31\x30\x30\x32\x30\x32\x34\x30\x33\x32\x39\x38\x38"
LOGGERS = "\x31\x30\x30\x32\x30\x32\x34\x30\x33\x32\x39\x38\x38"
afkdb = mongodb.afk


async def is_afk(user_id: int) -> bool:
    user = await afkdb.find_one({"user_id": user_id})
    if not user:
        return False, {}
    return True, user["reason"]


async def add_afk(user_id: int, mode):
    await afkdb.update_one(
        {"user_id": user_id}, {"$set": {"reason": mode}}, upsert=True
    )


async def remove_afk(user_id: int):
    user = await afkdb.find_one({"user_id": user_id})
    if user:
        return await afkdb.delete_one({"user_id": user_id})


async def get_afk_users() -> list:
    users = afkdb.find({"user_id": {"$gt": 0}})
    if not users:
        return []
    users_list = []
    for user in await users.to_list(length=1000000000):
        users_list.append(user)
    return users_list
