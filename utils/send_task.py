import os, httpx
INTERNAL_GLOVELANE = os.getenv("INTERNAL_GLOVELANE_URL")

http_client = httpx.AsyncClient()
async def send_task(
    operation: str,
    user_id: str,
    origin_timestamp: str,
    *args,  # This will capture additional positional arguments
    **kwargs  # This will capture additional keyword arguments for "Settings" operation
):
    platform_id = "Telegram"
    payload = None

    if operation in ("Buy", "Sell"):
        token, amount = args  # Unpack additional arguments
        payload = {
            "platform": platform_id,
            "operation": operation,
            "user_id": user_id,
            "origin_timestamp": origin_timestamp,
            "token": token,
            "amount": amount,
        }
    elif operation == "WalletGen":  # Check for WalletGen operation
        target_wallet = args[0]  # Get the first additional argument
        payload = {
            "platform": platform_id,
            "operation": operation,
            "user_id": user_id,
            "origin_timestamp": origin_timestamp,
            "target_wallet": target_wallet,
        }
    elif operation == "Menu":  # Check for WalletGen operation
        name = args[0]  # Get the first additional argument
        payload = {
            "platform": platform_id,
            "operation": operation,
            "user_id": user_id,
            "origin_timestamp": origin_timestamp,
            "name": name,
        }
    elif operation == "UserExists":
        payload = {
            "platform": platform_id,
            "operation": operation,
            "user_id": user_id,
            "origin_timestamp": origin_timestamp,
        }
    elif operation == "Signup":
        payload = {
            "platform": platform_id,
            "operation": operation,
            "user_id": user_id,
            "origin_timestamp": origin_timestamp,
        }
    elif operation == "Transfer":
        (
            token,
            amount,
        ) = args  # This expects two arguments, but 'transfer_operation' sends only one.
        payload = {
            "platform": platform_id,
            "operation": operation,
            "user_id": user_id,
            "origin_timestamp": origin_timestamp,
            "token": token,  # This 'token' field could be misnamed based on the GloveRouter 'Task' model.
            "amount": amount,
        }
    elif operation == "Settings":
        # For "Settings", just use whatever is passed in via kwargs
        payload = {
            "platform": platform_id,
            "operation": operation,
            "user_id": user_id,
            "origin_timestamp": origin_timestamp
        }
        payload.update(kwargs)
        print("Settings Payload: ",payload)

    url = INTERNAL_GLOVELANE
    headers = {"Content-Type": "application/json"}

    response = None
    try:
        response = await http_client.post(url, headers=headers, json=payload)
    except Exception as e:
        print(f"Error sending task: {e}")
        response = None
    return response
