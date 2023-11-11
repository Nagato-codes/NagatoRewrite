import discord
from discord import app_commands
from discord.ext import commands
from utils.nagato  import SERVERID
from views.helpview import HelpView

class Help(commands.Cog):
    def __init__(self, bot:commands.Bot)  :
        super().__init__()
        self.bot = bot

    @app_commands.command(name="help", description="Help message")
    async def help(self, interaction:discord.Interaction):
        view = HelpView(self.bot)
        embed = discord.Embed(title="Bot Help",description="Hello! Welcome to the help page.",color=discord.Color.random())
        embed.add_field(name="Who am I?", value="\nWell first of all i am a discord bot if you havent figured that out 🤓 i am cool too YEAHH. I have features such as moderation, tags, starboard, and more. You can get more information on my commands by using the dropdown below.\n", inline=False)
        embed.add_field(name="", value=f"\nI am also open source you can find my code at [Github](https://github.com/Nagato-codes/NagatoRewrite)", inline=False)
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot:commands.Bot):
    await bot.add_cog(Help(bot), guilds=[discord.Object(id=SERVERID)])