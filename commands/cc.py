import discord
import sqlite3
from discord.ext import commands
from discord import app_commands
from utils.config import SERVERID

class CustomCommands(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.conn = sqlite3.connect("Database/custom_commands.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS custom_commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trigger TEXT UNIQUE,
                response TEXT
            )
        """)
        self.conn.commit()

    @app_commands.command(name="createtag", description="Create a custom command")
    async def customcom(self, interaction:discord.Interaction, trigger: str, *, response: str):
        """
        Add a custom command.

        Usage: !customcommand trigger response
        """
        # Read banned words from the file
        with open("assets/misc/bannedwords.txt", "r") as file:
            banned_words = [word.strip() for word in file.read().split(", ")]

        # Check if any baned words are in the trigger or response
        if any(word in trigger for word in banned_words) or any(word in response for word in banned_words):
            await interaction.response.send_message("Sorry, your custom command contains banned words.")
            return

        try:
            self.cursor.execute("INSERT INTO custom_commands (trigger, response) VALUES (?, ?)", (trigger, response))
            self.conn.commit()
            await interaction.response.send_message(f"Custom command '{trigger}' added successfully.")
        except sqlite3.IntegrityError:
            await interaction.response.send_message(f"Custom command '{trigger}' already exists. You can update it using !update_command.")

    @app_commands.command(name="updatetag", description="Update a custom command")
    @commands.has_permissions(manage_messages=True)
    async def update_command(self, interaction:discord.Interaction, trigger: str, *, response: str):
        """
        Update an existing custom command.

        Usage: !update_command trigger new_response
        """
        self.cursor.execute("UPDATE custom_commands SET response = ? WHERE trigger = ?", (response, trigger))
        self.conn.commit()
        await interaction.response.send_message(f"Custom command '{trigger}' updated successfully.")

    @app_commands.command(name="removetag", description="Remove a custom command")
    @commands.has_permissions(manage_messages=True)
    async def remove_command(self, interaction:discord.Interaction, trigger: str):
        """
        Remove a custom command.

        Usage: !remove_command trigger
        """
        self.cursor.execute("DELETE FROM custom_commands WHERE trigger = ?", (trigger,))
        self.conn.commit()
        await interaction.response.send_message(f"Custom command '{trigger}' removed successfully.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if message.content.startswith("?"):  # Replace "!" with your desired prefix
            command = message.content.split()[0][1:].lower()
            self.cursor.execute("SELECT response FROM custom_commands WHERE trigger = ?", (command,))
            result = self.cursor.fetchone()

            if result:
                await message.channel.send(result[0])

    @app_commands.command()
    async def listcc(self, interaction:discord.Interaction):
        """
        List all available custom commands.
        
        Usage: !list_commands
        """
        self.cursor.execute("SELECT trigger FROM custom_commands")
        results = self.cursor.fetchall()

        if results:
            commands_list = [result[0] for result in results]
            commands_str = "\n".join(commands_list)
            embed = discord.Embed(
                title="Available custom commands",
                description=f"{commands_list}"
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("There are no custom commands available.")

async def setup(bot:commands.Bot):
    await bot.add_cog(CustomCommands(bot), guilds=[discord.Object(id=SERVERID)])