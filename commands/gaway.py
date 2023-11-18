import discord
from discord.ext import commands, tasks
import aiosqlite
from datetime import datetime
from discord import app_commands
import time
import random
from pytimeparse import parse
from utils.nagato import SERVERID

def convert(time):
    time_in_sec = parse(time)
    if not time_in_sec:
        return 1000
    return time_in_sec

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.giveawaycheck.start()

    @app_commands.command(name="gstart", description="Start a giveaway")
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def gstart(self, interaction: discord.Interaction):
        quest = [
            "Which channel should the giveaway be hosted in?",
            "How long should the giveaway last?",
            "How many winners should there be in the giveaway? (1-10)",
            "What should be the prize of the giveaway?"
        ]

        em = discord.Embed(
            title=" ",
            description="Answer the questions within 30s to start the giveaway!",
            timestamp=datetime.utcnow(),
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(embed=em)
        qmsg = await interaction.followup.send(
            "Fetching Questions..."
        )
        ans = []

        def check(msg):
            return msg.author == interaction.user and msg.channel == interaction.channel

        qc = 1
        for i in quest:
            em = discord.Embed(
                title=f"<:buzines:1120607891687211088> Q{qc}",
                description=f"{i}",
                color=discord.Colour.random()
            )
            qc += 1
            await qmsg.edit(
                content=None,
                embed=em
            )
            try:
                amsg = await self.bot.wait_for(
                    'message',
                    check=check,
                    timeout=30.0
                )
            except TimeoutError:
                await interaction.followup.send("Timeout, be quicker next time.")
                return
            else:
                ans.append(amsg.content)
                await amsg.delete()

        em = discord.Embed(
            title=" ",
            description="Please confirm the given details",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        ).add_field(
            name=f"{quest[0]}",
            value=f"{ans[0]}",
            inline=False).add_field(
            name=f"{quest[1]}",
            value=f"{ans[1]}").add_field(
            name=f"{quest[2]}",
            value=f"{ans[2]}",
            inline=False).add_field(
            name=f"{quest[3]}",
            value=f"{ans[3]}")

        await qmsg.edit(
            content=None,
            embed=em
        )
        await qmsg.add_reaction(
            "\U00002705"
        )

        def reactcheck(react, user):
            return user == interaction.user and str(react.emoji) == "\U00002705"

        try:
            react, user = await self.bot.wait_for(
                'reaction_add',
                check=reactcheck,
                timeout=30.0
            )
        except TimeoutError:
            em = discord.Embed(
                title="Giveaway Cancelled!",
                description="No reaction was added!",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )

            await qmsg.edit(
                content=None,
                embed=em
            )
            return
        else:
            cid = int(ans[0][2:-1])
            endtime = convert(ans[1])
            endtime = int(time.time()) + int(endtime)
            gch = self.bot.get_channel(cid)
            em = discord.Embed(
                title="Giveaway Started!",
                description=f"Giveaway Started in {gch.mention}, it will end <t:{endtime}:R>",
                color=discord.Color.green(),
                timestamp=datetime.utcnow())

            emg = discord.Embed(
                title="New Giveaway!",
                description="React with <:zyzzrave:1120650227771261029> to participate!",
                color=discord.Color.blurple(),
                timestamp=datetime.utcnow()
            ).add_field(
                name="Hosted by:",
                value=f"{interaction.user.mention}"
            ).add_field(
                name="Prize:",
                value=f"{ans[3]}"
            ).add_field(
                name="No of winners:",
                value=f"{str(ans[2])}").add_field(
                name="Ends at:",
                value=f"<t:{endtime}:R>")
            gping = discord.utils.get(interaction.guild.roles, name="Announcement Ping")

            gmsg = await gch.send(content=f"{gping.mention}", embed=emg)
            await gmsg.add_reaction("<:zyzzrave:1120650227771261029>")

            db = await aiosqlite.connect("Database/gaway.db")
            cur = await db.execute("INSERT INTO main VALUES(?,?,?,?,?,?)",
                                (interaction.user.id, int(ans[2]), str(ans[3]), int(endtime), int(gmsg.id), int(cid)))
            await db.commit()
            await db.close()
            await interaction.followup.send(embed=em)

    @tasks.loop(seconds=5)
    async def giveawaycheck(self):
        db = await aiosqlite.connect("Database/gaway.db")
        cur = await db.execute("SELECT * FROM main WHERE ending<?", (int(time.time()),))
        res = await cur.fetchone()
        if not res:
            return
        gch = self.bot.get_channel(int(res[5]))
        gmsg = await gch.fetch_message(int(res[4]))
        prize = res[2]
        host = gmsg.guild.get_member(int(res[0]))
        no_of_winner = int(res[1])
        winners = [user async for user in gmsg.reactions[0].users()]
        winners.pop(winners.index(self.bot.user))
        winni = []
        for w in winners:
            wee = random.choice(winners)
            winners.pop(winners.index(wee))
            winni.append(wee.id)

        if len(winni) < no_of_winner:
            valid = False
        else:
            winner_role = gmsg.guild.get_role(1172547990926393364)
            valid = True
        em = discord.Embed(
            title="Giveaway Ended!",
            description=f"Hosted by: {host.mention}",
            color=discord.Color.blurple(),
            timestamp=datetime.utcnow()
        ).add_field(
            name="Prize:",
            value=f"{prize}")

        if valid is True:
            em.add_field(
                name="Winners:",
                value=f"{', '.join([gmsg.guild.get_member(w).mention for w in winni])}")
            for w in winni:
                winner = gmsg.guild.get_member(w)
                await winner.add_roles(winner_role)

        else:
            em.add_field(
                name="Sad Life ;-;",
                value="Not enough reactions to choose winners!")

        await gmsg.reply(f"{winner_role.mention} Congrats!", embed=em)

        await db.execute("DELETE FROM main WHERE gmsgid=?", (int(res[4]),))
        await db.commit()

        await db.close()


async def setup(bot: commands.Bot):
    await bot.add_cog(Giveaway(bot), guilds=[discord.Object(id=SERVERID)])