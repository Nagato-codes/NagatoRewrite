import discord
from discord.ext import commands
from discord import app_commands
from utils.nagato  import SERVERID
from views.ticketview import TicketOpenView

class Ticket(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="ticket", description="Ticket View For the server")
    @commands.has_permissions(administrator=True)
    async def ticket(self, interaction:discord.Interaction):
        view = TicketOpenView(self.bot)
        embed = discord.Embed(
            title="Create a Ticket!",
            description="Creating a ticket for invalid\nreason will get you warned.n\nIf you need any help regarding punishments,\nroles, or you just have a general question,\nfeel free to create a ticket and a\nstaff member will get to you shortly!\n\n__Do not open support tickets for Coding Help.,__\n__Doing so will get you warned.__",
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot:commands.Bot):
    await bot.add_cog(Ticket(bot), guilds=[discord.Object(id=SERVERID)])