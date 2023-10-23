import discord
import random
from discord.ext import commands
from discord import app_commands
from utils.config import SERVERID

class LoveCalc(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="lovecalc", description="Calculate yours and a persons love")
    async def lovecalc(self, interaction: discord.Interaction, member1:discord.Member, member2: discord.Member):
        if member1.id == 923161381266685953 and member2.id == 995121392083292190:
            love_percent = "100%"
            embed = discord.Embed(
                title=" ",
                description="Love percentage of {0} and {1} is {2}%".format(member1.mention, member2.mention, love_percent),
                color=discord.Color.random()
            )
            embed.add_field(name="They should date they were meant for each other", value=" ", inline=True)
            await interaction.response.send_message(embed=embed)
        else:
            love_percent = random.randint(0, 100)
            if love_percent < 50:
                embed = discord.Embed(
                    title=" ",
                    description="Love Percentage of {0} and {1} is {2}%".format(member1.mention, member2.mention, love_percent),
                    color=discord.Color.random()
                )
                embed.add_field(name="Nah im not feeling the love", value=" ", inline=True)
                await interaction.response.send_message(embed=embed)
            if love_percent > 50 or love_percent == 100:
                embed = discord.Embed(
                    title=" ",
                    description="love percent of {0} and {1} is {2}%".format(member1.mention, member2.mention, love_percent),
                    color=discord.Color.random()
                )
                embed.add_field(name="YEAHH THEY SHOULD DATE", value=" ", inline=True)
                await interaction.response.send_message(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(LoveCalc(bot), guilds=[discord.Object(id=SERVERID)])