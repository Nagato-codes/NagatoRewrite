import discord
from discord.ext import commands
from discord import app_commands
from utils.nagato  import SERVERID

class Suggestion(commands.Cog):
    def __init__(self, bot:commands.Bot)  :
        super().__init__()
        self.bot = bot

    @app_commands.command(name="suggest", description="Suggest something")
    async def suggest(self, interaction: discord.Interaction, suggestion: str):
        # Assuming ctx.channel.purge is replaced with another approach to handle command messages
        sugg_channel = discord.utils.get(interaction.guild.channels, name="📄・suggestion")

        if sugg_channel:
            embed = discord.Embed(
                title="Suggestion",
                description=f"{interaction.user.mention} has suggested:\n{suggestion}",
                color=discord.Color.random()
            )
            sugg = await sugg_channel.send(embed=embed)

            await sugg_channel.send(f"^^Suggestion ID: {sugg.id}")
            await sugg.add_reaction('✅')
            await sugg.add_reaction('❌')

    @app_commands.command(name="approve", description="Approve a suggestion")
    @commands.has_permissions(administrator=True)
    async def approve(self, interaction: discord.Interaction, id: int):
        sugg_channel = discord.utils.get(interaction.guild.channels, name="📄・suggestion")

        if sugg_channel:
            suggMSG = await sugg_channel.fetch_message(id)
            embed = discord.Embed(
                title=f"Suggestion has been approved",
                description=f"The suggestion id of `{suggMSG.id}` has been approved by {interaction.user.mention}",
                color=discord.Color.random()
            )
            await sugg_channel.send(embed=embed)

    @app_commands.command(name="deny", description="Deny a suggestion")
    @commands.has_permissions(administrator=True)
    async def deny(self, interaction: discord.Interaction, id: int):
        sugg_channel = discord.utils.get(interaction.guild.channels, name="📄・suggestion")

        if sugg_channel:
            suggMSG = await sugg_channel.fetch_message(id)
            embed = discord.Embed(
                title=f"Suggestion has been Denied",
                description=f"The suggestion id of `{suggMSG.id}` has been Denied by {interaction.user.mention}",
                color=discord.Color.random()
            )
            await sugg_channel.send(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(Suggestion(bot), guilds=[discord.Object(id=SERVERID)])