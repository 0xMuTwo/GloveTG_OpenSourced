import logging
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

whisper_ip = "http://12.123.1.22:8000/"

async def openai_call(msg: str, user_id: int) -> dict:  # Return type is specified for clarity
    url = f'{whisper_ip}call_message'  # Use f-strings for concatenation
    payload = {
        "message": msg,
        "user_id": str(user_id),
    }
    try:
        # Use a context manager to ensure the client session is closed after the request
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()  # Raises an exception for 4XX/5XX responses
            return response.json()  # Return the parsed JSON response
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        logger.error(f"Request error occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

# Function to print the response
async def call_whisper(msg: str, user_id: int):
    response = await openai_call(msg, user_id)
    if response:
        return response.get("response")
    else:
        logger.error("Failed to get response from Whisper")


