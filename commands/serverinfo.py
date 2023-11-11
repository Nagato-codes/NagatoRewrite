import discord
from discord.ext import commands
from discord import app_commands
from utils.nagato import SERVERID

class ServerInfo(commands.Cog):
    def __init__(self, bot:commands.Bot):
        super().__init__()
        self.bot = bot

    @app_commands.command(name="info", description="displays the server info")
    @commands.has_permissions(administrator=True)
    async def rules(self, interaction:discord.Interaction):
        description = (
            "Welcome to [Pains Hideout], the ultimate hub of digital awesomeness! 🚀\n\n"
            "🌐 **About Us:**\n"
            "   - A community of friendly and diverse individuals.\n"
            "   - Engaging discussions on a variety of topics.\n"
            "   - Memes that transcend the boundaries of humor.\n\n"
            "🎉 **What We Offer:**\n"
            "   - Regular events and activities for members.\n"
            "   - Creative channels for showcasing your talents.\n"
            "   - Welcoming atmosphere for both newcomers and veterans.\n\n"
            "🤖 **Bots & Games:**\n"
            "   - Fun and interactive bots to keep you entertained.\n"
            "   - Game nights and challenges for the competitive spirit.\n\n"
            "🌈 **Join Us Today!**\n"
            "   - Embrace the chaos, share your stories, and make lasting connections!\n"
            "   - Don't forget to check out our rules and guidelines in the server info channel.\n\n"
        )
        embed = discord.Embed(title=" ", description=description, color=discord.Color.random())
        embed.set_thumbnail(url=interaction.guild.icon)
        await interaction.response.send_message(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(ServerInfo(bot), guilds=[discord.Object(id=SERVERID)])