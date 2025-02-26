import discord
from discord.ext import tasks
import asyncio
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID')) if os.getenv('GUILD_ID') else None
CHANNEL_ID = int(os.getenv('CHANNEL_ID')) if os.getenv('CHANNEL_ID') else None
MESSAGE = os.getenv('MESSAGE_CONTENT', 'Default message')  # Default message if not specified

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@tasks.loop(hours=2)
async def send_regular_message():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await channel.send(f"{MESSAGE} - Sent at {current_time}")
    else:
        print("Channel not found!")

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    guild = client.get_guild(GUILD_ID)
    if guild:
        print(f'Connected to server: {guild.name}')
        # Start the message loop
        if not send_regular_message.is_running():
            send_regular_message.start()
    else:
        print("Server not found!")

@send_regular_message.error
async def send_message_error(error):
    print(f"An error occurred: {error}")

async def main():
    try:
        if not all([TOKEN, CHANNEL_ID]):
            raise ValueError("Missing required environment variables")
        await client.start(TOKEN)
    except Exception as e:
        print(f"Error starting bot: {e}")

if __name__ == "__main__":
    asyncio.run(main())