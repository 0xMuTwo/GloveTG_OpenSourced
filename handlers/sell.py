from telegram import Update
from datetime import datetime

from utils.reply_text import reply_text
from utils.send_task import send_task
async def sell(update: Update, context) -> None:
    """Sends sell request"""
    instruct_text = "/sell [percent] [token address]"
    example_text = "Example: /sell 50 0xAABBCCDDD"
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

    percent, address = args

    if "%" in percent:
        percent = percent.replace("%", "")
    try:
        percent = float(percent)
    except ValueError:
        await reply_text(
            update, "Invalid Percentage:\n" f"{instruct_text}\n{example_text}"
        )
        return
    if not percent > 0:
        await reply_text(
            update, "Error: Number Below 0\n" f"{instruct_text}\n{example_text}"
        )
        return
    # TODO create CheckValidAddress
    current_time = datetime.now().isoformat()
    user_first_name = update.message.chat.first_name

    await reply_text(
        update, f"Queuing Order: {user_first_name} selling {percent}% of {address}"
    )
    await send_task("Sell", str(user_id), current_time, address, percent)
