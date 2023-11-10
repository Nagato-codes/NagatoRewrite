import discord
from discord.ext import commands
from discord import File
from easy_pil import Editor, load_image_async, Font

class Welcome(commands.Cog):
    def __init__(self, bot:commands.Bot)  :
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        memrole = discord.utils.get(member.guild.roles, name="Members")
        await member.add_roles(memrole)
        
        channel = self.bot.get_channel(1117161505624957101)

        background = Editor("assets/imgs/welcomebg.jpg")
        profile_image = await load_image_async(str(member.avatar))

        profile = Editor(profile_image).resize((150, 150)).circle_image()
        poppins = Font.poppins(size=50, variant="bold")

        poppins_small = Font.poppins(size=20, variant="light")

        background.paste(profile, (325, 90))
        background.ellipse((325, 90), 150, 150, outline="white", stroke_width=5)

        background.text((400, 260), f"WELCOME TO {member.guild.name}", color="white", font=poppins, align="center")
        background.text((400, 325), f"{member.name}#{member.discriminator}", color="white", font=poppins_small, align="center")

        file = File(fp=background.image_bytes, filename="assets/imgs/welcomebg.jpg")
        await channel.send(f"HELLO {member.mention}! WELCOME TO {member.guild.name}")
        await channel.send(file=file)

async def setup(bot:commands.Bot):
    await bot.add_cog(Welcome(bot))