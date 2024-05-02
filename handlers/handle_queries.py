from telegram import Update
from utils.send_task import send_task
from datetime import datetime
from utils.send_message import send_message_context


async def handle_queries(update: Update, context):
    query = update.callback_query
    if query.message:
        user_first_name = query.message.chat.first_name
        user_id = query.message.chat.id
    else:
        # Fallback if message is not present or we handle differently
        # depending on your Telegram bot logic
        user_first_name = "Unknown"
        user_id = query.from_user.id

    current_time = datetime.now().isoformat()
    token_address = context.user_data.get('TokenAddress', '')  # Safely getting the token address with a default value

    if query.data == "Cancel_TokenSpy":
        await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    elif query.data in ("Buy_1_SOL", "Buy_5_SOL"):
        sol_amount = 1 if query.data == "Buy_1_SOL" else 5
        print(f"User {query.from_user.id} requests {sol_amount} SOL of {token_address}")
        await send_message_context(context, user_id, f"Queuing Order: {user_first_name} buying {sol_amount} SOL of {token_address}")
        await send_task("Buy", str(user_id), current_time, token_address, sol_amount)
    elif query.data == "Sell":
        await query.edit_message_text(
            text=f"Sell Selected, type the amount you want to sell",
        )
    else:
        await query.edit_message_text(text=f"Selected option: {query.data}")

    await query.answer()