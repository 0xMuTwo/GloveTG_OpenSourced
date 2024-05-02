import logging, httpx
from httpx import Response, HTTPStatusError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

token_spy_ip = "http://12.123.1.22:8000/"


async def raw_token_call(token_addr: str) -> dict:
    url = f'{token_spy_ip}scan_token?tokenAddress={token_addr}'
    try:
        async with httpx.AsyncClient() as client:
            response: Response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except HTTPStatusError as exc:
        if exc.response.status_code == 400:
            return {"error": "Invalid Token Address", "status_code": 400}
        else:
            logger.error(f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")
            return {"error": f"HTTP error occurred: {exc.response.status_code}"}
    except httpx.RequestError as exc:
        logger.error(f"An error occurred while requesting {exc.request.url!r}.")
        return {"error": "A network error occurred."}
    except Exception as exc:
        logger.error(f"An unexpected error occurred: {exc}")
        return {"error": "An unexpected error occurred."}



def escape_markdown_v2(text: str) -> str:
    # List of markdown v2 characters to escape
    escape_chars = '_[]()~>#+-={}.!'

    # Add backslash before every markdown character
    return ''.join(['\\' + char if char in escape_chars else char for char in text])

def format_token_spy_data(data: dict) -> str:

    symbol = data["Symbol"]
    chain = data["Chain"]
    token_address = escape_markdown_v2(data["TokenAddress"])
    mcap = f"${data['MCap']:,}"  # This uses thousands separators
    price = data["Price"]
    liq = data["Liq"]
    liq_percentage = f"{(liq / data['MCap']) * 100:.2f}%" if data['MCap'] else "N/A"
    price_changes = data["PriceChanges"]
    price_volume = data["PriceVolume"]
    transaction_volume = data["TransactionVolume"]
    dexscreener_link = f"https://dexscreener.com/solana/{token_address}"

    main_data_msg = (
            f"🪙 {escape_markdown_v2(data['Name'])} ({escape_markdown_v2(symbol)})\n"
            f"⛓ {chain}\n"
            "➖➖➖➖\n"
            f"`{token_address}`\n\n"
            f"📊 *MCap*: {mcap}\n"
            f"🏷 *Price*: {price}\n"
            f"💧 *Liq*: ${liq:,.2f} ({liq_percentage})\n\n"
            "📉 *Price Changes*:\n"
            f"      5m: {price_changes['m5']}% \| 1h: {price_changes['h1']}% \| 24h: {price_changes['h24']}%\n\n"
            "🎚 *Volume*:\n"
            f"      1h: ${price_volume['h1']:,.0f} \| 6h: ${price_volume['h6']:,.0f} \| 24h: ${price_volume['h24']:,.0f}\n\n"
            "🔄 *Buys/Sells*:\n"
            f"      1h: {transaction_volume['1h']['B']}/{transaction_volume['1h']['S']} \| "
            f"24h: {transaction_volume['24h']['B']}/{transaction_volume['24h']['S']}\n\n"
            


        )
    
    link_addition = f"[{'📈 DexS'}]({dexscreener_link})\n\n"

    data_minus_link = escape_markdown_v2(main_data_msg)

    final_final_msg = data_minus_link + link_addition
    return final_final_msg

async def token_spy_call(token_addr: str) -> str:
    raw_data = await raw_token_call(token_addr)
    if 'error' in raw_data:
        if raw_data.get('status_code') == 400:
            return "Invalid Token Address"
        return f"An error occurred: {raw_data['error']}"
    return format_token_spy_data(raw_data)