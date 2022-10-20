import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", "300"))

# Replit Configuration
REPLIT_USERNAME = os.environ.get("REPLIT_USERNAME", None)
REPLIT_APP_NAME = os.environ.get("REPLIT_APP_NAME", None)
REPLIT = f"https://{REPLIT_APP_NAME.lower()}.{REPLIT_USERNAME}.repl.co" if REPLIT_APP_NAME and REPLIT_USERNAME else False
PING_INTERVAL = int(os.environ.get("PING_INTERVAL", "300"))

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
"""