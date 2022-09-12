# Made with python3
# (C) @MrProgrammer72
# Copyright permission under MIT License
# All rights reserved by MrProgrammer
# License -> https://github.com/MrProgrammer72/Telegraph-Uploader-Bot/blob/main/LICENSE

import os
import time
import math
import json
import string
import random
import traceback
import asyncio
import datetime
import aiofiles
from random import choice 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid, UserNotParticipant, UserBannedInChannel
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid
from telegraph import upload_file
from database import Database


UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "")
BOT_OWNER = int(os.environ["BOT_OWNER"])
DATABASE_URL = os.environ["DATABASE_URL"]
db = Database(DATABASE_URL, "FnTelegraphBot")

Bot = Client(
    "Telegraph Uploader Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
)

START_TEXT = """**ʜᴇʟʟᴏ {} 😇
ɪ ᴀᴍ ꜱᴍᴀʟʟ ᴍᴇᴅɪᴀ ᴏʀ ꜰɪʟᴇ ᴛᴏ ᴛᴇʟᴇɢʀᴀ.ᴘʜ ʟɪɴᴋ ᴜᴘʟᴏᴀᴅᴇʀ ʙᴏᴛ.**

>> `ɪ ᴄᴀɴ ᴄᴏɴᴠᴇʀᴛ ᴜɴᴅᴇʀ 5ᴍʙ ᴘʜᴏᴛᴏ ᴏʀ ᴠɪᴅᴇᴏ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ.`

ᴍᴀᴅᴇ ʙʏ 🖤 [ᴇxᴘᴏʀᴛ_ɢᴀʙʙᴀʀ](https://telegram.me/export_gabbar)"""

HELP_TEXT = """**ʜᴇʏ, ꜰᴏʟʟᴏᴡ ᴛʜᴇꜱᴇ ꜱᴛᴇᴘꜱ:**

➠ ᴊᴜꜱᴛ ɢɪᴠᴇ ᴍᴇ ᴀ ᴍᴇᴅɪᴀ ᴜɴᴅᴇʀ 5ᴍʙ
➠ ᴛʜᴇɴ ɪ ᴡɪʟʟ ᴅᴏᴡɴʟᴏᴀᴅ ɪᴛ
➠ ɪ ᴡɪʟʟ ᴛʜᴇɴ ᴜᴘʟᴏᴀᴅ ɪᴛ ᴛᴏ ᴛʜᴇ ᴛᴇʟᴇɢʀᴀ.ᴘʜ ʟɪɴᴋ

**ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ**

/start - ᴄʜᴇᴄᴋɪɴɢ ʙᴏᴛ ᴏɴʟɪɴᴇ 
/help - ꜰᴏʀ ᴍᴏʀᴇ ʜᴇʟᴘ
/about - ꜰᴏʀ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴍᴇ
/Status - ꜰᴏʀ ʙᴏᴛ ᴜᴘᴅᴀᴛᴇꜱ

ᴍᴀᴅᴇ ʙʏ 🤍 [ᴇxᴘᴏʀᴛ_ɢᴀʙʙᴀʀ](https://telegram.me/export_gabbar)"""

ABOUT_TEXT = """--**ᴀʙᴏᴜᴛ ᴍᴇ**--😁

🤖 **ɴᴀᴍᴇ :** [ᴛᴇʟᴇɢʀᴀᴘʜ ᴜᴘʟᴏᴀᴅᴇʀ](https://telegram.me/{})

👨‍💻 **ᴅᴇᴠᴇʟᴏᴘᴇʀ :** [ᴍʀ.ᴘʀᴏɢᴀᴍᴍᴇʀ](https://github.com/MrProgrammer72)

🇮🇳 **ᴇᴅɪᴛᴏʀ :** [ᴇxᴘᴏʀᴛ ɢᴀʙʙᴀᴛ](https://t.me/export_gabbar)

📢 **ᴄʜᴀɴɴᴀʟ :** [ꜱᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ](https://telegram.me/myworldGJ516)

👥 **ɢʀᴏᴜᴘ :** [ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ](https://telegram.me/ADVENTURE_FAMILY)

🌐 **ꜱᴏᴜʀᴄᴇ :** [ᴄʟɪᴄᴋ ʜᴇʀᴇ](https://telegra.ph/file/9b0455dae14d5639f936d.mp4)

📝 **ʟᴀɴɢᴜᴀɢᴇ :** [ᴘʏᴛʜᴏɴ3](https://python.org)

🧰 **ꜰʀᴀᴍᴇᴡᴏʀᴋ :** [ᴘʏʀᴏɢʀᴀᴍ](https://pyrogram.org)

📡 **ꜱᴇʀᴠᴇʀ :** [ʜᴇʀᴏᴋᴜ](https://heroku.com)"""

