import discord
from discord.ext import commands
from datetime import datetime

class Log(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        if member.bot:
            return
        embed = discord.Embed(
            title="Member Joined!",
            description=f"{member.mention}",
            timestamp=datetime.utcnow(),
            color=discord.Color.random()
        )
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_footer(text=f"ID: {0}".format(member.id))
        channel = discord.utils.get(member.guild.channels, name="🔰・logs")
        await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        if member.bot:
            return
        embed = discord.Embed(
            title="Member Left!",
            description=f"{member.mention}",
            timestamp=datetime.utcnow(),
            color=discord.Color.random()
        )
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_footer(text=f"ID: {0}".format(member.id))
        channel = discord.utils.get(member.guild.channels, name="🔰・logs")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after: discord.Member):
        if before.bot:
            return
        if before.nick != after.nick:
            embed = (
                discord.Embed(
                    title="Member Nickname Changed!",
                    timestamp=datetime.utcnow(),
                    color=discord.Color.random(),
                )
                .set_thumbnail(url=before.display_avatar)
                .set_footer(text="id: {0}".format(before.id))
                .add_field(name="Before", value="{0}".format(before.nick))
                .add_field(name="After", value=f"{after.nick}")
            )
            channel = discord.utils.get(before.guild.channels, name="🔰・logs")
            await channel.send(embed=embed)
        if before.roles != after.roles:
            embed = (
                discord.Embed(
                    title="Member Role Changed!",
                    timestamp=datetime.utcnow(),
                    color=discord.Color.random(),
                )
                .set_thumbnail(url=before.display_avatar)
                .set_footer(text="id: {0}".format(before.id))
                .add_field(
                    name="Before",
                    value="{0}".format(
                        ",".join(role.mention for role in before.roles[1:])
                    ),
                )
                .add_field(
                    name="After",
                    value=f"{','.join(role.mention for role in after.roles[1:])}",
                )
            )
            channel = discord.utils.get(before.guild.channels, name="🔰・logs")
            await channel.send(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(Log(bot))