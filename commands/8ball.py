import discord
import requests
from discord.ext import commands
from discord import app_commands
from utils.config import SERVERID

class EightBall(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="8ball", description="Ask the magic eight ball anything")
    async def eightball(self, interaction: discord.Interaction, *, question: str):
        try:
            response = requests.get("https://yesno.wtf/api/")
            data = response.json()
            answer = data["answer"]

            embed = discord.Embed(
                title="",
                description=f"{interaction.user.mention} ASKS: {question}",
                color=discord.Color.random()
            )
            embed.add_field(name=f"\n\n> Answer: {answer}", value=" ", inline=False)

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")

async def setup(bot:commands.Bot):
    await bot.add_cog(EightBall(bot), guilds=[discord.Object(id=SERVERID)])