from telegram import Update
from datetime import datetime

from utils.reply_text import reply_text
from utils.send_task import send_task

async def buy(update: Update, context) -> None:
    """Sends buy request"""
    instruct_text = "/buy [sol amount] [token address]."
    example_text = "Example: /buy 3.2 0xAABBCCDDD\n\nYou can also send the contract address as a message!"
    user_id = update.message.chat.id
    args = context.args
    if len(args) == 0:
        await reply_text(update, f"{instruct_text}\n{example_text}")
        return

    if len(args) != 2:
        await reply_text(
            update,
            "Invalid arguments for /buy command.\n"
            f"{instruct_text}\n"
            f"{example_text}",
        )
        return

    amount, address = args
    try:
        amount = float(amount)
    except ValueError:
        await reply_text(
            update, "Invalid Number:\n" f"{instruct_text}\n" f"{example_text}"
        )
        return
    if not amount > 0:
        await reply_text(
            update, "Error: Number Below 0\n" f"{instruct_text}\n" f"{example_text}"
        )
    # TODO create checkValidAddress function
    current_time = datetime.now().isoformat()
    user_first_name = update.message.chat.first_name
    await reply_text(
        update, f"Queuing Order: {user_first_name} buying {amount} SOL of {address}"
    )
    await send_task("Buy", str(user_id), current_time, address, amount)
