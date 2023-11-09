import discord
from discord.ext import commands
from utils.nagato import MESSLOGS

class MessageLogs(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.log_channel = self.bot.get_channel(MESSLOGS)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        logs_channel = self.log_channel

        if logs_channel:
            embed = discord.Embed(
                title="Message deleted",
                color=discord.Color.red(),
                timestamp=message.created_at
            )
            embed.add_field(name="> Channel", value=f"{message.channel.mention} ({message.channel.name})", inline=False)
            embed.add_field(name="> Message ID", value=message.id, inline=False)
            embed.add_field(name="> Message author", value=message.author.mention, inline=False)
            embed.add_field(name="> Message created", value=message.created_at.strftime('%Y-%m-%d %I:%M %p'), inline=False)
            embed.add_field(name="Message Content", value=message.content, inline=False)
            embed.set_thumbnail(url=message.author.avatar)

            await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
            logs_channel = self.log_channel

            if logs_channel:
                if before.content != after.content:
                    embed = discord.Embed(
                        title="Message edited",
                        color=discord.Color.blue(),
                        timestamp=after.created_at
                    )
                    embed.add_field(name="> Channel", value=f"{before.channel.mention} ({before.channel.name})", inline=False)
                    embed.add_field(name="> Message ID", value=before.id, inline=False)
                    embed.add_field(name="> Message author", value=before.author.mention, inline=False)
                    embed.add_field(name="> Message created", value=before.created_at.strftime('%Y-%m-%d %I:%M %p'), inline=False)
                    embed.add_field(name="Before", value=before.content, inline=True)
                    embed.add_field(name="After", value=after.content, inline=True)
                    embed.set_thumbnail(url=before.author.avatar)

                    await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages:discord.Message):
        # Prepare the content to be saved to the file
        deleted_content = ""
        for message in messages:
            deleted_content += f"{message.author.display_name}: {message.content}\n"
        
        # Write the deleted content to a file
        with open("assets/misc/deletedtext.txt", "w", encoding="utf-8") as file:
            file.write(deleted_content)

        logs_channel = self.log_channel
        
        with open("assets/misc/deletedtext.txt", "rb") as file:
            file_contents = discord.File(file, filename="deletedtext.txt")
            await logs_channel.send(file=file_contents)

async def setup(bot:commands.Bot):
    await bot.add_cog(MessageLogs(bot))