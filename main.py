import discord
from discord.ext import commands
import os
from utils.config import TOKEN

bot = commands.Bot(command_prefix="?", help_command=None, intents=discord.Intents.all(), application_id='1139850594501279745')

async def load_cogs():
    for c in os.listdir("./commands"):
        if c.endswith(".py"):
            await bot.load_extension(f"commands.{c[:-3]}")
            print(f"Loaded: {c[:-3]}")

@bot.event
async def on_ready():
    print("Logged in as {0}".format(bot.user.name))
    await load_cogs()

bot.run(TOKEN)