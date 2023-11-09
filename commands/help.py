import discord
from discord import app_commands
from discord.ext import commands
from utils.nagato  import SERVERID
from views.helpview import HelpView

class Help(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="help", description="Help message")
    async def help(self, interaction:discord.Interaction):
        view = HelpView(self.bot)
        embed = discord.Embed(title="",description="# Bot commands",color=discord.Color.random())
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot:commands.Bot):
    await bot.add_cog(Help(bot), guilds=[discord.Object(id=SERVERID)])