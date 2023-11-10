import discord
import wikipedia
from discord.ext import commands
from discord import app_commands
from utils.nagato  import SERVERID

class Wikipedia(commands.Cog):
    def __init__(self, bot: commands.Bot)  :
        super().__init__()
        self.bot = bot

    @app_commands.command(name="wiki", description="Search wikipedia")
    async def wiki(self, interaction:discord.Interaction, *, query: str):
        try:
            # Search Wikipedia for the query
            results = wikipedia.search(query)

            if not results:
                await interaction.response.send_message("No results found for the given query.")
                return

            # Retrieve the first search result
            first_result = results[0]

            # Fetch the summary of the article
            summary = wikipedia.summary(first_result, sentences=3)  # Limit to 2 sentences

            # Create an embed with the title and summary
            embed = discord.Embed(
                title=first_result,
                description=summary,
                color=discord.Color.blue()
            )

            await interaction.response.send_message(embed=embed)

        except wikipedia.exceptions.DisambiguationError as e:
            await interaction.response.send_message(f"Disambiguation error: ```{str(e)}```")
        except wikipedia.exceptions.PageError as e:
            await interaction.response.send_message(f"Page not found: {str(e)}")

async def setup(bot:commands.Bot):
    await bot.add_cog(Wikipedia(bot), guilds=[discord.Object(id=SERVERID)])