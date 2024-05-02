from telegram import Update
from datetime import datetime

from utils.reply_text import reply_text
from utils.send_task import send_task

async def transfer(update: Update, context) -> None:
    """Sends transfer request"""
    instruct_text = "/transfer [Sol Amount] [Wallet Address]"
    example_text = "Example: /transfer 5 0xAABBCCDDD"
    user_id = update.message.chat.id

    args = context.args

    if len(args) == 0:
        await reply_text(update, f"{instruct_text}\n{example_text}")
        return

    if len(args) != 2:
        await reply_text(
            update,
            "Invalid arguments for /sell command.\n" f"{instruct_text}\n{example_text}",
        )
        return

    solAmount, address = args
    # TODO CheckValidAddress(address):
    current_time = datetime.now().isoformat()
    user_first_name = update.message.chat.first_name

    await reply_text(
        update,
        f"Queuing Transfer: {user_first_name} transfering {solAmount} to {address}",
    )
    await send_task("Transfer", str(user_id), current_time, address, solAmount)
