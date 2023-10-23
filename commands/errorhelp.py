import traceback
from discord.ext import commands

class ErrorHandling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return  # Ignore errors handled by individual command error handlers

        # Log the error
        error_msg = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
        print(error_msg)

        # Send an error message to the user
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore unknown commands

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"You're missing a required argument. Please check the command's usage. {error}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Invalid argument provided. Please check the command's usage. {error}")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown. Try again in {error.retry_after:.2f} seconds.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You don't have the necessary permissions to run this command. {error}")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"I don't have the necessary permissions to perform this action. {error}")
        else:
            await ctx.send("An error occurred while executing this command. The error has been logged and will be investigated.")

async def setup(bot):
    await bot.add_cog(ErrorHandling(bot))