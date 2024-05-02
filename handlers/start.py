from telegram import Update
from utils.reply_text import reply_text

from datetime import datetime

from utils.send_task import send_task

async def start(update: Update, context) -> None:
    """Display a message with instructions on how to use this bot."""

    user_first_name = update.message.chat.first_name
    user_id = update.message.chat.id
    welcome_message = f"Glove Bot is activated, {user_first_name}"
    current_time = datetime.now().isoformat()
    await reply_text(update, welcome_message)
    await send_task("UserExists", str(user_id), current_time)
    return

