import discord
from discord.ext import commands
from discord import app_commands
from utils.config import SERVERID

class Avatar(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="avatar", description="Check you or a users avatar")
    async def avatar(self, interaction:discord.Interaction, user: discord.Member = None):
        user = user or interaction.user
        embed = discord.Embed(
            title=" ",
            description=f"### {user}\'s avatar",
            color=discord.Color.random()
        )
        embed.set_image(url=user.avatar)
        await interaction.response.send_message(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(Avatar(bot), guilds=[discord.Object(id=SERVERID)])