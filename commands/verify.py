import discord
from discord.ext import commands
from views.verifyview import VerifyView
from utils.config import SERVERID
from discord import app_commands

class Verify(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="verify", description="Verify button view")
    @commands.has_permissions(administrator=True)
    async def verifyview(self, interaction:discord.Interaction):
        if interaction.guild.id == 1116339771145465926:
            view = VerifyView(self.bot)
            await interaction.channel.purge(limit=1)
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Verify Yourself!!",
                    description="Verify Yourself in this server by clicking the button and writing the ***right*** code in the bots dm",
                    color=discord.Color.random()
                ),
                view=view
            )
        else:
            await interaction.response.send_message("Oops sorry but this command is only for my main server and how did you find out abt this")

async def setup(bot:commands.Bot):
    await bot.add_cog(Verify(bot), guilds=[discord.Object(id=SERVERID)])