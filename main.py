from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import bot
import asyncio
from webserver import keep_alive
import os

async def main():
    # Your existing code for running the Discord bot
    print()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
    keep_alive()
    bot.run_discord_bot()
