import discord
from discord.ext import commands
from discord import app_commands

@app_commands.command(name="oppai", description="晉見おっぱい教主")
async def oppai(interation: discord.Integration):
    embed = discord.Embed(
        color=discord.Colour.from_rgb(247, 166, 209))
    embed.set_image(url='https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/aa5ac6d0-9bc7-40fd-ba34-b9c36388bbd0/d8echfc-f06f9444-90d8-48b5-8c22-9fc2dae773fc.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2FhNWFjNmQwLTliYzctNDBmZC1iYTM0LWI5YzM2Mzg4YmJkMFwvZDhlY2hmYy1mMDZmOTQ0NC05MGQ4LTQ4YjUtOGMyMi05ZmMyZGFlNzczZmMucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.Ug_91_nIwEJuv0VZhZkU8eJudFS5Daj3ajnyHKqXhmw')
    await interation.response.send_message(embed=embed)


@app_commands.command(name="断る", description="だが断る！")
async def 断る(interation: discord.Integration):
    embed = discord.Embed(
        color=discord.Colour.blue())
    embed.set_image(url='https://pbs.twimg.com/media/CuLSuuDVMAAWB6p.jpg')
    await interation.response.send_message(embed=embed)

@app_commands.command(name="pray", description="pray everyday!!!")
async def pray(interation: discord.Integration):
    embed = discord.Embed(
        color=discord.Colour.teal())
    embed.set_image(url='https://media.tenor.com/YdDEOK6wfvUAAAAC/mushoku-tensei-roxy-migurdia.gif')
    await interation.response.send_message(embed=embed)

async def setup(bot):
    bot.tree.add_command(oppai)
    bot.tree.add_command(断る)
    bot.tree.add_command(pray)
