import logging, httpx
from telegram import Update

whisper_ip = "http://12.123.1.22:8000/"

logger = logging.getLogger(__name__)

http_client = httpx.AsyncClient()

async def send_message_context(context, user_id, message, parse_mode=None, disable_web_page_preview=None, reply_markup=None):
    try:
        print("Service Lv Messages: ",message)
        msg_response = await context.bot.send_message(
            chat_id=user_id,
            text=message,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup
        )

        url = whisper_ip + 'input_message'
        headers = {"Content-Type": "application/json"}
        payload = {
            "message": message,
            "user_id": str(user_id),
            "platform": "Telegram",
            "type": "Service_Response"
        }
        response = await http_client.post(url, headers=headers, json=payload)
        logger.info(f"Service MSG sent. Database Response: {response}")
        return msg_response
    except Exception as e:
        # Log the error with exception information
        logging.error('Error sending message to chat', user_id, e, exc_info=True)