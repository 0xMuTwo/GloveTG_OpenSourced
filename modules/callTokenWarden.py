import logging, httpx, pprint, re, math
from httpx import Response, HTTPStatusError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

menu_warden_ip = "http://12.123.1.22:8000/"

async def raw_menu_call(user_id: str) -> dict:
    url = f'{menu_warden_ip}/tg/menu/{user_id}'
    try:
        async with httpx.AsyncClient() as client:
            response: Response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except HTTPStatusError as exc:
        if exc.response.status_code == 500:
            return {"error": "Invalid Public Key", "status_code": 500}
        else:
            logger.error(f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")
            return {"error": f"HTTP error occurred: {exc.response.status_code}"}
    except httpx.RequestError as exc:
        logger.error(f"An error occurred while requesting {exc.request.url!r}.")
        return {"error": "A network error occurred."}
    except Exception as exc:
        logger.error(f"An unexpected error occurred: {exc}")
        return {"error": "An unexpected error occurred."}


def transform_menu_data(raw_data):
    public_key = raw_data.get("publicKey", "Wallet Address Not Found")
    holdings = raw_data.get("assetsWithPrice", [])

    menu_msg = ''
    
    wallet_msg = f'🪪 Your Wallet Address\n`{public_key}`\n\n'
    
    menu_msg += wallet_msg
    # Initialize the message for SOL amount and price to be empty
    sol_msg = ""

    sol_balance = 0
    net_worth = 0
    # Looking for the Wrapped SOL asset and formatting the output
    for asset in holdings:
        if asset['tokenPrice'].get('Symbol') == 'SOL':
            sol_balance = float(asset.get('tokenAmount'))
            sol_balance_truncated = truncate(sol_balance, 4)
            sol_price = float(asset['tokenPrice'].get('Price'))
            net_worth += (sol_balance * sol_price)
            sol_msg = f"Sol Balance: *{sol_balance_truncated}* | Sol Price: *${sol_price:.2f}*\n"
            # Break out of the loop as we already found Wrapped SOL asset
            sol_msg = escape_markdown(sol_msg)
            break

    if sol_balance == 0:
        no_money_notif = (
            'You have *0 Sol* in your wallet.\n'
            'Send Sol to your wallet address and let the fun begin.\n'
            'Need help? Type /fund\n\n'
        )
        no_money_notif = escape_markdown(no_money_notif)
        menu_msg += no_money_notif
        return menu_msg

    if sol_msg:
        # Remove SOL from the list of assets so it isn't processed further.
        holdings[:] = [asset for asset in holdings if asset['tokenPrice'].get('Symbol') != 'SOL']
   
    if sol_balance and not holdings:
        menu_msg += sol_msg
        sol_detected_msg = (
            '\n*Sol Detected!*\n'
            'Buy a token using the /buy command.'
        )
        sol_detected_msg = escape_markdown(sol_detected_msg)
        menu_msg += sol_detected_msg
        return menu_msg
    
    holdings.sort(key=lambda asset: float(asset.get('tokenAmount', 0)) * float(asset['tokenPrice'].get('Price', 0)))
    
    for asset in holdings:
        token_amount = float(asset.get('tokenAmount', {}))
        price = float(asset.get('tokenPrice', {}).get('Price'))
        token_value = token_amount * price
        net_worth += token_value
        if token_value < 0.001:
            continue  # Skip this asset if its value is less than $0.001

        assetAddress = asset.get("assetAddress")
        token_name = asset.get('tokenPrice', {}).get('Name')
        birdeye_url = generate_birdeye_url(assetAddress)
        displayed_token_value = rounded_balance_str(token_value)
        sol_value = token_value / sol_price if sol_price else 0
        price = format_asset_price(price)
        mcap = float(asset.get('tokenPrice', {}).get('MCap'))
        mcap = format_market_cap(mcap)
        price_changes = asset.get('tokenPrice', {}).get('PriceChanges')
        price_change_msg = format_price_changes(price_changes)
        token_link = markdown_link(token_name,birdeye_url)


        token_entry_minus_link = (
            f'Owned: *${displayed_token_value}* / *{sol_value:.4f} SOL*\n'
            f'{price_change_msg}\n'
            f'Market Cap: *{mcap}* @ *{price}*\n'
            f'*Token Address:*\n`{assetAddress}`\n\n'
        )
        token_entry_link = f'{token_link}\n'
        token_entry_minus_link = escape_markdown(token_entry_minus_link)
        token_entry  = token_entry_link + token_entry_minus_link
        menu_msg += token_entry
    
    net_worth_msg = f'Net Worth: *${net_worth:.2f}*'
    net_worth_msg = escape_markdown(net_worth_msg)
    
    menu_msg += sol_msg
    menu_msg += net_worth_msg
    
    transformed_data = menu_msg
    return transformed_data

async def call_menu_warden(user_id: str):
    raw_data = await raw_menu_call(user_id)
    pprint.pprint(raw_data)
    menu_data = transform_menu_data(raw_data)


    return menu_data

def escape_markdown(text:str) -> str:
    # Escape MarkdownV2 special characters (NOT INCLUDING ` or * because we need it for clickable copy & boldness)
    escape_chars = r'_[]()~>#+-=|{}.!'
    return re.sub(r'([{}])'.format(re.escape(escape_chars)), r'\\\1', text)



def format_price_changes(price_changes: dict) -> str:
    """
    Format the price changes for the given time intervals into a string.

    :param price_changes: A dictionary containing price change percentages for different intervals.
    :return: A formatted string representing the price change percentages.
    """
    time_intervals = [("m5", "5m"), ("h1", "1h"), ("h6", "6h"), ("h24", "24h")]
    formatted_changes = []
    for key, label in time_intervals:
        change = price_changes.get(key)
        sign = '+' if change and change >= 0 else ''  # '+' for positive, '' for negative or zero
        formatted_changes.append(f"{label}: *{sign}{change:.2f}%*" if change is not None else f"{label}: *N/A*")
    return ', '.join(formatted_changes)

def format_market_cap(market_cap: float) -> str:
    """
    Formats the market cap into a human-readable string with appropriate suffixes.
    :param market_cap: The market cap value to format.
    :return: A string representation of the market cap with abbreviations.
    """
    if market_cap < 1e3:
        return f"${market_cap:.2f}"
    elif market_cap < 1e6:
        return f"${market_cap / 1e3:.2f}K"
    elif market_cap < 1e9:
        return f"${market_cap / 1e6:.2f}M"
    elif market_cap < 1e12:
        return f"${market_cap / 1e9:.2f}B"
    else:
        return f"${market_cap / 1e12:.2f}T"


def format_asset_price(price: float) -> str:
    """
    Formats the price into a readable string, ensuring a minimum of 8 decimal places
    for very small prices.

    :param price: The price value to format.
    :return: A string representation of the price.
    """
    # Define a threshold for using extended precision
    precision_threshold = 0.01  # Prices below this use extended precision
    
    if price < precision_threshold:
        # Use extended decimal precision for tiny numbers
        formatted_price = f"${price:.7f}".rstrip('0').rstrip('.')
    else:
        # Use normal decimal precision
        formatted_price = f"${price:.2f}"
    
    return formatted_price

def rounded_balance_str(value: float, threshold: float = 0.01, max_precision: int = 10) -> str:
    """
    Round the balance for display, using extended precision for values below the threshold.

    :param value: The balance to format.
    :param threshold: Values below this use extended precision.
    :param max_precision: The maximum number of decimal places to display.
    :return: A balance string rounded for display.
    """
    if value == 0:
        return "0.00"
    elif value >= threshold:
        return f"{value:.2f}"
    else:
        return f"{value:.{max_precision}f}".rstrip('0').rstrip('.') or '0'
    
def generate_birdeye_url(tokenAddress: str) -> str:
    return f'https://birdeye.so/token/{tokenAddress}?chain=solana'


def markdown_link(name: str, url: str) -> str:
    # Escape only the markdown characters present in the name part of the link
    name_escaped = escape_markdown(name)
    # Do not escape anything in the URL
    return f"[{name_escaped}]({url})"


def truncate(number, digits) -> float:
    """
    Truncates a number to a specific number of decimal places without rounding.
    """
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper
