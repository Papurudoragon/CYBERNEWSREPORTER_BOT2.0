"""CISA news bot created by Van Perry 

This bot works by pulling an rss feed from CISA.gov. there is a 10 minute timer to check for a new link, and post if a new link exists."""

import discord
import feedparser
import asyncio
import os

my_secret = os.environ['DC_THREAT_FEED_BOT_SECRET'] #Auth

client = discord.Client(command_prefix='!', intents=discord.Intents.default() )
RSS_FEED = 'https://www.cisa.gov/uscert/ncas/current-activity.xml'
CHANNEL_ID = 1066453203333423285 # ID of your Discord channel
latest_link = None

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await check_feed()

async def check_feed():
    global latest_link
    await client.wait_until_ready()
    while not client.is_closed():
        feed = feedparser.parse(RSS_FEED)
        new_link = feed.entries[0].link
        if new_link != latest_link:
            latest_link = new_link
            channel = client.get_channel(CHANNEL_ID)
            await channel.send(latest_link)
        await asyncio.sleep(60) # 1 minute
   
  # Sometimes the bot times out, we can restart it with this:
  
try:
   client.run(my_secret) #set intents in the discord app page to run this  

except discord.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    os.system("python restarter.py")
    os.system('kill 1')







  
####### To Do: #######

# Test event not working and needs troublesheeoting..ab
  
# @client.event
# async def on_message(message):
#     if message.content.startswith('!test'):
#         response = f'Hello {message.author.name}, the test is successful'
#         await message.channel.send(response)
