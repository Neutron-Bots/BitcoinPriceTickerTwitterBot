import os
from dotenv import load_dotenv

load_dotenv()


SLEEP_TIME = int(os.environ.get("SLEEP_TIME", "300"))
SERVER_URL = os.environ.get("SERVER_URL")

DETAIL_TEMPLATE = """
Detail Analysis:

Market Cap: 
${market_cap} {market_cap_change_percentage_24h}%{market_cap_symbol}

Matket Rank: 
{market_cap_rank} 

Fully Diluted Valuation: 
${fully_diluted_valuation}

Total Volume: 
${total_volume}

Market Cap Change: 
{market_cap_symbol}{market_cap_change_24h}$
"""

INFO_TEMPLATE = """
1₿ = ${current_price} {price_change_percentage_24h}%{symbol}

Details:
Change: {symbol}{price_change_24h}$
24H Low = ${low_24h}🔻
24H High = ${high_24h}💹

#bitcoin #btc
"""
