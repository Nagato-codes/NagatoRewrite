import discord
import random
import asyncio
import os
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from discord.ui import View, button

# Using a dictionary to store verification codes
verification_codes = {}

def generate_verification_code():
    return ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", k=5))

def create_verification_image(code):
    image = Image.new('RGB', (200, 100), color=(255, 255, 255))
    d = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    d.text((10, 40), f"Verification Code: {code}", fill=(0, 0, 0), font=font)
    return image

async def send_verification_code(user):
    code = generate_verification_code()
    verification_codes[user.id] = code

    image = create_verification_image(code)
    image_path = f"verification_{user.id}.png"
    image.save(image_path)

    await user.send("Verification Code: ", file=discord.File(image_path))

    os.remove(image_path)

class VerifyView(View):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @button(
        label="Verify",
        emoji="✔️",
        style=discord.ButtonStyle.blurple
    )
    async def verify_view(
        self,
        interaction: discord.Interaction,
        button: discord.Button
    ):
        role = discord.utils.get(interaction.guild.roles, name="Verified")
        if role in interaction.user.roles:
                await interaction.response.send_message("You are already verified", ephemeral=True)

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Verification code sent",
                description=":white_check_mark: I have sent a DM with the verification code. When you have figured it out, write it in the bots DM"
            ),
            ephemeral=True
        )
        
        def check(message):
            return message.author == interaction.user and message.channel == interaction.user.dm_channel

        try:
            await send_verification_code(interaction.user)
            response = await self.bot.wait_for('message', check=check, timeout=180)
            if response.content == verification_codes.get(interaction.user.id):
                if role:
                    await interaction.user.add_roles(role)
                    await interaction.user.send(f"You are now verified in {interaction.guild}")
                    channel = discord.utils.get(interaction.guild.channels, name="💬・general")
                    await channel.send(f"Welcome {interaction.user.mention}")
                else:
                    await interaction.response.send_message("Sorry, this command is only for Nagato's main server.", ephemeral=True)
            else:
                await interaction.user.send("Sorry, wrong verification code. Try again.")
        except asyncio.TimeoutError:
            await interaction.user.send("Verification timed out. Try again")
        except discord.Forbidden:
            await interaction.response.send_message("Please contact a server administrator as i can not dm you", ephemeral=True)