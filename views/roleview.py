import discord
from discord.ext import commands
from discord.utils import get
from discord.ui import button, View

class PingRolesView(View):
    def __init__(self, bot:commands.Bot):
        super().__init__()
        self.bot = bot

    @button(
        label="Announcement Ping",
        style=discord.ButtonStyle.red,
        emoji="📯"
    )
    async def announcement(
        self,
        interaction:discord.Interaction,
        button: discord.Button
    ):
        role = get(interaction.guild.roles, name="Announcement Ping")
        if role in interaction.user.roles:
            return interaction.response.send_message("SUKA BLYAT")
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                title="Announcement Role Added",
                description=" ",
                color=discord.Color.random()
            )
            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

    @button(
        label="Bot Updates",
        style=discord.ButtonStyle.red,
        emoji="🤖"
    )
    async def botupdates(
        self,
        interaction:discord.Interaction,
        button: discord.Button
    ):
        role = get(interaction.guild.roles, name="Bot Updates")
        if role in interaction.user.roles:
            return
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                title="Bot updates Role Added",
                description=" ",
                color=discord.Color.random()
            )
            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

    @button(
        label="Chat Revival Ping",
        style=discord.ButtonStyle.red,
        emoji="💬"
    )
    async def crp(
        self,
        interaction:discord.Interaction,
        button: discord.Button
    ):
        role = get(interaction.guild.roles, name="Chat Revival Ping")
        if role in interaction.user.roles:
            return
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                title="Chat Revival Ping Role Added",
                description=" ",
                color=discord.Color.random()
            )
            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

    @button(
        label="Anime News",
        style=discord.ButtonStyle.red,
        emoji="📯"
    )
    async def animenews(
        self,
        interaction:discord.Interaction,
        button: discord.Button
    ):
        role = get(interaction.guild.roles, name="Anime News")
        if role in interaction.user.roles:
            return
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                title="Anime News Role Added",
                description=" ",
                color=discord.Color.random()
            )
            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

    @button(
        label="Programming News",
        style=discord.ButtonStyle.red,
        emoji="📯"
    )
    async def prognews(
        self,
        interaction:discord.Interaction,
        button: discord.Button
    ):
        role = get(interaction.guild.roles, name="Programming News")
        if role in interaction.user.roles:
            return
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                title="Programming News Role Added",
                description=" ",
                color=discord.Color.random()
            )
            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

class GenderRolesView(View):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        super().__init__()

    @button(
        label="Boy",
        style=discord.ButtonStyle.red,
        emoji="👦"
    )
    async def boy(
        self,
        interaction:discord.Interaction,
        button: discord.Button
    ):
        role = get(interaction.guild.roles, name="Boy")
        if role in interaction.user.roles:
            return
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                title="Boy Role Added",
                description=" ",
                color=discord.Color.random()
            )
            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

    @button(
        label="Girl",
        style=discord.ButtonStyle.red,
        emoji="👧"
    )
    async def girl(
        self,
        interaction:discord.Interaction,
        button: discord.Button
    ):
        role = get(interaction.guild.roles, name="Girl")
        if role in interaction.user.roles:
            return
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                title="girl Role Added",
                description=" ",
                color=discord.Color.random()
            )
            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

    @button(
        label="Other",
        style=discord.ButtonStyle.red,
        emoji="🤰"
    )
    async def Other(
        self,
        interaction:discord.Interaction,
        button: discord.Button
    ):
        role = get(interaction.guild.roles, name="Other")
        if role in interaction.user.roles:
            return
        else:
            await interaction.user.add_roles(role)
            embed = discord.Embed(
                title="Other Role Added",
                description=" ",
                color=discord.Color.random()
            )
            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )