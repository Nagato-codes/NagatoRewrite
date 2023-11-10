import discord
from discord import app_commands
from discord.ext import commands
from utils.nagato import SERVERID
from discord.utils import get

class Revive(commands.Cog):
    def __init__(self, bot:commands.Bot)  :
        super().__init__()
        self.bot = bot

    @app_commands.command(name="revive", description="revive the chat")
    @commands.cooldown(rate=1, per=3600, type=commands.BucketType.user)
    async def revive(self, interaction:discord.Interaction):
        role = get(interaction.guild.roles, name="Chat Revival Ping")
        await interaction.response.send_message(content=role.mention, embed=discord.Embed(
            title="Chat Revived",
            description=f"Revived by {interaction.user.mention}"
        ))

async def setup(bot:commands.Bot):
    await bot.add_cog(Revive(bot), guilds=[discord.Object(id=SERVERID)])