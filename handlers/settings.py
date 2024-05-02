from telegram import Update
from datetime import datetime
from utils.send_task import send_task
from utils.reply_text import reply_text

async def settings(update: Update, context) -> None:
    """Processes settings command and allows users to update or view settings."""
    print("In settings")
    instruct_text = ("/settings view —See Current Settings\n"
                     "/settings slippage=100 —Set Slippage (in bps)\n"
                     "/settings rpc=https://enter-your.rpc/value —Set RPC")
    user_id = update.effective_chat.id  # This is the recommended way to get user_id
    current_time = datetime.now().isoformat()

    # Extract arguments from the command
    args = context.args
    

    # Check if user wants to view settings
    if len(args) == 1 and args[0].lower() == "view":
        # Use an additional 'view' parameter to signal fetching current settings
        await send_task("Settings", str(user_id), current_time, view=True)
        return
    elif len(args) == 0:
        await reply_text(update, instruct_text)
        return

    # Parse arguments and send task to update settings
    settings_kwargs = {}
    for arg in args:
        if '=' in arg:
            key, value = arg.split('=', 1)
            settings_kwargs[key] = value

    # Send task with any settings provided
    # TODO Catch silly calls like /settings rpc (with no values) 
            # or generally anything that's not in format.
    await reply_text(update, "Settings Updated.")
    await send_task("Settings", str(user_id), current_time, **settings_kwargs)

    return
