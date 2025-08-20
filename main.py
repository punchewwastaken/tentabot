import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import json
load_dotenv()
TOKEN = os.getenv("TOKEN")
with open('datum.json', 'r') as f:
    datum = json.load(f)

for each in datum:
    print(each)

intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('YOUR_BOT_TOKEN')