import discord
from discord.ext import commands
import json
import os
from datetime import datetime

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="! ", intents=intents)

# Config - Replace these with your values
CHANNEL_ID = "CHANNEL_ID"  # Replace with your Discord channel ID
TOKEN = "DISCORD_TOKEN"      # Replace with your Discord bot token

# File to store messages
MESSAGE_FILE = "messages.json"

# Load existing messages
def load_messages():
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, "r") as f:
            return json.load(f)
    return []

# Save messages
def save_messages(messages):
    with open(MESSAGE_FILE, "w") as f:
        json.dump(messages, f, indent=2)

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
