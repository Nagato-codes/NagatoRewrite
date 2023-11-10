import discord
import aiosqlite
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from utils.nagato  import SERVERID

async def update_staff_list_embed(guild):
    # Fetch the staff roles from your guild (server)
    staff_roles = [
        "Nagato", 
        "Official Projects", 
        "Deva Path",
        "Animal Path",
        "Asura Path", 
        "Preta Path", 
        "Human Path", 
        "Naraka Path"
    ]
    
    # Initialize an empty string to store the list of members for each staff role
    embed_description = ""
    
    # Connect to the database
    async with aiosqlite.connect("Database/staff_list.db") as db:
        for role_name in staff_roles:
            # Fetch members with the specified staff role
            members_with_role = [
                member.mention for member in guild.members if any(role.name == role_name for role in member.roles)
            ]
            
            # Insert or update the staff role and members in the database
            await db.execute("DELETE FROM staff_list WHERE role_name=?", (role_name,))
            for member_mention in members_with_role:
                await db.execute("INSERT INTO staff_list VALUES (?, ?)", (role_name, member_mention))
            
            # Build the embed description
            embed_description += f"**{role_name}**\n"
            for member_mention in members_with_role:
                embed_description += f"- {member_mention}\n"
            embed_description += "\n"
        
        await db.commit()

    # Update the staff list embed
    channel = discord.utils.get(guild.text_channels, name="📕・role-info")
    if channel:
        embed = discord.Embed(
            title="Staff List",
            description=embed_description,
            color=discord.Color.gold(),
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text="Staff List", icon_url=guild.icon)
        await channel.purge(limit=1)  # Remove the previous embed message
        await channel.send(embed=embed)

