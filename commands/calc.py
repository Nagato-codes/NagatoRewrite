import discord
import math
from discord.ext import commands
from discord import app_commands
from utils.config import SERVERID

class MathCommands(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    def parse_expression(self, expression):
        # Replace some common mathematical functions and constants
        expression = expression.replace('pi', str(math.pi))
        expression = expression.replace('sqrt', 'math.sqrt')
        expression = expression.replace('sin', 'math.sin')
        expression = expression.replace('cos', 'math.cos')
        expression = expression.replace('tan', 'math.tan')
        expression = expression.replace('log', 'math.log')
        expression = expression.replace('^', '**')  # Exponentiation
        expression = expression.replace('exp', 'math.exp')
        expression = expression.replace('abs', 'abs')  # Absolute value
        expression = expression.replace('ceil', 'math.ceil')  # Ceiling
        expression = expression.replace('floor', 'math.floor')  # Floor
        expression = expression.replace('trunc', 'math.trunc')  # Truncation
        return expression

    def evaluate_expression(self, expression):
        try:
            result = eval(expression, {"__builtins__": None}, {"math": math})
            return result
        except Exception as e:
            return str(e)
        
    @app_commands.command(name="calc", description="Calculate any expression")
    async def calc(self, interaction: discord.Interaction, *, expression: str):
        expression = self.parse_expression(expression=expression)
        result = self.evaluate_expression(expression=expression)
        embed = discord.Embed(
            title="Calculated!",
            description=f"Result: {result}",
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(MathCommands(bot), guilds=[discord.Object(id=SERVERID)])