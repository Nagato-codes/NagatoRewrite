import discord
from discord.ext import commands
from discord import app_commands
from utils.config import SERVERID
from views.roleview import PingRolesView, GenderRolesView

class ReactRoles(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="pingroles")
    @commands.has_permissions(administrator=True)
    async def pingroles(self, interaction:discord.Interaction):
        await interaction.channel.purge(limit=1)
        view = PingRolesView(self.bot)
        embed = discord.Embed(
            title=" ",
            description="# PING ROLES",
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="genderroles")
    @commands.has_permissions(administrator=True)
    async def genderroles(self, interaction:discord.Interaction):
        await interaction.channel.purge(limit=1)
        view = GenderRolesView(self.bot)
        embed = discord.Embed(
            title=" ",
            description="# GENDER ROLES",
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot:commands.Bot):
    await bot.add_cog(ReactRoles(bot), guilds=[discord.Object(id=SERVERID)])