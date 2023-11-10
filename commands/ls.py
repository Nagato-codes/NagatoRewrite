import discord
from discord.ext import commands

class Ls(commands.Cog):
    def __init__(self, bot:commands.Bot)  :
        super().__init__()
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def ls(self, ctx:commands.Context):
        invites = []
    
        for guild in self.bot.guilds:
            try:
                invite = await guild.invites()
                if invite:
                    invites.append(f"{guild.name}: {invite[0].url}")
                else:
                    invites.append(f"{guild.name}: No invites available.")
            except discord.errors.Forbidden:
                invites.append(f"{guild.name}: Bot doesn't have the 'Create Instant Invite' permission.")

        await ctx.send(embed=discord.Embed(title="", description="\n".join(invites)))

async def setup(bot:commands.Bot):
    await bot.add_cog(Ls(bot))