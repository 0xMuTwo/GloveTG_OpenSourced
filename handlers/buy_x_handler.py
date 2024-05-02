
from enum import Enum
from telegram import (
    Update,
    ForceReply,
)

from telegram.ext import (
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
)
from datetime import datetime


from utils.reply_text import reply_text
from utils.send_message import send_message_context
from utils.send_task import send_task


class States(Enum):
    AWAIT_BUY_AMOUNT = 1  # User is expected to enter an amount after "Buy X SOL"

async def ask_for_buy_amount(update: Update, context) -> States:
    # Send a new message to the user, asking for the amount of SOL they wish to buy.
    query = update.callback_query
    await query.answer()  # This is important to give feedback to the user's button press action.
    await send_message_context(
            context, query.message.chat_id, 'Please reply with the amount of SOL you wish to buy:', reply_markup=ForceReply(selective=True)
        )
    # Store the original message ID to potentially delete it later.
    context.user_data['original_message_id'] = query.message.message_id
    
    return States.AWAIT_BUY_AMOUNT


async def buy_amount_received(update: Update, context) -> int:
    user_data = context.user_data
    sol_amount = update.message.text.strip()
    try:
        sol_amount_float = float(sol_amount)
        assert sol_amount_float > 0
    except (ValueError, AssertionError):
        await reply_text(update, "Invalid amount. Press button and try again.")
        return ConversationHandler.END

    token_address = user_data.get("TokenAddress")
    if token_address:
        user_first_name = update.message.chat.first_name
        user_id = update.message.chat.id
        current_time = datetime.now().isoformat()
        await reply_text(update, f"Queuing Order: {user_first_name} buying {sol_amount} SOL of {token_address}")
        await send_task("Buy", str(user_id), current_time, token_address, sol_amount)
    else:
        await reply_text(update, "No token address found. Please start the process again by sending the token address.")

    return ConversationHandler.END

buy_x_sol_conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(ask_for_buy_amount, pattern='^Buy_X_SOL$')],
    states={
        States.AWAIT_BUY_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, buy_amount_received)],
    },
    fallbacks=[],
)