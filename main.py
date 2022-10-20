# Importing Tweepy
import asyncio
import traceback
import tweepy
from config import ACCESS_TOKEN, API_SECRET, API_KEY, BEARER_TOKEN, ACCESS_TOKEN_SECRET, REPLIT, SLEEP_TIME
from utils import BTCTicker, ping_server

# Credentials
api_key = API_KEY
api_secret = API_SECRET
bearer_token = fr"{BEARER_TOKEN}"
access_token = ACCESS_TOKEN
access_token_secret = ACCESS_TOKEN_SECRET

# Gainaing access and connecting to Twitter API using Credentials
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

# Creating API instance. This is so we still have access to Twitter API V1 features
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

if REPLIT:
    from threading import Thread

    from flask import Flask, jsonify
    app = Flask('')
    @app.route('/')
    def main():
        res = {
            "status":"running",
            "hosted":"replit.com",
        }
        return jsonify(res)

    def run():
        app.run(host="0.0.0.0", port=8000)
    
    async def keep_alive():
        server = Thread(target=run)
        server.start()

async def tweet_the_price(tweepy: tweepy.Client):
    info_message, detail_message = await BTCTicker()
    tweet = tweepy.create_tweet(text=info_message)
    tweet_id = tweet[0]['id']
    tweet = tweepy.create_tweet(text=detail_message, in_reply_to_tweet_id=tweet_id)

async def main():
    if REPLIT:
        await keep_alive()
        asyncio.create_task(ping_server())

    while True:
        try:
            await tweet_the_price(client)
        except Exception as e:
            print(e)
            
        await asyncio.sleep(SLEEP_TIME)

if __name__ ==  "__main__":
    print("Bot started Running")
    asyncio.run(main())
