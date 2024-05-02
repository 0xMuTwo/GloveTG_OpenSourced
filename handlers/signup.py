from telegram import Update
from datetime import datetime
from utils.send_task import send_task

async def signup(update: Update, context) -> None:
    """Signs up users"""
    user_id = update.message.chat.id
    current_time = datetime.now().isoformat()
    await send_task("Signup", str(user_id), current_time)
    return