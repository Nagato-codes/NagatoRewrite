import discord
from discord.ext import commands
from discord.ui import button, View

class BanAppealView(View):
    def __init__(self, bot:commands.Bot):
        super().__init__()
        self.bot = bot

    @button(
        label="Ban Appeal",
        style=discord.ButtonStyle.blurple,
        emoji=":link:"
    )
    async def ban_appeal(
        self, 
        interaction:discord.Interaction,
        button:discord.Button
    ):
        link = "https://nagato.vercel.app/bp.html"
        await interaction.response.send_message(
            embed=discord.Embed(
                title="",
                description=f"Click this [link] to ban appeal({link})",
                color=discord.Color.random()
            )
        )