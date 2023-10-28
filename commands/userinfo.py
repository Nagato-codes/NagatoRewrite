import discord
from discord.ext import commands
from utils.config import SERVERID
from discord import app_commands

class UserInfo(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command()
    async def userinfo(self, interaction:discord.Interaction, user: discord.Member = None):
        user = user or interaction.user
        roles = [role.mention for role in user.roles if role != interaction.guild.default_role]
        
        # Determine the user's status
        if user.status == discord.Status.online:
            status = "Online"
        elif user.status == discord.Status.idle:
            status = "Idle"
        elif user.status == discord.Status.dnd:
            status = "Do Not Disturb"
        else:
            status = "Offline"
        
        # Create a list of user's custom activities
        activities = []
        for activity in user.activities:
            if isinstance(activity, discord.CustomActivity):
                activities.append(activity.name)
        
        embed = discord.Embed(
            title=f"User Info - {user}",
            color=user.color,
            timestamp=interaction.message.created_at
        )
        embed.set_thumbnail(url=user.avatar)
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar)

        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Display Name", value=user.display_name, inline=True)
        embed.add_field(name="Discriminator", value=user.discriminator, inline=True)
        embed.add_field(name="Account Created", value=user.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"), inline=False)
        embed.add_field(name="Join Date", value=user.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC"), inline=False)
        embed.add_field(name="Status", value=status, inline=True)
        
        if activities:
            embed.add_field(name="Activities", value=', '.join(activities), inline=False)
        
        embed.add_field(name="Roles", value=', '.join(roles) if roles else 'None', inline=False)
        
        # Server-specific information
        if user.top_role != interaction.guild.default_role:
            embed.add_field(name="Top Role", value=user.top_role.mention, inline=True)
        embed.add_field(name="Boosted", value="Yes" if user.premium_since else "No", inline=True)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(UserInfo(bot), guilds=[discord.Object(id=SERVERID)])