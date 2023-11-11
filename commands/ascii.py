import discord
from art import text2art
from discord import app_commands
from discord.ext import commands
from utils.nagato import SERVERID

class AsciiText(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="asciiart", description="turn text to art")
    async def ascii(self, interaction:discord.Interaction, text: str):
        art = text2art(text=text)
        await interaction.response.send_message(f"```\n{art}\n```")

async def setup(bot:commands.Bot):
    await bot.add_cog(AsciiText(bot), guilds=[discord.Object(id=SERVERID)])