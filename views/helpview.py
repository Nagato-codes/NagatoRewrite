import discord
from discord import SelectOption
from discord.ext import commands
from discord.ui import Select, View

class HelpSelect(Select):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        options = [
            SelectOption(
                label="Moderation Commands",
                description="LIST OF ALL MODERATION COMMANDS",
                emoji="⚙",
                default=False
            ),
            SelectOption(
                label="Level Commands",
                description="LIST OF ALL LEVEL RELATED COMMANDS",
                emoji="🏆",
                default=False
            ),
            SelectOption(
                label="Staff Commands",
                description="LIST OF ALL STAFF COMMANDS",
                emoji="👷‍♂️",
                default=False
            ),
            SelectOption(
                label="Fun/Util Commands",
                description="LIST OF ALL FUN/UTIL COMMANDS",
                emoji="<:EF:1120599525652963409>",
                default=False
            ),
            SelectOption(
                label="Economy Commands",
                description="LIST OF ECONOMY COMMANDS",
                emoji="💸",
                default=False
            )    
        ]
        super().__init__(
            options=options, 
            placeholder="Select an options",
            min_values=1,
            max_values=1,
            disabled=False
        )

    async def callback(self, interaction: discord.Interaction):
        selected_option = interaction.data['values'][0]
        if selected_option == "Moderation Commands":
            M_embed = discord.Embed(
                title=" ",
                description="# Moderation Commands",
                color=discord.Color.random()
            )
            M_embed.add_field(
                name="``/warn``",
                value="Warn a member",
                inline=True
            )
            M_embed.add_field(
                name="``/warnings``",
                value="Check warnings of a user",
                inline=True
            )
            M_embed.add_field(
                name="``/clearwarns``",
                value="Clear all warns of a user",
                inline=True
            )
            M_embed.add_field(
                name="``/warndelete``",
                value="Delete a warning of a user",
                inline=True
            )
            M_embed.add_field(
                name="``/ban``",
                value="Ban a member",
                inline=True
            )
            M_embed.add_field(
                name="``/unban``",
                value="Unban a member",
                inline=True
            )
            M_embed.add_field(
                name="``/kick``",
                value="Kick a member",
                inline=True
            )
            M_embed.add_field(
                name="``/mute``",
                value="Mute a member",
                inline=True
            )
            M_embed.add_field(
                name="``/purge``",
                value="Purge messages in a channel",
                inline=True
            )
            M_embed.add_field(
                name="``/lock``",
                value="Lock a channel",
                inline=True
            )
            M_embed.add_field(
                name="``/unlock``",
                value="unlock a channel if its locked",
                inline=True
            )
            M_embed.add_field(
                name="``/genderroles``",
                value="Servers Gender roles",
                inline=True
            )
            M_embed.add_field(
                name="``/pingroles``",
                value="Servers ping roles",
                inline=True
            )
            M_embed.add_field(
                name="``/ticket``",
                value="Servers ticket view",
                inline=True
            )
            M_embed.add_field(
                name="``/verifyview``",
                value="Servers verify view",
                inline=True
            )
            await interaction.response.send_message(embed=M_embed, ephemeral=True)
        elif selected_option == "Level Commands":
            L_embed = discord.Embed(
                title="",
                description="# Level commands",
                color=discord.Color.random()
            )
            L_embed.add_field(
                name="``/rank``",
                value="Checl yours or a users rank",
                inline=True
            )
            L_embed.add_field(
                name="``leaderboard``",
                value="Check the servers leaderboard",
                inline=True
            )
            L_embed.add_field(
                name="``/rank_reset``",
                value="Reset a users rank",
                inline=True
            )
            L_embed.add_field(
                name="``/increase_level``",
                value="Increase a users level",
                inline=True
            )
            L_embed.add_field(
                name="``/increase_xp``",
                value="Increase a users xp",
                inline=True
            )
            await interaction.response.send_message(embed=L_embed, ephemeral=True)
        elif selected_option == "Staff Commands":
            S_embed = discord.Embed(
                title="",
                description="# Staff Commands",
                color=discord.Color.random()
            )
            S_embed.add_field(
                name="``create_staff_db``",
                value="Create the staff database",
                inline=True
            )
            S_embed.add_field(
                name="``/remove_staff_id``",
                value="Remove a users staff application id",
                inline=True
            )
            S_embed.add_field(
                name="``/apply``",
                value="Apply for staff",
                inline=True
            )
            S_embed.add_field(
                name="``/accept`` ",
                value="accept a staff application",
                inline=True
            )
            S_embed.add_field(
                name="``/hrd``",
                value="....",
                inline=True
            )
            S_embed.add_field(
                name="``/resign``",
                value="Resign from the staff team",
                inline=True
            )
            S_embed.add_field(
                name="``/leave_request``",
                value="Ask for a leave request",
                inline=True
            )
            S_embed.add_field(
                name="``create_staff_list_db``",
                value="create the staff list database",
                inline=True
            )
            S_embed.add_field(
                name="``/update_staff_list``",
                value="Update the staff list whenever there is a new staff member",
                inline=True
            )
            await interaction.response.send_message(embed=S_embed, ephemeral=True)
        elif selected_option == "Fun/Util Commands":
            FU_embed = discord.Embed(
                title=" ",
                description="# Fun/Util Commands",
                color=discord.Color.random()
            )
            FU_embed.add_field(
                name="``/8ball``",
                value="ask the magic 8ball anything",
                inline=True
            )
            FU_embed.add_field(
                name="``/avatar``",
                value="Check a users or your avatar",
                inline=True
            )
            FU_embed.add_field(
                name="``/botstats``",
                value="Displays the bots statistics",
                inline=True
            )
            FU_embed.add_field(
                name="``/calc``",
                value="Calculate anything for e.g log(10), sin(18)",
                inline=True
            )
            FU_embed.add_field(
                name="``/createtag``",
                value="Create a custom commands",
                inline=True
            )
            FU_embed.add_field(
                name="``/updatetag``",
                value="Update a custom command",
                inline=True
            )
            FU_embed.add_field(
                name="``/removetag``",
                value="Remove a custom command",
                inline=True
            )
            FU_embed.add_field(
                name="``/listcc``",
                value="List all the available commands",
                inline=True
            )
            FU_embed.add_field(
                name="``/choose``",
                value="Let the bot choose between two options",
                inline=True
            )
            FU_embed.add_field(
                name="``/echo``",
                value="Make the bot say anything :smirk:",
                inline=True
            )
            FU_embed.add_field(
                name="``/joke``",
                value="Gives a random joke",
                inline=True
            )
            FU_embed.add_field(
                name="``/lovecalc``",
                value="Calculate love between two members",
                inline=True
            )
            FU_embed.add_field(
                name="``/meme``",
                value="Gives a random meme",
                inline=True
            )
            FU_embed.add_field(
                name="``/spotify``",
                value="See what you or someone else is listening to",
                inline=True
            )
            FU_embed.add_field(
                name="``/suggest``",
                value="Suggest something",
                inline=True
            )
            FU_embed.add_field(
                name="``/accept``",
                value="Accept a suggestion",
                inline=True
            )
            FU_embed.add_field(
                name="``/deny``",
                value="Deny a suggestion",
                inline=True
            )
            FU_embed.add_field(
                name="``/userinfo``",
                value="Displays Information about a user",
                inline=True
            )
            FU_embed.add_field(
                name="``/wiki``",
                value="Search something in wikipedia",
                inline=True
            )
            FU_embed.add_field(
                name="``/report``",
                value="Report a user in the server",
                inline=True
            ) 
            FU_embed.add_field(
                name="``/hug``",
                value="HUG A USER",
                inline=True
            )
            FU_embed.add_field(
                name="``/kiss``",
                value="kiss a user",
                inline=True
            )
            await interaction.response.send_message(embed=FU_embed, ephemeral=True)
        elif selected_option == "Economy Commands":
            E_embed = discord.Embed(
                title="",
                description="# Economy Commands",
                color=discord.Color.random()
            )
            E_embed.add_field(
                name="``/addacc``",
                value="make your economy account",
                inline=True
            )
            E_embed.add_field(
                name="``/addbal``",
                value="add money to a users account",
                inline=True
            )
            E_embed.add_field(
                name="``/daily``",
                value="daily money!",
                inline=True
            )
            E_embed.add_field(
                name="``/work``",
                value="find a job and work",
                inline=True
            )
            E_embed.add_field(
                name="``/gamble``",
                value="gamble some money",
                inline=True
            )
            E_embed.add_field(
                name="``/beg``",
                value="beg for money",
                inline=True
            )
            E_embed.add_field(
                name="``/balance``",
                value="Check your or a users balance",
                inline=True
            )
            E_embed.add_field(
                name="``/deposit``",
                value="deposit money to bank",
                inline=True
            )
            E_embed.add_field(
                name="``/withdraw``",
                value="withdraw money from bank",
                inline=True
            )
            E_embed.add_field(
                name="``/economylb``",
                value="money leaderboard",
                inline=True
            )
            E_embed.add_field(
                name="``/transfer``",
                value="Transfer money to a user",
                inline=True
            )
            E_embed.add_field(
                name="``/shop``",
                value="view the shop",
                inline=True
            )
            E_embed.add_field(
                name="``/buy``",
                value="buy from shop",
                inline=True
            )
            E_embed.add_field(
                name="``/inventory``",
                value="view your inventory",
                inline=True
            )
            E_embed.add_field(
                name="``/sell``",
                value="sell the items you have",
                inline=True
            )
            E_embed.add_field(
                name="``/duel``",
                value="duel a member for money",
                inline=True
            )
            E_embed.add_field(
                name="``/invest``",
                value="Invest in...",
                inline=True
            )
            E_embed.add_field(
                name="``/redeem``",
                value="redeem your investments",
                inline=True
            )
            await interaction.response.send_message(embed=E_embed, ephemeral=True)

class HelpView(View):
    def __init__(self, bot:commands.Bot):
        super().__init__()
        self.bot = bot
        self.add_item(HelpSelect(self.bot))