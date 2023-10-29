import discord
import aiosqlite
import asyncio
import re
from random import choice
from discord.ext import commands
from time import time
from discord import app_commands
from utils.config import SERVERID
from views.banapp import BanAppealView

async def get_wid():
    db = await aiosqlite.connect("Database/warns.db")
    res = "welp"
    while res is not None:
        ink = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        inklist = []
        wid = "#"
        for i in ink:
            inklist.append(i)
        for i in range(5):
            let = choice(inklist)
            wid = f"{wid}{let}"
        cur = await db.execute("SELECT wid FROM warn WHERE wid=?", (wid,))
        res = await cur.fetchone()
    await db.close()
    return wid


async def createdb():
    db = await aiosqlite.connect("Database/warns.db")
    await db.execute("""
    CREATE TABLE IF NOT EXISTS warn(
        memid INTEGER,
        reason TEXT,
        mod INTEGER,
        time INTEGER,
        wid TEXT
    )
        """)
    await db.close()

BULLET = "•"
time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {
    "h": 3600,
    "s": 1,
    "m": 60,
    "d": 86400
}
    
class Moderation(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def warndb(self, ctx):
        await createdb()
        await ctx.reply("CREATED WARNS DM")

    @app_commands.command(name="warn", description="Warn a member")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, *, reason: str):
        wid = await get_wid()
        db = await aiosqlite.connect("Database/warns.db")
        await db.execute(
            "INSERT INTO warn VALUES(?,?,?,?,?)",
            (
                member.id,
                reason,
                interaction.user.id,
                int(time()),
                wid
            )
        )
        await db.commit()
        await db.close()
        await interaction.response.send_message(
            embed=discord.Embed(
                description=f":white_check_mark: Warned: `{str(member)} `Reason: `{reason}`",
                color=discord.Color.green()
            )
        )
        try:
            embed = discord.Embed(
                title="User Warned!",
                description=f"User: `{str(member)}` has been warned\nReason: `{reason}`\nModerator:{interaction.user.mention}",
                color=discord.Color.random()
            )
            await log_channel.send(embed=embed)
            await member.send(
                embed=discord.Embed(
                    description=f"You have been warned in {interaction.guild.name} for `{reason}`",
                    color=discord.Color.red()
                )
            )
            log_channel = discord.utils.get(interaction.guild.channels, name="🔰・logs")
        except:
            pass

    @app_commands.command(name="warnings", description="Check a users warnings")
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, interaction: discord.Interaction, member: discord.Member):
        db = await aiosqlite.connect("Database/warns.db")
        cur = await db.execute("SELECT * FROM warn WHERE memid=? ORDER BY time DESC", (member.id,))
        res = await cur.fetchall()
        await db.close()
        if not res:
            return await interaction.response.send_message(embed=discord.Embed(description=f"{member.mention} has **0** warnings", color=discord.Color.green()))
        embed = discord.Embed(
            description=f"{member.mention} warnings:", color=discord.Color.red())
        wc = 1
        for i in res:
            embed.add_field(
                name=f"Warn {wc}:",
                value=f"**Warned by:** <@{i[2]}> **for:** {i[1]} **on:** <t:{i[3]}:R> **Id:** `{i[4]}`",
                inline=False)
            wc += 1

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="clearwarns", description="Clear all warnings of a user")
    @commands.has_permissions(manage_channels=True)
    async def clearwarn(self, interaction: discord.Interaction, member: discord.Member):
        db = await aiosqlite.connect("Database/warns.db")
        try:
            await db.execute("DELETE FROM warn WHERE memid=?", (member.id,))
            await db.commit()
            await interaction.response.send_message(embed=discord.Embed(description=f"Cleared warnings for: {member.mention}", color=discord.Color.green()))
            log_channel = discord.utils.get(interaction.guild.channels, name="🔰・logs")
            embed = discord.Embed(
                title="All Warnings Cleared!",
                description=f"User: `{str(member)}` warning have been cleared\nModerator:{interaction.user.mention}",
                color=discord.Color.random()
            )
            await log_channel.send(embed=embed)
        except:
            await interaction.response.send_message(embed=discord.Embed(description=f"No warnings found for: **{member.mention}**", color=discord.Color.red()))
        await db.close()

    @app_commands.command(name="warndelete", description="Delete a warning of a user")
    @commands.has_permissions(manage_channels=True)
    async def warn_delete(self, interaction:discord.Interaction, wid: int):
        db = await aiosqlite.connect("Database/warns.db")
        try:
            await db.execute("DELETE FROM warn WHERE wid=?", (wid,))
            await db.commit()
            await interaction.response.send_message(embed=discord.Embed(description=f"Deleted warn with id **{wid}**", color=discord.Color.green()))
            log_channel = discord.utils.get(interaction.guild.channels, name="🔰・logs")
            embed = discord.Embed(
                title="Warn Cleared!",
                description=f"The Warn id of {wid} has been deleted\nModerator:{interaction.user.mention}",
                color=discord.Color.random()
            )
            await log_channel.send(embed=embed)
        except Exception as e:
            await interaction.response.send_message(embed=discord.Embed(description=f"No warnings found with id: **{wid}**", color=discord.Color.red()))
        await db.close()

    @app_commands.command(name="ban", description="Ban a user from the server")
    @commands.has_permissions(ban_members=True)
    async def ban(self, interaction:discord.Interaction, member:discord.Member, *, reason: str = "No reason provided"):
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="User Banned!",
                description=" ",
                color=discord.Color.random()
            )
            embed.add_field(name="User ID", value=member.id, inline=True)
            embed.add_field(name="UserName", value=member.name, inline=True)
            embed.set_footer(icon_url=interaction.user.avatar, text=f"Banned By • {interaction.user.mention}")
            await interaction.response.send_message(embed=embed)
            log_channel = discord.utils.get(interaction.guild.channels, name="🔰・logs")
            log_embed = discord.Embed(
                title="User Banned!",
                description=" ",
                color=discord.Color.random()
            )
            log_embed.add_field(name="User ID", value=member.id, inline=True)
            log_embed.add_field(name="UserName", value=member.name, inline=True)
            log_embed.set_footer(icon_url=interaction.user.avatar, text=f"Banned By • {interaction.user.mention}")
            await log_channel.send(embed=log_embed)
            view = BanAppealView(self.bot)
            try:
                Membed = discord.Embed(
                    title=f"YOU HAVE BEEN BANNED FROM {interaction.guild.name}",
                    description=f"Reason: {reason}"
                )
                await member.send(embed=Membed, view=view)
            except discord.Forbidden:
                pass
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")

    @app_commands.command(name="kick", description="Kick a member from the server")
    @commands.has_permissions(kick_members=True)
    async def kick(self, interaction:discord.Interaction, member:discord.Member, *, reason: str = "No reason provided"):
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="User Kicked!",
                description=" ",
                color=discord.Color.random()
            )
            embed.add_field(name="User ID", value=member.id, inline=True)
            embed.add_field(name="UserName", value=member.name, inline=True)
            embed.set_footer(icon_url=interaction.user.avatar, text=f"Kicked By • {interaction.user.display_name}")
            await interaction.response.send_message(embed=embed)
            log_channel = discord.utils.get(interaction.guild.channels, name="🔰・logs")
            log_embed = discord.Embed(
                title="User Kicked!",
                description=" ",
                color=discord.Color.random()
            )
            log_embed.add_field(name="User ID", value=member.id, inline=True)
            log_embed.add_field(name="UserName", value=member.name, inline=True)
            log_embed.set_footer(icon_url=interaction.user.avatar, text=f"Kicked By • {interaction.user.display_name}")
            await log_channel.send(embed=log_embed)
            try:
                Membed = discord.Embed(
                    title=f"YOU HAVE BEEN KICKED FROM {interaction.guild.name}",
                    description=f"Reason: {reason}"
                )
                await member.send(embed=Membed)
            except discord.Forbidden:
                pass
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")

    @app_commands.command(name="unban", description="Unban a user from the server")
    @commands.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, member:discord.Member, *, reason: str = "No reason provided"):
        try:
            await member.unban(reason=reason)
            embed = discord.Embed(
                title="User Unbanned!",
                description=" ",
                color=discord.Color.random()
            )
            embed.add_field(name="User ID", value=member.id, inline=True)
            embed.add_field(name="UserName", value=member.name, inline=True)
            embed.set_footer(icon_url=interaction.user.avatar, text=f"Unbanned By • {interaction.user.display_name}")
            await interaction.response.send_message(embed=embed)
            log_channel = discord.utils.get(interaction.guild.channels, name="🔰・logs")
            log_embed = discord.Embed(
                title="User Unbanned!",
                description=" ",
                color=discord.Color.random()
            )
            log_embed.add_field(name="User ID", value=member.id, inline=True)
            log_embed.add_field(name="UserName", value=member.name, inline=True)
            log_embed.set_footer(icon_url=interaction.user.avatar, text=f"Unbanned By • {interaction.user.display_name}")
            await log_channel.send(embed=log_embed)
            try:
                Membed = discord.Embed(
                    title=f"YOU HAVE BEEN UNBANNED FROM {interaction.guild.name}",
                    description=f"Reason: {reason}"
                )
                await member.send(embed=Membed)
            except discord.Forbidden:
                pass
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")

    @app_commands.command(name="mute", description="Mute a user in the server")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, time: int, reason: str = None):
        role = discord.utils.get(interaction.guild.roles, name="Muted")
        await member.add_roles(role)
        embed = discord.Embed(
            title="Member Muted!",
            description=" ",
            color=discord.Color.random()
        )
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="UserName", value=member.name, inline=True)
        embed.add_field(name="Time", value=time, inline=True)
        embed.add_field(name="Reason", value=f"{reason}", inline=True)
        embed.set_footer(icon_url=interaction.user.avatar, text=f"Muted By • {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)
        log_channel = discord.utils.get(interaction.guild.channels, name="🔰・logs")
        log_embed = discord.Embed(
            title="Member Muted",
            description=" ",
            color=discord.Color.random()
        )
        log_embed.add_field(name="User ID", value=member.id, inline=True)
        log_embed.add_field(name="UserName", value=member.name, inline=True)
        log_embed.add_field(name="Time", value=time, inline=True)
        log_embed.set_footer(icon_url=interaction.user.avatar, text=f"Muted By • {interaction.user.display_name}")
        try:
            Membed = discord.Embed(
                title=f"YOU HAVE BEEN MUTED IN {interaction.guild.name}"
            )
            await member.send(embed=Membed)
        except discord.Forbidden:
            pass
        await log_channel.send(embed=embed)
        await asyncio.sleep(time)
        await member.remove_roles(role)

    @app_commands.command(name="purge", description="Purge Messages in a channel")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, interaction:discord.Interaction, amount: int):
        if amount == 0:
            await interaction.response.send_message("How the f-")
            return
        if amount == 1:
            await interaction.response.send_message("Its 1 message im not gonna delee it do it on your own")
            return
        deleted = await interaction.channel.purge(limit=amount + 1)
        embed = discord.Embed(
            title=f"{len(deleted)} messages were deleted",
            description=" ",
            color=discord.Color.random()
        )
        embed.add_field(name="Channel", value=interaction.channel.mention, inline=True)
        embed.set_footer(icon_url=interaction.user.avatar, text=f"Purged by {BULLET} {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="lock", description="Lock a channel")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, interaction:discord.Interaction, channel: discord.TextChannel = None):
        channel = channel or interaction.channel
        await channel.set_permissions(interaction.guild.default_role, send_messages=False, view_channel=True)
        embed = discord.Embed(
            title=":lock: Channel Locked",
            description=" ",
            color=discord.Color.random()
        )
        embed.set_footer(icon_url=interaction.user.avatar, text=f"Locked by {BULLET} {interaction.user.mention}")
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="unlock", description="Unlock a channel")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, interaction:discord.Interaction, channel: discord.TextChannel = None):
        channel = channel or interaction.channel
        await channel.set_permissions(interaction.guild.default_role, send_messages=True, view_channel=True)
        embed = discord.Embed(
            title=":lock: Channel Unlocked",
            description=" ",
            color=discord.Color.random()
        )
        embed.set_footer(icon_url=interaction.user.avatar, text=f"Unlocked by {BULLET} {interaction.user.mention}")
        await interaction.response.send_message(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(Moderation(bot), guilds=[discord.Object(id=SERVERID)])