import discord
from discord.ext import commands

class admin_commands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("admin_commands is ready")

    @commands.command(name='clear', aliases=["purge"])
    @commands.has_role('我在搞')
    async def clear(self, message, channel_id, limit:int =1):
        channel = discord.utils.find(lambda r: r.id == int(channel_id),
                            message.guild.text_channels)
        await channel.purge(limit = limit + 1)


    @commands.command()
    @commands.has_role('我在搞')
    async def delete(self, message, arg:str):
        msg = await message.channel.fetch_message(int(arg))
        await msg.delete()
        await message.message.delete()

async def setup(bot):
    await bot.add_cog(admin_commands(bot))
