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

messages={
    "tentamen":"Tentaregistration öppnar nu! Dags att registreta! Glöm inte att du även kan ansöka om plussning för att höja ditt betyg!",
    "registration":"Kursregistreting har öppnat! Glöm inte att dubbelkolla vilka kurser du ska söka om!",
    "anmalan":"Kursanmälan har öppnat på antagning.se! Glöm inte att ansöka till nästa termins kurser!",
    "omtentamen":"Omtentaregistreting har öppnats! Om du behöver göra en omtenta, glöm inte att registrera dig!"
}

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