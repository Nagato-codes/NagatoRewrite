from discord.ext import commands
from discord import Member
from utils.nagato import update_presence

class Presence(commands.Cog):
    def __init__(self, bot:commands.Bot)  :
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member:Member):
        await update_presence(bot=self.bot)

    @commands.Cog.listener()
    async def on_member_remove(self, member:Member):
        await update_presence(bot=self.bot)

async def setup(bot:commands.Bot):
    await bot.add_cog(Presence(bot))