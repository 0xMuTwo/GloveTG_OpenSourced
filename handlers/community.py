from telegram import Update
from utils.reply_text import reply_text

async def community(update: Update, context) -> None:
    message_text = (
        "🚀 Meet Some Friends! 🫂\n\n"
        "Twitter: https://twitter.com/Glove\n"
        "Telegram: https://t.me/Glove\n"
        "Discord: https://discord.gg/7"
    )
    await reply_text(update, message_text)
    return
