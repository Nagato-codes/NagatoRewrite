import random
import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands
import time
from utils.nagato import SERVERID

class Afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="afk", description="""Sets your afk""")
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def afk(self, interaction:discord.Interaction, reason: str = None):
        try:
            reason = reason or "AFK"
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
                    description=" You are already AFK",
                    color=discord.Color.brand_red()
                )
                await interaction.response.send_message(embed=em, ephemeral=True)
        finally:
            await db.close()

    @commands.Cog.listener(name="on_message")
    async def check_afk_message(self, msg: discord.Message):
        if msg.author.bot or msg.guild is None:
            return
        db = await aiosqlite.connect("Database/afk.db")
        try:
            cur = await db.execute("SELECT memname FROM afk WHERE memid=?", (msg.author.id,))
            name = await cur.fetchone()
            if name:
                cur = await db.execute("SELECT afktime FROM afk WHERE memid=?", (msg.author.id,))
                trs = await cur.fetchone()
                tp = int(time.time()) - int(trs[0])  # checking the afk time
                if tp >= 30:
                    await db.execute("DELETE FROM afk WHERE memid=?", (msg.author.id,))
                    await db.commit()
                    try:
                        await msg.author.edit(nick=f"{name[0]}")
                    except:
                        pass
                    emoji = random.choice(
                        ['<a:loading_think:1120651645928357959>', '<:buzines:1120607891687211088>', '<:hehe:1120606280927682600>'])
                    em = discord.Embed(
                        description=f"{emoji} I removed your AFK",
                        color=discord.Color.dark_gold()
                    )
                    await msg.reply(embed=em)
        finally:
            await db.close()

    @commands.Cog.listener(name="on_message")
    async def check_afk_mention(self, message: discord.Message):
        for mention in message.mentions:
            db: aiosqlite.Connection = await aiosqlite.connect("Database/afk.db")
            try:
                cursor = await db.execute("SELECT memres, afktime FROM afk WHERE memid = ?", (mention.id,))
                result = await cursor.fetchone()
                if result:
                    emojies = random.choice(
                        [
                            '<a:loading_think:1120651645928357959>',
                            '<:buzines:1120607891687211088>'
                        ]
                    )
                    embed = discord.Embed(
                        description="{0} {1} is AFK: {2} ({3})".format(
                            emojies,
                            mention.mention,
                            result[0],
                            f"<t:{result[1]}:f>"
                        )
                    )
                    await message.reply(embed=embed)
                    break
            finally:
                await db.close()    

async def setup(bot:commands.Bot):
    await bot.add_cog(Afk(bot), guilds=[discord.Object(id=SERVERID)])