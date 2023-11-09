import discord
from discord.ext import commands
from discord import app_commands
from discordify import Spotify
from utils.nagato  import SERVERID

class Spotifyy(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="spotify", description="Look at what you or some one is listening to")
    async def sp(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        client = Spotify(bot=self.bot, member=member)
        content , image, view = await client.get()
        await interaction.response.send_message(content=content, file=image, view=view)

async def setup(bot:commands.Bot):
    await bot.add_cog(Spotifyy(bot), guilds=[discord.Object(id=SERVERID)])