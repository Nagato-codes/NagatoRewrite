import discord
import requests
import random
from discord.ext import commands
from discord import app_commands
from utils.config import SERVERID

class Meme(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="meme", description="Displays a random meme")
    async def meme(self, interaction:discord.Interaction):
        try:
            response = requests.get("https://www.reddit.com/r/dankmemes/top.json?sort=top&t=day", headers={'User-Agent': 'Mozilla/5.0'})
            data = response.json()
            memes = data['data']['children']
            
            # Filter out stickied posts and select a random meme
            non_stickied_memes = [meme for meme in memes if not meme['data']['stickied']]
            selected_meme = random.choice(non_stickied_memes)

            meme_embed = discord.Embed(
                title=selected_meme['data']['title'],
                url=f"https://www.reddit.com{selected_meme['data']['permalink']}",
                color=0xFF4500  # You can customize the color
            )
            meme_embed.set_image(url=selected_meme['data']['url'])
            await interaction.response.send_message(embed=meme_embed)
        except Exception as e:
            await interaction.response.send_message(f"An error occured: {e}")

async def setup(bot:commands.Bot):
    await bot.add_cog(Meme(bot), guilds=[discord.Object(id=SERVERID)])