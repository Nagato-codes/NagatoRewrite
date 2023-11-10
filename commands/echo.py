import discord
from discord.ext import commands
from discord import app_commands
from utils.nagato  import SERVERID

class Echo(commands.Cog):
    def __init__(self, bot:commands.Bot)  :
        super().__init__()
        self.bot = bot

    @app_commands.command(name="echo", description="Make the bot say anything")
    async def echo(self, interaction: discord.Interaction, *, message: str):
        with open("assets/misc/bannedwords.txt", "r") as file:
            banned_words = [word.strip() for word in file.read().split(",")]

        # Check if any banned words are in the trigger or response
        if any(word in message for word in banned_words):
            await interaction.response.send_message("Sorry, your message contains banned words.")
            return
        
        embed = discord.Embed(
            title=" ",
            description=message,
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(Echo(bot), guilds=[discord.Object(id=SERVERID)])