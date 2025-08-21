import discord
from discord import app_commands, ui
from discord.ext import commands
from dotenv import load_dotenv
import os
import json
import datetime

load_dotenv()
TOKEN = os.getenv("TOKEN")
DISCORD_SERVER_ID = os.getenv("SERVER_ID")
# with open("datum.json", "r") as f:
#     datum = json.load(f)

# for each in datum:
#     print(each)

intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run("YOUR_BOT_TOKEN")
