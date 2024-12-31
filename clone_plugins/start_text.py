import os
import json
from pyrogram import Client, filters

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

# Command to set custom start text (Owner only)
@Client.on_message(filters.command("start_text") & filters.private)
async def set_start_text(client, message):
    if message.from_user.id != 7357726710:  # Replace with your Telegram ID
        await message.reply("🚫 You are not authorized to use this command.")
        return

    if len(message.command) < 2:
        await message.reply("⚠️ Please provide the new start text.\n\nUsage: `/start_text <new_text>`")
        return

    new_text = " ".join(message.command[1:])

    if not new_text.strip():
        await message.reply("⚠️ The start text cannot be empty. Please provide valid text.")
        return

    if len(new_text) > 4096:
        await message.reply("⚠️ The start text is too long. Please provide a shorter text.")
        return

    save_start_text(client.me.id, new_text)  # Save the start text under this bot's unique ID
    await message.reply(f"✅ Start text updated to:\n\n`{new_text}`")

# Command to display the current start text
@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    start_text = load_start_text(client.me.id)  # Load the start text for this bot
    await message.reply(
        start_text.format(message.from_user.first_name, client.me.first_name),
        disable_web_page_preview=True
    )