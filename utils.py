import asyncio
import logging

from pycoingecko import CoinGeckoAPI

from config import DETAIL_TEMPLATE, INFO_TEMPLATE, PING_INTERVAL

cg = CoinGeckoAPI()
import asyncio
import logging
import traceback

import aiohttp

from config import PING_INTERVAL, REPLIT

logging.getLogger().setLevel(logging.INFO)

async def BTCTicker():
    try:
        data = (cg.get_coins_markets(ids="bitcoin", vs_currency="usd"))[0]
        symbol = "🔻" if data['price_change_percentage_24h'].__str__().startswith("-") else "📈"
        market_cap_symbol = "🔻" if data['market_cap_change_percentage_24h'].__str__().startswith("-") else "📈"

        detail_message_reply_text = DETAIL_TEMPLATE.format(
            market_cap=data["market_cap"],
            market_cap_change_24h=int(data["market_cap_change_24h"]),
            market_cap_change_percentage_24h=data["market_cap_change_percentage_24h"],
            market_cap_symbol=market_cap_symbol,
            market_cap_rank=data["market_cap_rank"],
            fully_diluted_valuation=data["fully_diluted_valuation"],
            total_volume=data["total_volume"],
        )

        info_message_reply_text = INFO_TEMPLATE.format(
            current_price=data['current_price'],
            price_change_percentage_24h="%.2f" % data['price_change_percentage_24h'],
            symbol=symbol,
            price_change_24h="%.2f" % data["price_change_24h"],
            low_24h=data["low_24h"],
            high_24h=data["high_24h"],
        )
        return info_message_reply_text, detail_message_reply_text
    except Exception as e:
        print(e)

async def ping_server():
    sleep_time = PING_INTERVAL
    while True:
        await asyncio.sleep(sleep_time)
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(REPLIT) as resp:
                    logging.info(f"Pinged server with response: {resp.status}")
        except TimeoutError:
            logging.warning("Couldn't connect to the site URL..!")
        except Exception:
            traceback.print_exc()
