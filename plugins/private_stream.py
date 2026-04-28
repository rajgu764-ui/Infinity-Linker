import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from info import URL, BIN_CHANNEL, CHANNEL, FSUB, MAX_FILES
from database.users_db import db
from web.utils.file_properties import get_hash
from plugins.check_verification import av_x_verification
from utils import temp, get_size
from plugins.utils import is_user_allowed, is_user_joined
from Script import script


@Client.on_message(filters.private & (filters.document | filters.video | filters.audio), group=4)
async def private_receive_handler(c: Client, m: Message):

    user_id = m.from_user.id

    # ✅ FSUB FIX
    if FSUB and not await is_user_joined(c, m):
        await m.reply_text("⚠️ Please join our channel first to use this bot!")
        return

    # ✅ BAN CHECK
    if await db.is_user_blocked(user_id):
        await m.reply_text("🚫 You are banned from using this bot!\nContact admin: @ratul1277")
        return

    # ✅ LIMIT CHECK
    if not await db.has_premium_access(user_id):
        is_allowed, remaining_time = await is_user_allowed(user_id)
        if not is_allowed:
            await m.reply_text(
                f"🚫 You already sent {MAX_FILES} files!\n⏳ Try again after {remaining_time} seconds."
            )
            return

    # ✅ VERIFICATION (only text → file skip)
    if not await db.has_premium_access(user_id):
        if m.text:
            verified = await av_x_verification(c, m)
            if not verified:
                return

    # ✅ FILE
    file = m.document or m.video or m.audio
    file_name = file.file_name if file.file_name else f"Infinity_{int(time.time())}.mkv"
    file_size = get_size(file.file_size)

    try:
        forwarded = await m.forward(chat_id=BIN_CHANNEL)

        hash_str = get_hash(forwarded)

        stream = f"{URL}watch/{forwarded.id}/{file_name}?hash={hash_str}"
        download = f"{URL}{forwarded.id}?hash={hash_str}"
        file_link = f"https://t.me/{temp.U_NAME}?start=file_{forwarded.id}"

        await db.files.insert_one({
            "user_id": user_id,
            "file_name": file_name,
            "file_size": file_size,
            "file_id": forwarded.id,
            "hash": hash_str,
            "timestamp": time.time()
        })

        await forwarded.reply_text(
            f"👤 User: [{m.from_user.first_name}](tg://user?id={user_id})\n"
            f"🆔 ID: {user_id}\n"
            f"🔗 Stream: {stream}",
            disable_web_page_preview=True
        )

        await m.reply_text(
            script.CAPTION_TXT.format(CHANNEL, file_name, file_size, stream, download),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("• STREAM •", url=stream),
                    InlineKeyboardButton("• DOWNLOAD •", url=download)
                ],
                [
                    InlineKeyboardButton("• GET FILE •", url=file_link),
                    InlineKeyboardButton("• DELETE •", callback_data=f"deletefile_{forwarded.id}")
                ],
                [
                    InlineKeyboardButton("• CLOSE •", callback_data="close_data")
                ]
            ])
        )

    except FloodWait as e:
        await asyncio.sleep(e.value)
        await c.send_message(BIN_CHANNEL, f"⚠️ FloodWait: {e.value}s")
