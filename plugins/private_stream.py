import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import VERIFY_EXPIRE, SHORTLINK_URL
from database.users_db import db


async def av_x_verification(client, message):
    user_id = message.from_user.id

    # ✅ SAFE COMMAND HANDLE (NO ERROR)
    cmd = message.command or []

    # যদি command না থাকে (file/text without command)
    if not cmd:
        return True

    # Example: /start verify_xxxxx
    if len(cmd) > 1 and cmd[1].startswith("verify_"):
        token = cmd[1].split("_", 1)[1]

        data = await db.get_verify_token(user_id)

        if not data:
            await message.reply_text("❌ Verification data not found!")
            return False

        # Token match check
        if data["token"] != token:
            await message.reply_text("❌ Invalid verification link!")
            return False

        # Expire check
        if time.time() > data["expire"]:
            await message.reply_text("⌛ Verification link expired!")
            return False

        # ✅ VERIFIED SUCCESS
        await db.update_verify_status(user_id, True)

        await message.reply_text("✅ You are successfully verified! Now send your file.")
        return True

    # 🔒 NOT VERIFIED → SEND BUTTON
    verified = await db.is_user_verified(user_id)

    if not verified:
        verify_token = str(int(time.time()))
        expire_time = time.time() + VERIFY_EXPIRE

        await db.save_verify_token(user_id, verify_token, expire_time)

        verify_link = f"https://{SHORTLINK_URL}/verify?token={verify_token}"

        await message.reply_text(
            "🔒 **You are not verified!**\n\nClick the button below to verify and continue.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Verify Now", url=verify_link)]
            ])
        )
        return False

    return True
