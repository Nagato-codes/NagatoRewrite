import discord
import asyncio
import time
import chat_exporter
from github import Github
from discord.ext import commands
from utils.nagato import GTOKEN
from discord.ui import View, Button, button

async def get_transcript(member:  discord.User, channel: discord.TextChannel):
    export = await chat_exporter.export(channel=channel)
    file_name = f"{member.id}.html"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(export)

def upload(file_path: str, member_name: str):
    github = Github(GTOKEN)
    repo = github.get_repo("Nagato-codes/Website")
    file_name = f"{int(time.time())}"
    repo.create_file(
        path=f"tickets/{file_name}.html",
        message=f"Ticket Log for {member_name}",
        branch="main",
        content=open(file_path, "r", encoding="utf-8").read()
    )
    return file_name

class TicketOpenView(View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @button(
        label="Open Ticket",
        emoji="🎫",
        style=discord.ButtonStyle.blurple,
    )
    async def open_ticket_view(self, interaction, button):
        await interaction.response.send_message(
            embed=discord.Embed(
                description=":white_check_mark: Opening a Ticket!",
                color=discord.Color.green()
            ),
            ephemeral=True
        )

        category = discord.utils.get(interaction.guild.categories, name="Tickets")
        staff_role = discord.utils.get(interaction.guild.roles, name="6 Paths Of Pain")
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")

        # Create a new text channel with specific permissions
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            staff_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            muted_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
        }

        channel_name = f"{interaction.user.name}'s Ticket"
        channel = await interaction.guild.create_text_channel(name=channel_name, overwrites=overwrites, category=category, topic=f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL")

        await interaction.edit_original_response(
            embed=discord.Embed(
                title="Thank you for keeping our server safe!",
                description=f"created ticket channel {channel.mention}",
                color=discord.Color.random()
            )
        )

        view = TicketCloseView(self.bot)

        await channel.send(
            f"{interaction.user.mention}",
            embed=discord.Embed(
                title="**WELCOME!**",
                description="Support will arrive shortly,\n"
                            "For fast support make sure\n"
                            "to drop your question beforehand.\n"
                            "You may ping staff, but please don't spam :gigachad:"
            ),
            view=view
        )

class TicketCloseView(View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @button(
        label="Close Ticket",
        emoji="🔒",
        style=discord.ButtonStyle.red
    )
    async def close_ticket_view(self, interaction, button):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Closing Ticket",
                description="Closing Ticket in 5 seconds",
                color=discord.Color.random()
            )
        )

        await asyncio.sleep(3)

        delete_view = TicketDeleteView(self.bot)
        category = discord.utils.get(interaction.guild.categories, name="Closed Tickets")

        # Set channel permissions to allow reading and disallow sending
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=False, send_messages=False),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
        }
        await interaction.channel.edit(category=category, overwrites=overwrites)

        await interaction.edit_original_response(
            embed=discord.Embed(
                title="Closed Ticket",
                description="This ticket has been closed!",
                color=discord.Color.random()
            ),
            view=delete_view
        )

        log_channel = discord.utils.get(interaction.guild.channels, name="🔰・ticket-logs")

        member_id = int(interaction.channel.topic.split()[0])
        member = interaction.guild.get_member(member_id)
        await get_transcript(member=member, channel=interaction.channel)
        file_name = upload(f"{member.id}.html", member.name)
        link = f"https://nagato-codes.github.io/Website/tickets/{file_name}"

        embed = (
            discord.Embed(
                title="Ticket Closed",
                color=discord.Color.og_blurple(),
            )
            .add_field(name="Opened by:", value=member.mention, inline=False)
            .add_field(name="Closed by:", value=interaction.user.mention, inline=False)
            .add_field(
                name="Closing Time:", inline=False, value=f"<t:{int(time.time())}:f>"
            )
        )

        view = View(timeout=None)
        view.add_item(TranscriptView(channel=interaction.channel, url=link))
        log_message = await log_channel.send(embed=embed, view=view)
        embed.add_field(name="Logs:", inline=False, value=log_message.jump_url)
        try:
            await member.send(embed=embed, view=view)
        except discord.Forbidden:
            pass

class TranscriptView(Button):
    def __init__(self, channel: discord.TextChannel, url: str):
        super().__init__(
            label="Transcript",
            emoji="🔗",
            url=url,
            style=discord.ButtonStyle.url
        )

class TicketDeleteView(View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @button(
        label="Delete Ticket",
        emoji="🗑️",
        style=discord.ButtonStyle.red
    )
    async def delete_ticket_view(self, interaction, button):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Deleting Ticket",
                description="Deleting Ticket in 5 seconds",
                color=discord.Color.random()
            )
        )

        await asyncio.sleep(3)

        # Delete the ticket channel
        await interaction.channel.delete()