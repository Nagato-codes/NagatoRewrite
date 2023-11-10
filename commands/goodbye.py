import discord
from discord.ext import commands

class Leave(commands.Cog):
    def __init__(self, bot:commands.Bot)  :
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        channel = discord.utils.get(member.guild.channels, name="👋・goodbye")
        embed = discord.Embed(
            title=f"Member Left!",
            description=" I hope you dont get dinner today ",
            color=discord.Color.random()
        )
        embed.set_thumbnail(url=member.display_avatar)
        await channel.send(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(Leave(bot))