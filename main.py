# Importing Tweepy
import asyncio
from twitterapi import TwitterUIFlow
from config import SERVER_URL, SLEEP_TIME
from utils import BTCTicker, ping_server


if SERVER_URL:
    from threading import Thread

    from flask import Flask, jsonify

    app = Flask("")

    @app.route("/")
    def main():
        res = {"status": "running"}
        return jsonify(res)

    def run():
        app.run(port=8000)

    async def keep_alive():
        server = Thread(target=run)
        server.start()


async def tweet_the_price(flow: TwitterUIFlow):
    info_message, detail_message = await BTCTicker()
    flow.CreateTweet(info_message)
    tweet_id = flow.content["data"]["create_tweet"]["tweet_results"]["result"][
        "rest_id"
    ]
    flow.CreateTweet(detail_message, in_reply_to_tweet_id=tweet_id)


async def main():
    if SERVER_URL:
        await keep_alive()
        asyncio.create_task(ping_server())
        
    flow = TwitterUIFlow()
    flow.LoadCookies("cookies.json")

    while True:
        try:
            await tweet_the_price(flow)
        except Exception as e:
            print(e)

        await asyncio.sleep(SLEEP_TIME)


if __name__ == "__main__":
    print("Bot started Running")
    asyncio.run(main())
