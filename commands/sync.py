import discord
from discord.ext import commands
from utils.nagato  import SERVERID

class Sync(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx:commands.Context) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.reply(embed=discord.Embed(
            title="Commands Synced",
            description=f"Synced {len(fmt)} commands",
            color=discord.Color.random()
        ))

async def setup(bot:commands.Bot):
    await bot.add_cog(Sync(bot), guilds=[discord.Object(id=SERVERID)])