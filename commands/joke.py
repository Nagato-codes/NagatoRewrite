import discord
import requests
from discord.ext import commands
from discord import app_commands
from utils.nagato  import SERVERID

class Joke(commands.Cog):
    def __init__(self, bot: commands.Bot)  :
        super().__init__()
        self.bot = bot

    @app_commands.command(name="joke", description="Gives a random joke")
    async def joke(self, interaction: discord.Interaction):
        joke_api_url = "https://v2.jokeapi.dev/joke/Any"  # JokeAPI URL for random jokes

        try:
            response = requests.get(joke_api_url)
            data = response.json()

            if response.status_code == 200:
                embed = discord.Embed(
                    title="Joke",
                    color=discord.Color.blue()
                )

                if "joke" in data:
                    joke_text = data["joke"]
                elif "setup" in data and "delivery" in data:
                    joke_text = f"{data['setup']}\n{data['delivery']}"
                else:
                    await interaction.response.send_message("No joke data found.")
                    return

                embed.description = joke_text

                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("Failed to fetch a joke.")
        except Exception as e:
            print(e)
            await interaction.response.send_message("An error occurred while fetching the joke")

async def setup(bot:commands.Bot):
    await bot.add_cog(Joke(bot), guilds=[discord.Object(id=SERVERID)])