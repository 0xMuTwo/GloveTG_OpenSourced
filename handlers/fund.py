from telegram import Update 
from utils.reply_text import reply_text

async def fund(update: Update, context) -> None:
    fund_video = "https://www.youtube.com/shorts/62PQ0YHNZU"

    message_text = (
        "🚀 Getting started with Glove Wallet is super easy! 🌟\n\n"
        "1️⃣ Buy some SOL from well-known exchanges like Moonpay, Coinbase, or Binance. 🛒\n\n"
        "2️⃣ Once you've got your SOL, simply transfer it to your Glove Wallet Address. ✅\n\n"
        "Need a hand with buying? Check out this quick video on Moonpay for guidance! 🎥👇"
    )
    await reply_text(update, message_text)
    await reply_text(update, fund_video)
    return