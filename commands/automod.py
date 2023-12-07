import time
import sqlite3
import discord
import aiohttp
from commands.mod import get_wid
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
            "webhook_url": webhook.url
        }
        url = " https://ayuitz.vercel.app/sendwebhook"
        async with aiohttp.ClientSession() as session:
            response = await session.post(url=url, json=data) 
        if not response.status == 200:
            await channel.send(embed=discord.Embed(description=message.content).set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)) 

    def auto_warn(self, member: discord.Member, * reason: str):
        wid = await get_wid()
        db = await sqlite3.connect("Database/warns.db")
        await db.execute(
            "INSERT INTO warn VALUES(?,?,?,?,?)",
            (
                member.id,
                reason,
                interaction.user.id,
                int(time()),
                wid
            )
        )
        
        db.commit() 
        db.close() 

    @commands.Cog.listener() 
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        banned_words = self.get_banned_words() 
        found_words = []

        for word in banned_words:
            if word.lower() in message.content.lower().split:
                found_words.append(word) 
        member = message.author
        reason = "Used Banned word(s): `" + " ".join(found_words) + "`"
        if len(found_words) != 0:
            self.auto_warn(member=member, reason=reason) 
        new_content = self.filter_words(banned_words, message. content.lower()) 
        if not message.content.lower() = new_content.lower():
            await message.delete() 
            message_content = new_content
            channel = message.channel
            await self.send_new_message(channel=channel, message=message) 

async def setup(bot: commands.Bot):
    await bot.add_cog(Automod(bot)) 