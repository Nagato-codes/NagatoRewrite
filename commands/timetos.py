import discord
import re
from discord import app_commands
from discord.ext import commands
from utils.nagato import SERVERID

def parse_time(time_str):
    # Define a regular expression pattern to match time inputs like '6h' or '7d'
    pattern = re.compile(r'(?P<value>\d+)(?P<unit>[smhd])')
    match = pattern.match(time_str)

    if not match:
        raise ValueError('Invalid time format. Please use the format X[s/m/h/d].')

    value = int(match.group('value'))
    unit = match.group('unit')

    # Convert the time to seconds based on the unit
    if unit == 's':
        seconds = value
    elif unit == 'm':
        seconds = value * 60
    elif unit == 'h':
        seconds = value * 3600
    elif unit == 'd':
        seconds = value * 86400
    else:
        raise ValueError('Invalid time unit. Please use one of [s/m/h/d].')

    return seconds

class TimeConvertor(commands.Cog):
    def __init__(self, bot:commands.Bot):
        super().__init__()
        self.bot = bot

    @app_commands.command(name="converttosec", description="this command is useful when your trying to mute someone and need to convert minutes to seconds")
    async def convertos(self, intearction:discord.Interaction, time: str):
        try:
            seconds = parse_time(time)
            await intearction.response.send_message(f'{time} is equal to {seconds} seconds.')
        except ValueError as e:
            await intearction.response.send_message(f'Error: {e}')

async def setup(bot:commands.Bot):
    await bot.add_cog(TimeConvertor(bot), guilds=[discord.Object(id=SERVERID)])