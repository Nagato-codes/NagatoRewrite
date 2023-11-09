import discord
from discord.ext import commands
import aiosqlite
import asyncio
from commands.automod import get_wid
import time

class AntiSpamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_threshold = 10
        self.spam_cooldown = 10
        self.user_spam_count = {}

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author == self.bot.user:
            return  # Ignore messages sent by the bot itself

        author_id = message.author.id

        # Initialize spam count for the user
        if author_id not in self.user_spam_count:
            self.user_spam_count[author_id] = 0

        # Check if the user is spamming
        self.user_spam_count[author_id] += 1

        if self.user_spam_count[author_id] > self.spam_threshold:
            # Inform the user that they are spamming
            await message.channel.send(f"{message.author.mention}, please do not spam.")
            db = await aiosqlite.connect("Database/warns.db")
            reason = f"Spamming"
            wid = await get_wid()
            await db.execute("INSERT INTO warn VALUES(?, ?, ?, ?, ?)", (message.author.id, reason, self.bot.user.id, int(time.time()), wid))
            await db.commit()
            await db.close()
            try:
                await message.author.send(embed=discord.Embed(description=f"You were warned for: {reason}", color=discord.Color.dark_purple()))
            except discord.Forbidden:
                pass
            try:
                await message.delete()
            except discord.errors.NotFound:
                pass

            # Add a cooldown period for the user
            await asyncio.sleep(self.spam_cooldown)
            self.user_spam_count[author_id] = 0

    def set_threshold(self, threshold):
        self.spam_threshold = threshold

    def set_cooldown(self, cooldown):
        self.spam_cooldown = cooldown

async def setup(bot:commands.Bot):
    await bot.add_cog(AntiSpamCog(bot))