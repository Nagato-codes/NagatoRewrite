import discord
import json
from discord import File
from discord.ext import commands
from discord import app_commands
from easy_pil import Editor, load_image_async, Font
from utils.config import SERVERID

#if you want to give role to the user at any specific level upgrade then you can do like this
#enter the name of the role in a list
level = ["Rookie (5)", "Baller (15)", "Expert (20)", "Master (50)", "Mythical (100)"]

#add the level number at which you want to give the role
level_num = [5, 15, 20, 50, 100]

class Levelsys(commands.Cog):
  def __init__(self, bot:commands.Bot) -> None:
    super().__init__()
    self.bot = bot

  #this will increase the user's xp everytime they message
  @commands.Cog.listener()
  async def on_message(self, message:discord.Message):

    #the bot's prefix is ? that's why we are adding this statement so user's xp doesn't increase when they use any commands
    if not message.content.startswith("?"):

      #checking if the bot has not sent the message
      if not message.author.bot:
        with open("utils/levels.json", "r") as f:
          data = json.load(f)
        
        #checking if the user's data is already there in the file or not
        if str(message.author.id) in data:
          xp = data[str(message.author.id)]['xp']
          lvl = data[str(message.author.id)]['level']

          #increase the xp by the number which has 100 as its multiple
          increased_xp = xp+25
          new_level = int(increased_xp/100)

          data[str(message.author.id)]['xp']=increased_xp

          with open("utils/levels.json", "w") as f:
            json.dump(data, f)

          if new_level > lvl:
            await message.channel.send(f"{message.author.mention} Just Leveled Up to Level {new_level}!!!")

            data[str(message.author.id)]['level']=new_level
            data[str(message.author.id)]['xp']=0

            with open("utils/levels.json", "w") as f:
              json.dump(data, f)
            
            for i in range(len(level)):
              if new_level == level_num[i]:
                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))

                mbed = discord.Embed(title=f"{message.author} You Have Gotten role **{level[i]}**!", color = message.author.colour)
                mbed.set_thumbnail(url=message.author.avatar)
                await message.channel.send(embed=mbed)
        else:
          data[str(message.author.id)] = {}
          data[str(message.author.id)]['xp'] = 0
          data[str(message.author.id)]['level'] = 1

          with open("utils/levels.json", "w") as f:
            json.dump(data, f)

  @app_commands.command(name="rank", description="Shows Your or any users Rank")
  async def rank(self, interaction: discord.Interaction, user: discord.Member = None):
    user = user or interaction.user

    with open("utils/levels.json", "r") as f:
      data = json.load(f)

    xp = data[str(user.id)]["xp"]
    lvl = data[str(user.id)]["level"]

    next_level_xp = (lvl+1) * 100
    xp_need = next_level_xp
    xp_have = data[str(user.id)]["xp"]

    percentage = int(((xp_have * 100)/ xp_need))

    if percentage < 1:
      percentage = 0
    
    ## Rank card
    background = Editor(f"assets/imgs/zIMAGE.png")
    profile = await load_image_async(str(user.avatar))

    profile = Editor(profile).resize((150, 150)).circle_image()
    
    poppins = Font.poppins(size=40)
    poppins_small = Font.poppins(size=30)

    #you can skip this part, I'm adding this because the text is difficult to read in my selected image
    ima = Editor("assets/imgs/zBLACK.png")
    background.blend(image=ima, alpha=.5, on_top=False)

    background.paste(profile.image, (30, 30))

    background.rectangle((30, 220), width=650, height=40, fill="#fff", radius=20)
    background.bar(
        (30, 220),
        max_width=650,
        height=40,
        percentage=percentage,
        fill="#ff9933",
        radius=20,
    )
    background.text((200, 40), str(user.name), font=poppins, color="#ff9933")

    background.rectangle((200, 100), width=350, height=2, fill="#ff9933")
    background.text(
        (200, 130),
        f"Level : {lvl}   "
        + f" XP : {xp} / {(lvl+1) * 100}",
        font=poppins_small,
        color="#ff9933",
    )

    card = File(fp=background.image_bytes, filename="zCARD.png")
    await interaction.response.send_message(file=card)

  @app_commands.command(name="leaderboard", description="Shows the server leaderboard")
  async def leaderboard(self, interaction: discord.Interaction, range_num: int = 5):
    with open("utils/levels.json", "r") as f:
      data = json.load(f)

    l = {}
    total_xp = []

    for userid in data:
      xp = int(data[str(userid)]['xp']+(int(data[str(userid)]['level'])*100))

      l[xp] = f"{userid};{data[str(userid)]['level']};{data[str(userid)]['xp']}"
      total_xp.append(xp)

    total_xp = sorted(total_xp, reverse=True)
    index=1

    mbed = discord.Embed(
      title="Leaderboard Results"
    )
    mbed.set_thumbnail(url=interaction.guild.icon
                       )
    for amt in total_xp:
      id_ = int(str(l[amt]).split(";")[0])
      level = int(str(l[amt]).split(";")[1])
      xp = int(str(l[amt]).split(";")[2])

      member = await self.bot.fetch_user(id_)

      if member is not None:
        name = member.name
        mbed.add_field(name=f"{index}. {name}",
        value=f"**Level: {level} | XP: {xp}**", 
        inline=False)

        if index == range_num:
          break
        else:
          index += 1

    await interaction.response.send_message(embed = mbed)

  @app_commands.command(name="rank_reset", description="reset a users rank")
  @commands.has_permissions(administrator=True)
  async def rank_reset(self, interaction: discord.Interaction, user: discord.Member):
    member = user or interaction.user
    
    with open("utils/levels.json", "r") as f:
      data = json.load(f)

    del data[str(member.id)]

    with open("utils/levels.json", "w") as f:
      json.dump(data, f)

    await interaction.response.send_message(f"{member.mention}'s Data Got reset")
  
  @app_commands.command(name="increase_level", description="Increase a users level")
  @commands.has_permissions(administrator=True)
  async def increase_level(self, interaction: discord.Interaction, increase_by: int, user: discord.Member):
    member = user or interaction.user

    with open("utils/levels.json", "r") as f:
      data = json.load(f)
    
    data[str(member.id)]['level'] += increase_by

    with open("utils/levels.json", "w") as f:
      json.dump(data, f)
    
    await interaction.response.send_message(f"{member.mention}, Your level was increased by {increase_by}")

  @app_commands.command(name="increase_xp", description="Increase a users xp rate")
  @commands.has_permissions(administrator=True)
  async def increase_xp(self, interaction: discord.Interaction, increase_by: int, user: discord.Member):
    member = user or interaction.user

    with open("utils/levels.json", "r") as f:
      data = json.load(f)

    data[str(member.id)]['xp'] += increase_by

    with open("utils/levels.json", "w") as f:
      json.dump(data, f)

    await interaction.response.send_message(f"{member.mention}, Your Xp was increased by {increase_by}")

async def setup(bot:commands.Bot):
  await bot.add_cog(Levelsys(bot), guilds=[discord.Object(id=SERVERID)])