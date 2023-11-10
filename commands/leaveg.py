import discord
from discord.ext import commands

class LeaveGuildCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='leaveguild')
    async def leaveguild(self, ctx, *, guild_name):
        """
        Command to make the bot leave a specific guild.
        """
        # Check if the command invoker is a server administrator
        if ctx.author.guild_permissions.administrator:
            # Try to find the guild by name
            target_guild = discord.utils.get(self.bot.guilds, name=guild_name)

            if target_guild:
                await ctx.send(f"Leaving the guild: {target_guild.name}. Goodbye!")
                await target_guild.leave()
            else:
                await ctx.send("I'm not a member of that guild.")
        else:
            await ctx.send("You don't have permission to use this command.")

async def setup(bot):
    await bot.add_cog(LeaveGuildCog(bot))