import os
import json
from pyrogram import Client, filters
from config import DB_URI as MONGO_URL
from pymongo import MongoClient

mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["cloned_vjbotz"]

# Default start text
CLONE_START_TXT = """<b>Hᴇʟʟᴏ {}, ᴍʏ ɴᴀᴍᴇ {}, 【ɪ ᴀᴍ ʟᴀᴛᴇꜱᴛ ᴀᴅᴠᴀɴᴄᴇᴅ】ᴀɴᴅ ᴘᴏᴡᴇʀꜰᴜʟ ꜰɪʟᴇ ꜱᴛᴏʀᴇ ʙᴏᴛ +├ᴄᴜꜱᴛᴏᴍ ᴜʀʟ ꜱʜᴏʀᴛɴᴇʀ ꜱᴜᴘᴘᴏʀᴛ┤+  ᢵᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ sᴜᴘᴘᴏʀᴛ ᢴ ᢾᴀɴᴅ ʙᴇꜱᴛ ᴜɪ ᴘᴇʀꜰᴏʀᴍᴀɴᴄᴇᢿ

ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛʜɪs ғᴇᴀᴛᴜʀᴇ ᴛʜᴇɴ ᴄʀᴇᴀᴛᴇ ʏᴏᴜʀ ᴏᴡɴ ᴄʟᴏɴᴇ ʙᴏᴛ ғʀᴏᴍ ᴍʏ <a href=https://t.me/vj_botz>ᴘᴀʀᴇɴᴛ</a></b>"""

START_TEXT_FILE = "start_texts.json"  # A single file to store start texts for all bots

# Load start text for a specific bot
def load_start_text(bot_id):
    try:
        if os.path.exists(START_TEXT_FILE):
            with open(START_TEXT_FILE, "r") as file:
                data = json.load(file)
                return data.get(str(bot_id), CLONE_START_TXT)
    except Exception as e:
        print(f"Error loading start text: {e}")
    return CLONE_START_TXT

# Save start text for a specific bot
def save_start_text(bot_id, text):
    try:
        data = {}
        if os.path.exists(START_TEXT_FILE):
            with open(START_TEXT_FILE, "r") as file:
                data = json.load(file)
        data[str(bot_id)] = text  # Save the text under the bot's unique ID
        with open(START_TEXT_FILE, "w") as file:
            json.dump(data, file)
    except Exception as e:
        print(f"Error saving start text: {e}")

@Client.on_message(filters.command("start_text") & filters.private)
async def set_start_text(client, message):
    try:
        # Get the bot owner's ID from the database
        owner = mongo_db.bots.find_one({'bot_id': client.me.id})
        owner_id = int(owner['user_id'])

        # Check if the user is authorized
        if message.from_user.id != owner_id:
            await message.reply("🚫 You are not authorized to use this command.")
            return

        # Validate the command arguments
        if len(message.command) < 2:
            await message.reply("⚠️ Please provide the new start text.\n\nUsage: `/start_text <new_text>`")
            return

        new_text = " ".join(message.command[1:]).strip()

        # Validate the new start text
        if not new_text:
            await message.reply("⚠️ The start text cannot be empty. Please provide valid text.")
            return

        if len(new_text) > 4096:
            await message.reply("⚠️ The start text is too long. Please provide a shorter text.")
            return

        # Update the start text in the database
        mongo_db.bots.update_one(
            {'bot_id': client.me.id},
            {'$set': {'start_text': new_text}}
        )

        # Confirm success
        await message.reply(f"✅ Start text updated successfully:\n\n`{new_text}`")

    except Exception as e:
        # Handle any exceptions
        await message.reply(f"❌ An error occurred: {str(e)}")
