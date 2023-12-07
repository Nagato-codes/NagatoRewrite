import time
import sqlite3
import discord
import aiohttp
from discord.ext import commands

class Automod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot 
    
    def get_banned_words(self):
        with open("assets/misc/bannedwords.txt", "r") as f:
            return f.read().lower().split(", ")
    
    def filter_words(self, filter_words: str, message: str) -> str:
        for word in filter_words:
            word_length = Len(filter_words) // 2
            stars = "\*" * word_length 
            message = message.replace(word, f'{stars}{word[word_length:]}') 
        return message

    async def send_new_message(self, channel: discord.TextChannel, message: discord.Message):
        webhook = await channel.create_webhook(name=message.author.display_name) 
        data = data = {
            "message": message.content, 
            "avatar_url": message.author.display_avatar.url, 
            "webhook_url: webhook.url
        }
        url = " https://ayuitz.vercel.app/sendwebhook"
        async with aiohttp.ClientSession() as session:
            response = await session.post(url=url, json=data) 
        if not response.status == 200:
            await channel.send(embed=discord.Embed(description=message.content).set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)) 

    
async def setup(bot: commands.Bot):
    await bot.add_cog(Automod(bot)) 