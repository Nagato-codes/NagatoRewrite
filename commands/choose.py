import discord
import random
from discord.ext import commands
from discord import app_commands
from utils.config import SERVERID

class Choose(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="choose", description="Let the bot make your decisions")
    async def choose(self, interaction: discord.Interaction, option1: str, option2: str):
        options = [option1, option2]

        with open("assets/misc/bannedwords.txt", "r") as file:
            banned_words = [word.strip() for word in file.read().split(",")]

        # Check if any banned words are in the trigger or response
        if any(word in option1 for word in banned_words) or any(word in option2 for word in banned_words):
            await interaction.response.send_message("Sorry, your options contains banned words.")
            return
        
        selected_option = random.choice(options)
        embed = discord.Embed(
            title="Bot's Choice",
            description=f"The bot has chosen: {selected_option}",
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Choose(bot), guilds=[discord.Object(id=SERVERID)])