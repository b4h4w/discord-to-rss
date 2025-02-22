import discord
from discord.ext import commands
import json
import os
from datetime import datetime

# Set up intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="! ", intents=intents)

# Config from environment variables
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
TOKEN = os.getenv("DISCORD_TOKEN")

# File to store messages
MESSAGE_FILE = "messages.json"

# Load existing messages
def load_messages():
    try:
        if os.path.exists(MESSAGE_FILE):
            with open(MESSAGE_FILE, "r") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading messages: {e}")
    return []

# Save messages
def save_messages(messages):
    try:
        with open(MESSAGE_FILE, "w") as f:
            json.dump(messages, f, indent=2)
    except IOError as e:
        print(f"Error saving messages: {e}")

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}")

@bot.event
async def on_message(message):
    if message.channel.id == CHANNEL_ID and not message.author.bot:
        messages = load_messages()
        message_data = {
            "id": str(message.id),
            "author": message.author.name,
            "content": message.content,
            "timestamp": message.created_at.isoformat(),
            "link": f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
        }
        messages.append(message_data)
        save_messages(messages)
        print(f"Saved message from {message.author.name}")

bot.run(TOKEN)
