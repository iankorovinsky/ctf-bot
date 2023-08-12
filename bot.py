# bot.py
import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands
import requests
import time
import json
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit
from selenium import webdriver
import undetected_chromedriver as uc
import re

load_dotenv()
TOKEN = 'BOT_TOKEN'

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')

@bot.event
async def on_message(message):
    # Make sure the Bot doesn't respond to it's own messages
    if message.author == bot.user: 
        return
    
    if message.content == 'hello':
        await message.channel.send(f'Hi {message.author}')
    if message.content == 'bye':
        await message.channel.send(f'Goodbye {message.author}')

    await bot.process_commands(message)

    if message.content == '!ctf-upcoming':
         ctfs = ctf_request()
         ctfs = '\n'.join(ctfs)
         await message.channel.send(f"Here are upcoming CTFs:\n{ctfs}")
        
def ctf_request():
        options = uc.ChromeOptions()
        options.headless = False
        seconds_since_epoch = int(time.time())
        headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9,ru;q=0.8", "Dnt": "1", "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"', "Sec-Ch-Ua-Mobile":"?0", "Sec-Ch-Ua-Platform": "Windows", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site":"same-origin", "Sec-Fetch-User": "?1", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
        for header, value in headers.items():
            options.add_argument(f'--header={header}:{value}')
        driver = uc.Chrome(options=options)
        URL = f"https://ctftime.org/api/v1/events/?limit=10&start={seconds_since_epoch}"
        driver.get(URL)
        driver.implicitly_wait(400) # Let the JavaScript load
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser") # Get the page source and parse it
        driver.close() # Close the driver
        events = json.loads(soup.get_text())
        ctfs = []
        for item in events:
            title = item.get("title")
            link = item.get("url")
            start = item.get("start")
            finish = item.get("finish")
            style = item.get("format")
            restrictions = item.get("restrictions")
            ctfs.append(f"Title: {title} | Link: {link} | Start: {start} | Finish: {finish} | Style: {style} | Restrictions: {restrictions}")
        return ctfs
bot.run(TOKEN)