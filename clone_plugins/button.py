from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackContext

# /start command
def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Default Button", url="https://example.com")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome! Here are your buttons:", reply_markup=reply_markup)

# /btn1 command to add a button
def btn1(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        update.message.reply_text("Usage: /btn1 <button_text> <url>")
        return

    button_text, url = context.args[0], context.args[1]
    keyboard = [[InlineKeyboardButton(button_text, url=url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("New button added:", reply_markup=reply_markup)

# Register handlers (assuming `dispatcher` is set up)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("btn1", btn1))
