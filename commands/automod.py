import discord
import time
import aiosqlite
from discord.ext import commands
from random import choice
from utils.nagato import SERVERID

async def get_wid() -> str:
    db = await aiosqlite.connect("Database/warns.db")
    res = " "
    while res is not None:
        ink = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        inklist = []
        wid = "#"
        for i in ink:
            inklist.append(i)
        for i in range(5):
            letter = choice(inklist)
            wid = f"{wid}{letter}"
        cur = await db.execute("SELECT wid FROM warn WHERE wid=?", (wid,))
        res = await cur.fetchone()
    await db.close()
    return wid

def get_banned_words():
    with open("assets/misc/bannedwords.txt", "r") as f:
        words = f.read().split(", ")
    return words

def get_new_message(msg: discord.Message):
    sentence = msg.content
    banned_words = get_banned_words()
    found_words = []
    for word in banned_words:
        if word in sentence.lower():
            sentence = sentence.replace(f"{word[1:]}", "\*"*len(word[1:]))
            found_words.append(word)
    found_words = ", ".join(found_words)
    return sentence, found_words

class Automod(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.guild is None:
            return
        if message.author.bot:
            return
        if message.author.guild_permissions.administrator:
            return
        new_message = get_new_message(message)
        if not new_message[0] == message.content:
            await message.delete()
            embed = [
                discord.Embed(
                    description=f"{message.author.mention} used a banned word!", color=discord.Color.brand_red()),
                discord.Embed(
                    description=f"{new_message[0]}", color=discord.Color.dark_orange())
            ]
            await message.channel.send(embeds=embed)
            db = await aiosqlite.connect("Database/warns.db")
            reason = f"Banned word(s) used: '{new_message[1]}'"
            wid = await get_wid()
            await db.execute("INSERT INTO warn VALUES(?, ?, ?, ?, ?)", (message.author.id, reason, self.bot.user.id, int(time.time()), wid))
            await db.commit()
            await db.close()
            try:
                await message.author.send(embed=discord.Embed(description=f"You were warned for: {reason}", color=discord.Color.dark_purple()))
            except discord.Forbidden:
                pass

async def setup(bot:commands.Bot):
    await bot.add_cog(Automod(bot), guilds=[discord.Object(id=SERVERID)])