FORCE_SUBSCRIBE_TEXT = "<code>ꜱᴏʀʀʏ ᴅᴇᴀʀ ʏᴏᴜ ᴍᴜꜱᴛ ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ ꜰᴏʀ ᴜꜱɪɴɢ ᴍᴇ ✨....</code>"

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🎧 ᴍᴜꜱɪᴄ ʙᴏᴛ 🎧', url='https://t.me/GJ516_VCPALYER_BOT'),
        ],[
        InlineKeyboardButton('ʜᴇʟᴘ ⚙', callback_data='help'),
        InlineKeyboardButton('ᴀʙᴏᴜᴛ 🔰', callback_data='about'),
        InlineKeyboardButton('ᴄʟᴏꜱᴇ ✖️', callback_data='close')
        ]]
    )

HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🎧 ᴍᴜꜱɪᴄ ʙᴏᴛ 🎧', url='https://t.me/GJ516_VCPALYER_BOT'),
        ],[
        InlineKeyboardButton('ʜᴏᴍᴇ 🏘', callback_data='home'),
        InlineKeyboardButton('ᴀʙᴏᴜᴛ 🔰', callback_data='about'),
        InlineKeyboardButton('ᴄʟᴏꜱᴇ ✖️', callback_data='close')
        ]]
    )

ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🎧 ᴍᴜꜱɪᴄ ʙᴏᴛ 🎧', url='https://t.me/GJ516_VCPALYER_BOT'),
        ],[
        InlineKeyboardButton('ʜᴏᴍᴇ 🏘', callback_data='home'),
        InlineKeyboardButton('ʜᴇʟᴘ ⚙', callback_data='help'),
        InlineKeyboardButton('ᴄʟᴏꜱᴇ ✖️', callback_data='close')
        ]]
    )


async def send_msg(user_id, message):
	try:
		await message.copy(chat_id=user_id)
		return 200, None
	except FloodWait as e:
		await asyncio.sleep(e.x)
		return send_msg(user_id, message)
	except InputUserDeactivated:
		return 400, f"{user_id} : ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ\n"
	except UserIsBlocked:
		return 400, f"{user_id} : ᴜꜱᴇʀ ɪꜱ ʙʟᴏᴄᴋᴇᴅ\n"
	except PeerIdInvalid:
		return 400, f"{user_id} : ᴜꜱᴇʀ ɪᴅ ɪɴᴠᴀʟɪᴅ\n"
	except Exception as e:
		return 500, f"{user_id} : {traceback.format_exc()}\n"


@Bot.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT.format((await bot.get_me()).username),
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    if not await db.is_user_exist(update.from_user.id):
	    await db.add_user(update.from_user.id)
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
	reply_markup=START_BUTTONS
    )


@Bot.on_message(filters.private & filters.command(["help"]))
async def help(bot, update):
    if not await db.is_user_exist(update.from_user.id):
	    await db.add_user(update.from_user.id)
    await update.reply_text(
        text=HELP_TEXT,
      	disable_web_page_preview=True,
	reply_markup=HELP_BUTTONS
    )


@Bot.on_message(filters.private & filters.command(["about"]))
async def about(bot, update):
    if not await db.is_user_exist(update.from_user.id):
	    await db.add_user(update.from_user.id)
    await update.reply_text(
        text=ABOUT_TEXT.format((await bot.get_me()).username),
        disable_web_page_preview=True,
	reply_markup=ABOUT_BUTTONS
    )