class Staff(commands.Cog):
    def __init__(self, bot:commands.Bot)  :
        super().__init__()
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def create_staff_db(self, ctx:commands.Context):
        try:
            async with aiosqlite.connect('Database/staff_applications.db') as db:
                await db.execute(
                    "CREATE TABLE IF NOT EXISTS staff_applications (user_id INTEGER PRIMARY KEY)"
                )
                await db.commit()
            await ctx.reply("Staff applications database created successfully")
        except Exception as e:
            await ctx.send(e)

    @app_commands.command(name="remove_staff_id", description="Remove a staff member from the database")
    @commands.has_permissions(administrator=True)
    async def remove_id(self, interaction: discord.Interaction, user_id: int):
        # Check if the user ID is in the staff applications database
        async with aiosqlite.connect("Database/staff_applications.db") as db:
            cursor = await db.execute("SELECT * FROM staff_applications WHERE user_id=?", (user_id,))
            row = await cursor.fetchone()
            if row:
                # Remove the user's ID from the database
                await db.execute("DELETE FROM staff_applications WHERE user_id=?", (user_id,))
                await db.commit()

                embed = discord.Embed(
                    title="Application Removed",
                    description=f"User ID {user_id}'s staff application has been removed from the database.",
                    color=discord.Color.green()
                )
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(
                    title="Error",
                    description=f"User ID {user_id} is not found in the staff applications database.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed)

    @app_commands.command(name="apply", description="Apply for staff")
    async def apply(self, interaction:discord.Interaction):
        if "Baller (15)" in interaction.user.roles:
            await interaction.response.send_message("Sorry You need to be level 15")
            return
        else:
            questions = [
                "Tell us about yourself.",
                "Why do you want to join our staff team?",
                "Do you have any previous experience as a staff member?",
                "What qualities do you possess that would make you a good staff member?",
                "How active are you on our server?",
                "How well do you work in a team?",
                "How would you handle a situation where there is a disagreement among staff members?",
                "Are you familiar with our server's rules and guidelines?",
                "How would you handle a situation where a user is being disrespectful or breaking rules?",
                "Is there anything else you'd like to add?"
        ]
            user_id = str(interaction.user.id)
            user_dm = await interaction.user.create_dm()

            def check(m):
                return m.author == interaction.user and m.channel == user_dm

            # Collect answers from the user
            answers = []
            for question in questions:
                await user_dm.send(f"**Question:** {question}")
                answer = await self.bot.wait_for('message', check=check)
                answers.append(answer.content)

            # Send answers to the guild owner
            guild = interaction.guild
            owner = guild.owner

            # Send the answers as an embed
            answers_embed = discord.Embed(title=f"Staff Application Answers of {interaction.user}", color=discord.Color.green())
            for idx, (question, answer) in enumerate(zip(questions, answers), start=1):
                answers_embed.add_field(name=f"Question {idx}", value=f"**Q:** {question}\n**A:** {answer}", inline=False)

            owner_dm = await owner.create_dm()
            await owner_dm.send(embed=answers_embed)

            await interaction.response.send_message("Your application has been submitted. Thank you!")

    @app_commands.command(name="accept", description="appect a staff application")
    @commands.has_permissions(administrator=True)
    async def accept(self, interaction:discord.Interaction, user_id: int):
        async with aiosqlite.connect("staff_applications.db") as db:
            cur = await db.execute("SELECT * FROM staff_applications WHERE user_id =?", (user_id,))
            row = await cur.fetchone()
            if row:
                user = interaction.guild.get_member(user_id)
                if user:
                    embed = discord.Embed(
                        title="Welcome to the Staff Team!",
                        description=f"Congratulations, you've been accepted as a staff member! in {interaction.guild.name}",
                        color=discord.Color.green()
                    )
                    await user.send(embed=embed)
                    await interaction.response.send_message("Lets see his reaction")
                else:
                    embed = discord.Embed(
                        title="Error",
                        description="User ID not found in staff applications",
                        color=discord.Color.red()
                    )
                    await interaction.response.send_message(embed=embed)

    @app_commands.command(name="hrd", description="......")
    async def hrd(self, interaction:discord.Interaction):
        # Check if the user is in the staff applications database
        async with aiosqlite.connect("Database/staff_applications.db") as db:
            cursor = await db.execute("SELECT * FROM staff_applications WHERE user_id=?", (interaction.user.id,))
            row = await cursor.fetchone()
            if row:
                server_id = str(interaction.guild.id)

                hrd_role = discord.utils.get(interaction.guild.roles, name="Naraka Path")

                if hrd_role:
                    await interaction.user.add_roles(hrd_role)
                    await interaction.response.send_message(f"You have been granted the STAFF role: {hrd_role.mention}")
                else:
                    await interaction.response.send_message("HRD Role not configured for this server.")
            else:
                await interaction.response.send_message("You must first apply for staff using the `?apply` command.")

    @app_commands.command(name="resign", description="Resign from staff position")
    async def resign(self, interaction: discord.Interaction):
        # Check if the user is in the staff applications database
        async with aiosqlite.connect("Database/staff_applications.db") as db:
            cursor = await db.execute("SELECT * FROM staff_applications WHERE user_id=?", (interaction.user.id,))
            row = await cursor.fetchone()
            if row:
                # Define the list of questions for the resignation letter
                questions = [
                    "Why are you resigning from your staff position?",
                    "What are your reasons for leaving the staff team?",
                    "Is there anything you'd like to say to the staff and community?"
                ]

                user_dm = await interaction.user.create_dm()

                def check(m):
                    return m.author == interaction.user and m.channel == user_dm

                # Collect answers for the resignation letter from the user
                answers = []
                for question in questions:
                    await user_dm.send(f"**Question:** {question}")
                    answer = await self.bot.wait_for('message', check=check)
                    answers.append(answer.content)

                # Send the resignation letter to the guild owner
                guild = interaction.guild
                owner = guild.owner

                # Send the resignation letter as an embed
                resignation_embed = discord.Embed(title=f"Resignation Letter of {interaction.user}", color=discord.Color.red())
                for idx, (question, answer) in enumerate(zip(questions, answers), start=1):
                    resignation_embed.add_field(name=f"Question {idx}", value=f"**Q:** {question}\n**A:** {answer}", inline=False)

                owner_dm = await owner.create_dm()
                await owner_dm.send(embed=resignation_embed)

                await interaction.response.send_message("Your resignation letter has been submitted. Thank you for your service!")
            else:
                await interaction.response.send_message("You must first apply for staff using the `?apply` command.")

    @app_commands.command(name="leave_request", description="Request a leave")
    async def leave_request(self, interaction: discord.Interaction):
        # Check if the user is in the staff applications database
        async with aiosqlite.connect("Database/staff_applications.db") as db:
            cursor = await db.execute("SELECT * FROM staff_applications WHERE user_id=?", (interaction.user.id,))
            row = await cursor.fetchone()
            if row:
                # Define the list of questions for the leave request
                questions = [
                    "What is the reason for your leave request?",
                    "How long do you anticipate being away?",
                    "Is there anything you'd like to communicate to the staff and community?"
                ]

                user_dm = await interaction.user.create_dm()

                def check(m):
                    return m.author == interaction.user and m.channel == user_dm

                # Collect answers for the leave request from the user
                answers = []
                for question in questions:
                    await user_dm.send(f"**Question:** {question}")
                    answer = await self.bot.wait_for('message', check=check)
                    answers.append(answer.content)

                # Send the leave request to the guild owner
                guild = interaction.guild
                owner = guild.owner

                # Send the leave request as an embed
                leave_request_embed = discord.Embed(title=f"Leave Request of {interaction.user}", color=discord.Color.orange())
                for idx, (question, answer) in enumerate(zip(questions, answers), start=1):
                    leave_request_embed.add_field(name=f"Question {idx}", value=f"**Q:** {question}\n**A:** {answer}", inline=False)

                owner_dm = await owner.create_dm()
                await owner_dm.send(embed=leave_request_embed)

                await interaction.response.send_message("Your leave request has been submitted. Thank you!")
            else:
                await interaction.response.send_message("You must first apply for staff using the `?apply` command.")

    @commands.command()
    @commands.is_owner()
    async def create_staff_list_db(self, ctx:commands.Context):
        async with aiosqlite.connect("Database/staff_list.db") as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS staff_list (role_name TEXT, member_name TEXT)"
            )
            await db.commit()
        await ctx.reply("Staff List Database Created Successfully")

    @app_commands.command(name="update_staff_list", description="Update staff list")
    @commands.has_permissions(administrator=True)
    async def update_staff_list(self, interaction: discord.Interaction):
        if interaction.guild.id == 1116339771145465926:
            if interaction.user.guild_permissions.administrator:
                await update_staff_list_embed(interaction.guild)
                await interaction.response.send_message("Staff list updated successfully.")
            else:
                await interaction.response.send_message("You do not have permission to use this command.")
        else:
            await interaction.response.send_message("Oops, that command is only for my main server.")

async def setup(bot:commands.Bot):
    await bot.add_cog(Staff(bot), guilds=[discord.Object(id=SERVERID)])