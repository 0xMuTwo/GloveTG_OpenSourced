import logging, httpx
whisper_ip = "http://12.123.1.22:8000/"

http_client = httpx.AsyncClient()

async def reply_text(update, message, parse_mode=None, disable_web_page_preview=None, reply_markup=None):
    try:
        print("Telegram Lv Messages: ", message)
        if parse_mode:
            msg_response = await update.message.reply_text(message, parse_mode=parse_mode, disable_web_page_preview = disable_web_page_preview, reply_markup=reply_markup)
        else:
            msg_response = await update.message.reply_text(message)

        user_id = update.message.from_user.id

        url = whisper_ip + 'input_message'
        headers = {"Content-Type": "application/json"}
        payload = {
            "message": message,
            "user_id": str(user_id),
            "platform": "Telegram",
            "type": "Platform_Response"
        }
        response = await http_client.post(url, headers=headers, json=payload)
        logging.info(f"Telegram MSG sent. Database Response: {response.text}")
        return msg_response

    except Exception as e:
        # Log the error with exception information
        logging.error('Error sending reply_text to user', exc_info=True)
