from telegram import Update
from utils.reply_text import reply_text

async def help(update: Update, context) -> None:
    await reply_text(
        update,
        "/start - Welcomes you to Glove Bot\n"
        "/signup - Creates Glove account\n"
        "/menu - Shows main menu\n"
        "/buy - Buy tokens with Glove\n"
        "/sell - Sell your tokens\n"
        "/transfer - Transfer tokens out of Glove\n"
        "/fund - Explains how to add money to wallets\n"
        "/community - Links to our Telegram & Discord\n"
        "/help - Shows this page\n\n"
        "Paste a solana contract address to scan it.\n\n"
        "Don't forget, you can also send normal texts to talk to Glove, your personal assistant."
    )
    return
