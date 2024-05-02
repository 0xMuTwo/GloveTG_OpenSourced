#!/usr/bin/env python
# pylint: disable=import-error,unused-argument
"""
Telegram Interface for Glove Protocol.
"""

# Standard Library Imports
import asyncio, re, json, logging, httpx, os
from enum import Enum
from http import HTTPStatus

# Third Party
import uvicorn
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response, JSONResponse

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    ForceReply,
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
)

# Local
from modules.MsgMiddleware import reply_text, send_message_tgapp, log_outgoing_messages
from modules.callWhisper import call_whisper
from modules.callTokenSpy import token_spy_call
from handlers import setup_handlers

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Define configuration constants
URL = os.getenv("URL")
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT", 8000))
TOKEN = os.getenv("TOKENAPI")
INTERNAL_GLOVELANE = os.getenv("INTERNAL_GLOVELANE_URL")

http_client = httpx.AsyncClient()  # Initialize client globally, so it's reused.



async def plain_text(update: Update, context) -> None:
    """Handles Plain Text. Sends to GPT, unless we think it's a contract"""
    # TODO this can be further refactored, seperate these concerns bro
    user_id = update.message.chat.id
    user_text = update.message.text.strip()
    user_data = context.user_data
    # If user_text is 44 characters with no spaces, or special characters, call token spy.
    if re.fullmatch(r"^[A-Za-z0-9]{44}$", user_text):
        token_answer = await token_spy_call(user_text)
        if token_answer == "Invalid Token Address":
            return await reply_text(update, "I can't find that address, try checking again.")
        user_data["TokenAddress"] = user_text
        keyboard = [
        [InlineKeyboardButton("Cancel", callback_data="Cancel_TokenSpy")],
        [
            InlineKeyboardButton("Buy 1.0 SOL", callback_data="Buy_1_SOL"),
            InlineKeyboardButton("Buy 5.0 SOL", callback_data="Buy_5_SOL"),
            InlineKeyboardButton("Buy X SOL", callback_data="Buy_X_SOL"),
        ],
     ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await reply_text(update, token_answer, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True, reply_markup=reply_markup)
        try:
            await context.bot.delete_message(chat_id=user_id, message_id=update.message.message_id)
        except Exception as e:
            print(f"Failed to delete the original message: {e}")
    else:
        whisper_response = await call_whisper(user_text, user_id)
        await reply_text(update, whisper_response)
    return

async def notify(request: Request) -> Response:
    """Handle custom updates."""
    try:
        # Extract the JSON payload directly from the request object
        data = await request.json()
    except json.JSONDecodeError:
        return PlainTextResponse(
            status_code=HTTPStatus.BAD_REQUEST, content="Could not load JSON."
        )
    user_id = data.get("user_id")
    message = data.get("message")
    parse_mode_str = data.get("parse_mode", "HTML")

    parse_mode_mapping = {
        "MARKDOWN": ParseMode.MARKDOWN,
        "MARKDOWN_V2": ParseMode.MARKDOWN_V2,
        "HTML": ParseMode.HTML,
    }

    parse_mode = parse_mode_mapping.get(parse_mode_str, ParseMode.HTML)
    # Now we can use the application instance from the state provided by request.app.state
    telegram_application = request.app.state.telegram_application
    disable_web_page_preview = True
    try:
        await send_message_tgapp(
            telegram_application, user_id, message, parse_mode, disable_web_page_preview
        )
    except Exception as exc:
        logger.error(f"Failed to send message: {exc}")
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content=f"Failed to send message due to an error: {exc}",
        )

    return JSONResponse({"ok": True}, status_code=HTTPStatus.OK)

async def main() -> None:
    """Set up PTB application and a web application for handling the incoming requests."""
    # Here we set updater to None because we want our custom webhook server to handle the updates
    # and hence we don't need an Updater instance
    application = (
        Application.builder()
        .token(TOKEN)
        .updater(None)
        .build()
    )
    starlette_app = Starlette()
    starlette_app.state.telegram_application = application

    application.add_handler(
        MessageHandler(filters.ALL, log_outgoing_messages), group=-1
    )

    setup_handlers(application)
    # catch plain text
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, plain_text))


    # Pass webhook settings to telegram
    await application.bot.set_webhook(
        url=f"{URL}/telegram", allowed_updates=Update.ALL_TYPES
    )

    # Set up webserver
    async def telegram(request: Request) -> Response:
        """Handle incoming Telegram updates by putting them into the `update_queue`"""
        await application.update_queue.put(
            Update.de_json(data=await request.json(), bot=application.bot)
        )
        return Response()

    async def health(_: Request) -> PlainTextResponse:
        """For the health endpoint, reply with a simple plain text message."""
        return PlainTextResponse(content="The bot is still running fine :)")

    starlette_app.add_route("/telegram", telegram, methods=["POST"])
    starlette_app.add_route("/healthcheck", health, methods=["GET"])
    starlette_app.add_route("/notify", notify, methods=["POST"])

    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=starlette_app,
            port=PORT,
            use_colors=False,
            host=HOST,
        )
    )

    # Run application and webserver together
    async with application:
        await application.start()
        await webserver.serve()
        await application.stop()
        await http_client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