@Bot.on_message(filters.media & filters.private)
async def telegraph_upload(bot, update):
    if not await db.is_user_exist(update.from_user.id):
	    await db.add_user(update.from_user.id)
    if UPDATE_CHANNEL:
        try:
            user = await bot.get_chat_member(UPDATE_CHANNEL, update.chat.id)
            if user.status == "kicked":
                await update.reply_text(text="ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ!")
                return
        except UserNotParticipant:
            await update.reply_text(
		  text=FORCE_SUBSCRIBE_TEXT,
		  reply_markup=InlineKeyboardMarkup(
			  [[InlineKeyboardButton(text="⚙ ᴊᴏɪɴ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ ⚙", url=f"https://telegram.me/{UPDATE_CHANNEL}")]]
		  )
	    )
            return
        except Exception as error:
            print(error)
            await update.reply_text(text="ꜱᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ. ᴄᴏɴᴛᴀᴄᴛ <a href='https://telegram.me/export_gabbar'>ᴅᴇᴠᴇʟᴏᴘᴇʀ</a>.", disable_web_page_preview=True)
            return
    medianame = "./DOWNLOADS/" + "FayasNoushad/FnTelegraphBot"
    text = await update.reply_text(
        text="<code>ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴛᴏ ᴍʏ ꜱᴇʀᴠᴇʀ ...</code>",
        disable_web_page_preview=True
    )
    await bot.download_media(
        message=update,
        file_name=medianame
    )
    await text.edit_text(
        text="<code>ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴄᴏᴍᴘʟᴇᴛᴇᴅ. ɴᴏᴡ ɪ ᴀᴍ ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀ.ᴘʜ ʟɪɴᴋ ......</code>",
        disable_web_page_preview=True
    )
    try:
        response = upload_file(medianame)
    except Exception as error:
        print(error)
        await text.edit_text(
            text=f"ᴇʀʀᴏʀ :- {error}",
            disable_web_page_preview=True
        )
        return
    try:
        os.remove(medianame)
    except Exception as error:
        print(error)
        return
    await text.edit_text(
        text=f"<b>Link :-</b> <code>https://telegra.ph{response[0]}</code>\n\n<b>ᴊᴏɪɴ :-</b> @ADVENTURE_FAMILYS",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="ᴏᴘᴇɴ ʟɪɴᴋ 🇮🇳", url=f"https://telegra.ph{response[0]}"),
                    InlineKeyboardButton(text="ꜱʜᴀʀᴇ ʟɪɴᴋ 🇮🇳", url=f"https://telegram.me/share/url?url=https://telegra.ph{response[0]}")
                ],
  
                    InlineKeyboardButton(text="⚙ ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇꜱ ɢʀᴏᴜᴘ ⚙", url="https://telegram.me/ADVENTURE_FAMILYS")
                ],
                [
                    InlineKeyboardButton('🎧 ᴍᴜꜱɪᴄ ʙᴏᴛ 🎧', url='https://t.me/GJ516_VCPLAYER_BOT')
                ]
            ]
        )
    )


@Bot.on_message(filters.private & filters.command("broadcast") & filters.user(BOT_OWNER) & filters.reply)
async def broadcast(bot, update):
	broadcast_ids = {}
	all_users = await db.get_all_users()
	broadcast_msg = update.reply_to_message
	while True:
	    broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
	    if not broadcast_ids.get(broadcast_id):
	        break
	out = await update.reply_text(text=f"ʙʀᴏᴀᴅᴄᴀꜱᴛ ꜱᴛᴀʀᴛᴇᴅ! ʏᴏᴜ ᴡɪʟʟ ʙᴇ ɴᴏᴛɪꜰɪᴇᴅ ᴡɪᴛʜ ʟᴏɢ ꜰɪʟᴇ ᴡʜᴇɴ ᴀʟʟ ᴛʜᴇ ᴜꜱᴇʀꜱ ᴀʀᴇ ɴᴏᴛɪꜰɪᴇᴅ.")
	start_time = time.time()
	total_users = await db.total_users_count()
	done = 0
	failed = 0
	success = 0
	broadcast_ids[broadcast_id] = dict(total = total_users, current = done, failed = failed, success = success)
	async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
	    async for user in all_users:
	        sts, msg = await send_msg(user_id = int(user['id']), message = broadcast_msg)
	        if msg is not None:
	            await broadcast_log_file.write(msg)
	        if sts == 200:
	            success += 1
	        else:
	            failed += 1
	        if sts == 400:
	            await db.delete_user(user['id'])
	        done += 1
	        if broadcast_ids.get(broadcast_id) is None:
	            break
	        else:
	            broadcast_ids[broadcast_id].update(dict(current = done, failed = failed, success = success))
	if broadcast_ids.get(broadcast_id):
	    broadcast_ids.pop(broadcast_id)
	completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
	await asyncio.sleep(3)
	await out.delete()
	if failed == 0:
	    await update.reply_text(text=f"ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ `{completed_in}`\n\nᴛᴏᴛᴀʟ ᴜꜱᴇʀ {total_users}.\nᴛᴏᴛᴀʟ ᴅᴏɴᴇ {done}, {success} ꜱᴜᴄᴄᴇꜱꜱ ᴀɴᴅ {failed} ꜰᴀɪʟᴇᴅ.", quote=True)
	else:
	    await update.reply_document(document='broadcast.txt', caption=f"ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ  `{completed_in}`\n\nᴛᴏᴛᴀʟ ᴜꜱᴇʀ {total_users}.\nᴛᴏᴛᴀʟ ᴅᴏɴᴇ {done}, {success} ꜱᴜᴄᴄᴇꜱꜱ ᴀɴᴅ {failed} ꜰᴀɪʟᴇᴅ.")
	os.remove('broadcast.txt')


@Bot.on_message(filters.private & filters.command("status"), group=5)
async def status(bot, update):
    total_users = await db.total_users_count()
    text = "**ʙᴏᴛ ꜱᴛᴀᴛᴜꜱ**\n"
    text += f"\n**ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ:** `{total_users}`"
    await update.reply_text(
        text=text,
        quote=True,
        disable_web_page_preview=True
    )


Bot.run()
