from telegram import Update
from datetime import datetime
from telegram.constants import ParseMode

from utils.reply_text import reply_text
from utils.send_task import send_task

from modules.callTokenWarden import call_menu_warden

async def menu(update: Update, context) -> None:
    """Shows User the Main Menu"""
    user_id = update.message.chat.id
    menu = await call_menu_warden(str(user_id))
    await reply_text(update, menu, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)
