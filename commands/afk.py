import discord
import random
import aiosqlite
import time
from discord import app_commands
from utils.config import SERVERID
from discord.ext import commands

class AFK(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="afk", description="SET YOUR AFK!!")
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def afk(self, interaction: discord.Interaction, *, reason: str = "No Reason Provided"):
        member = interaction.user
        db: aiosqlite.Connection = await aiosqlite.connect("Database/afk.db")
        cur = await db.execute("SELECT memres FROM afk WHERE memid=?", (member.id,))
        res = await cur.fetchone()
        if not res:
            await db.execute("INSERT INTO afk VALUES(?,?,?,?)", (member.id, member.display_name, reason, int(time.time())))
            await db.commit()
            try:
                await member.edit(nick=f"[AFK] {member.display_name}")
            except:
                pass
            emoji = random.choice(['⚪', '🔴', '🟤', '🟣', '🟢', '🟡', '🟠', '🔵'])
            em = discord.Embed(
                title=" ",
                description=f"{emoji} I set your AFK: {reason}",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=em)
        elif res:
            em = discord.Embed(
                description="You are already AFK",
                color=discord.Color.brand_red()
            )
            await interaction.response.send_message(embed=em)
        await db.close()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        for mention in message.mentions:
            db: aiosqlite.Connection = await aiosqlite.connect("Database/afk.db")
            cursor = await db.execute("SELECT memres, afktime FROM afk WHERE memid = ?", (mention.id,))
            result = await cursor.fetchone()
            if result:
                await db.execute("DELETE FROM afk WHERE memid = ?", (mention.id,))
                await db.commit()
                try:
                    await mention.edit(nick=mention.display_name)  # Remove AFK from the nickname
                except:
                    pass
            await db.close()
            if not result:
                return
            emojies = random.choice(['<a:emoji_3:938727345831960617>', '<:in_sleep1:938727849429434399>'])
            embed = discord.Embed(
                description="{0} {1} is AFK: {2} ({3})".format(
                    emojies,
                    mention.mention,
                    result[0],
                    f"<t:{result[1]}:>"
                )
            )
            await message.reply(embed=embed)
            break

async def setup(bot: commands.Bot):
    await bot.add_cog(AFK(bot), guilds=[discord.Object(id=SERVERID)])