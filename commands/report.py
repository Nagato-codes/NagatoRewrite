import discord
from discord import app_commands
from discord.ext import commands
from utils.nagato  import SERVERID
from views.reportview import ReportModal

class Report(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        super().__init__()
        self.bot=bot

    @app_commands.command(name="report", description="Report a user")
    async def report(self, interaction:discord.Interaction):
        await interaction.response.send_modal(ReportModal())

async def setup(bot:commands.Bot):
    await bot.add_cog(Report(bot), guilds=[discord.Object(id=SERVERID)])