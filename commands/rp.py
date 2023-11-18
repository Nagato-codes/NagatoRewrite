import discord
import random
from discord import app_commands
from discord.ext import commands
from utils.nagato import SERVERID

class RolePlay(commands.Cog):
    def __init__(self, bot:commands.Bot):
        super().__init__()
        self.bot = bot

    @app_commands.command(name="hug", description="Hug a user")
    async def hug(self, interaction:discord.Interaction, user: discord.User):
        if user == interaction.user:
            await interaction.response.send_message("BRO IS SO DOWN BAD HE WANTS TO HUG HIMSELF")

        gifs = [
            "https://cdn.discordapp.com/attachments/1116771487416864858/1175351251416916058/r1kC_dQPW.gif?ex=656aea27&is=65587527&hm=98fda603067f63b5c57a226ce8b56e2c4822ad9746082580c75ce5386df32a03&",
            "https://cdn.discordapp.com/attachments/1116771487416864858/1175351251072974918/r1XEOymib.gif?ex=656aea27&is=65587527&hm=f29318cc35ae9930ec1c13f46c025d032069793abb5ae7edac7d430aa6b8282e&",
            "https://cdn.discordapp.com/attachments/1116771487416864858/1175351250716467210/S1OAduQwZ.gif?ex=656aea27&is=65587527&hm=6732e5dea4c6087e8850e06d5965b460ee09f159dcf6c794bacc2cbc117de8c0&",
            "https://cdn.discordapp.com/attachments/1116771487416864858/1175351249206521956/Sy65_OQvZ.gif?ex=656aea26&is=65587526&hm=6c745a52935ec80b49f978f912c713909f0ce3a877e7531b4abc681584d67555&",
            "https://cdn.discordapp.com/attachments/1116771487416864858/1175351248849993789/S1gUsu_Qw-.gif?ex=656aea26&is=65587526&hm=c33629f662797d6b599c03db4c7b7808c893e29d1402e37663436e8463d345dd&",
            "https://cdn.discordapp.com/attachments/1116771487416864858/1175351249953095770/rkIK_u7Pb.gif?ex=656aea26&is=65587526&hm=dc770f4f7cde0a631544926b615d9e0a08dd0aa6a20e604be91a7cf91da6bea2&",
            "https://cdn.discordapp.com/attachments/1116771487416864858/1175351250305429564/Hy4hxRKtW.gif?ex=656aea27&is=65587527&hm=af2a2760a5d2ec8af9c2d8f93dc1dfeb01e8bed80c92f9762da91e252524a302&"
        ]

        _choice = random.choice(gifs)

        await interaction.response.send_message(f"{interaction.user.mention} HUGGED {user.mention}  {_choice}")

    @app_commands.command(name="kiss", description="kiss a user")
    async def kiss(self, interaction:discord.Interaction, user:discord.User):
        if user == interaction.user:
            await interaction.response.send_message("BRO IS SO DOWN BAD HE WANTS TO KISS HIMSELF")

        gifs = [
            "https://cdn.discordapp.com/attachments/1116771487416864858/1175352216173940818/rJ6PWohA-.gif?ex=656aeb0d&is=6558760d&hm=f96cfe6f092468230a300dcc85b4c39ede9d006080921bf7a9fa2e93fac9d955&",
            "https://cdn.discordapp.com/attachments/1116771487416864858/1175352695205396610/rJeB2aOP-.gif?ex=656aeb7f&is=6558767f&hm=4e2698b886b7df0a359a4ca0e1a0de996b1fe3619e13e8727d09fecd0e592abc&",
            "https://cdn.discordapp.com/attachments/1116771487416864858/1175352695629037608/HJmunTOw-.gif?ex=656aeb7f&is=6558767f&hm=c2d0a63455536c247e00ebad036f3cff97b744f92671669a56d4810fc24c6f01&",
            "https://cdn.discordapp.com/attachments/1116771487416864858/1175352696040063007/ry9uXAFKb.gif?ex=656aeb7f&is=6558767f&hm=d90ec9ab3f0f682ae372d295a91d21f6b6aad378aef83114167c45239bea2037&",
            "https://tenor.com/view/hyakkano-100-girlfriends-anime-kiss-kiss-anime-anime-kiss-cheek-gif-404363882587350736",
            "https://tenor.com/view/2-gif-14550762836565607423",
            "https://tenor.com/view/horimiya-animes-anime-shoujo-shounen-romance-boy-girl-gif-17793070781933240295",
            "https://tenor.com/view/engage-kiss-anime-kiss-gif-8228667042523289216"
        ]

        _choice = random.choice(gifs)

        await interaction.response.send_message(f"{interaction.user.mention} KISSED {user.mention}  {_choice}")

async def setup(bot:commands.Bot):
    await bot.add_cog(RolePlay(bot), guilds=[discord.Object(id=SERVERID)])