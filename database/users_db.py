import datetime
from datetime import timedelta
import pytz
import motor.motor_asyncio
import logging
from info import DB_URL, DB_NAME, TIMEZONE, VERIFY_EXPIRE

logger = logging.getLogger(__name__)

client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
mydb = client[DB_NAME]


class Database:
    def __init__(self):
        self.users = mydb.users
        self.blocked_users = mydb.blocked_users
        self.blocked_channels = mydb.blocked_channels
        self.files = mydb.files
        self.refer_collection = mydb.refers 
        self.misc = mydb.misc
        self.verify_id = mydb.verify_id
        self.protected_links = mydb.protected_links

    # ---------------- USER ---------------- #

    def new_user(self, id, name):
        return {"id": int(id), "name": name}

    async def add_user(self, id, name):
        if not await self.is_user_exist(id):
            await self.users.insert_one(self.new_user(id, name))

    async def is_user_exist(self, id):
        return bool(await self.users.find_one({'id': int(id)}))

    async def get_user(self, user_id):
        return await self.users.find_one({"id": int(user_id)})

    # ---------------- VERIFY SYSTEM ---------------- #

    async def get_notcopy_user(self, user_id):
        user_id = int(user_id)
        user = await self.misc.find_one({"user_id": user_id})

        tz = pytz.timezone(TIMEZONE)

        if not user:
            default = {
                "user_id": user_id,
                "last_verified": datetime.datetime(2000, 1, 1, tzinfo=tz),
                "second_time_verified": datetime.datetime(2000, 1, 1, tzinfo=tz),
            }
            await self.misc.insert_one(default)
            return default

        return user

    async def update_notcopy_user(self, user_id, value: dict):
        return await self.misc.update_one(
            {"user_id": int(user_id)},
            {"$set": value},
            upsert=True
        )

    # ✅ FIXED (TIMEZONE SAFE)
    async def is_user_verified(self, user_id):
        user = await self.get_notcopy_user(user_id)

        tz = pytz.timezone(TIMEZONE)
        now = datetime.datetime.now(tz)

        last_verified = user.get("last_verified")

        if last_verified is None:
            return False

        if last_verified.tzinfo is None:
            last_verified = pytz.utc.localize(last_verified)

        last_verified = last_verified.astimezone(tz)

        # ✅ VERIFY_EXPIRE BASED (BEST FIX)
        diff = (now - last_verified).total_seconds()

        return diff < VERIFY_EXPIRE

    # ✅ FIXED SECOND VERIFY LOGIC
    async def use_second_shortener(self, user_id):
        user = await self.get_notcopy_user(user_id)

        tz = pytz.timezone(TIMEZONE)
        now = datetime.datetime.now(tz)

        last_verified = user.get("last_verified")
        second_verified = user.get("second_time_verified")

        if not last_verified or not second_verified:
            return False

        if last_verified.tzinfo is None:
            last_verified = pytz.utc.localize(last_verified)

        if second_verified.tzinfo is None:
            second_verified = pytz.utc.localize(second_verified)

        last_verified = last_verified.astimezone(tz)
        second_verified = second_verified.astimezone(tz)

        # যদি verify expire হয়ে যায়
        if (now - last_verified).total_seconds() > VERIFY_EXPIRE:
            return second_verified < last_verified

        return False

    # ---------------- VERIFY ID ---------------- #

    async def create_verify_id(self, user_id: int, hash, file_id=None):
        return await self.verify_id.insert_one({
            "user_id": user_id,
            "hash": hash,
            "verified": False,
            "file_id": file_id,
            "created_at": datetime.datetime.utcnow()
        })

    async def get_verify_id_info(self, user_id: int, hash):
        return await self.verify_id.find_one({
            "user_id": user_id,
            "hash": hash
        })

    async def update_verify_id_info(self, user_id, hash, value: dict):
        return await self.verify_id.update_one(
            {"user_id": user_id, "hash": hash},
            {"$set": value}
        )

    # ---------------- PREMIUM ---------------- #

    async def has_premium_access(self, user_id):
        user = await self.get_user(user_id)

        if not user:
            return False

        expiry = user.get("expiry_time")

        if not expiry:
            return False

        # ✅ FIXED TIME CHECK
        now = datetime.datetime.utcnow()

        if expiry > now:
            return True

        # expire হয়ে গেলে remove
        await self.users.update_one(
            {"id": int(user_id)},
            {"$set": {"expiry_time": None}}
        )
        return False

    # ---------------- BAN ---------------- #

    async def is_user_blocked(self, user_id: int) -> bool:
        return await self.blocked_users.find_one({"user_id": int(user_id)}) is not None

    async def block_user(self, user_id: int, reason="No reason"):
        await self.blocked_users.update_one(
            {"user_id": int(user_id)},
            {"$set": {
                "user_id": int(user_id),
                "reason": reason,
                "blocked_at": datetime.datetime.utcnow()
            }},
            upsert=True
        )

    async def unblock_user(self, user_id: int):
        await self.blocked_users.delete_one({"user_id": int(user_id)})


db = Database()
