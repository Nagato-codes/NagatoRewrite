from discord.ext import commands
from discord.ui import Modal, TextInput
from discord import Interaction, TextStyle, Embed, Color
from discord.utils import get

class ReportModal(Modal, title="Report User"):
    user_name = TextInput(label="User's Discord name", placeholder="eg.: JohnDoe#0000", required=True, max_length=100, style=TextStyle.short)
    user_id = TextInput(label="User's Discord ID", placeholder="To grab a users ID, make sure you have Developer mode on", required=True, max_length=100, style=TextStyle.short)
    description = TextInput(label="What did they do?", placeholder="eg.: Broke rule#4", required=True, min_length=200, max_length=2000, style=TextStyle.paragraph)

    async def on_submit(self, interaction: Interaction):
        await interaction.response.send_message(f"{interaction.user.mention}, Thank you for submitting your report, the moderation team will see it momentarily", ephemeral=True)

        channel = get(interaction.guild.channels, name="🔰・reports")

        await channel.send(embed=Embed(
            title="USER REPORTED!",
            description=f"### Report Submitted by {interaction.user.mention} \n ### Name: {self.user_name} \n ### ID: {self.user_id} \n ### Reported for: {self.description}",
            color=Color.random()
        ))