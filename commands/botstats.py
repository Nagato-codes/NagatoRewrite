import discord
import time
import psutil
from discord.ext import commands
from discord import app_commands
from utils.nagato import SERVERID

class BotStats(commands.Cog):
    def __init__(self, bot:commands.Bot)  :
        super().__init__()
        self.bot = bot

    @app_commands.command(name="botstats", description="Displays bots statistics")
    async def botstats(self, interaction:discord.Interaction):
        start_time = time.time()  # Capture the start time

        latency = round(self.bot.latency * 1000)
        ram_usage = psutil.virtual_memory().percent
        cpu_usage = psutil.cpu_percent()
        discord_version = discord.__version__

        embed = discord.Embed(
            title="🏓 Bot Statistics",
            description="Here are some statistics about the bot:",
            color=discord.Color.random()
        )

        embed.add_field(
            name="API Latency",
            value=f"{latency} ms",
            inline=True
        )
        embed.add_field(
            name="RAM Usage",
            value=f"{ram_usage}%",
            inline=True
        )
        embed.add_field(
            name="CPU Usage",
            value=f"{cpu_usage}%",
            inline=True
        )
        embed.add_field(
            name="Discord Version",
            value=f"{discord_version}",
            inline=True
        )
        embed.add_field(
            name="Bot ID",
            value=f"{self.bot.user.id}",
            inline=True
        )

        end_time = time.time()  # Capture the end time
        response_time = round((end_time - start_time) * 1000)  # Calculate the response time in milliseconds

        embed.add_field(
            name="Response Time",
            value=f"{response_time} ms",
            inline=True
        )

        embed.set_footer(
            text=f"Requested by {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(BotStats(bot), guilds=[discord.Object(id=SERVERID)])