import os
import asyncio
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
import screenshot
import HangmanGame
import BlackjackGame
import pandas as pd

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Bot is now online')
    await bot.change_presence(activity=discord.Game(name="打敗Goomba總帥並征服世界"))
    try:
        synced = await bot.tree.sync()
        print(f'Sunced {len(synced)} commands')
    except Exception as e:
        print(e)



target_meassage_id = 1085077296555249684


@bot.event
async def on_command_error(message, error):
    if isinstance(error, commands.CommandNotFound):
        await message.channel.send('コマンド存在しません')
    elif isinstance(error, commands.CheckFailure):
        await message.channel.send("権限がありません")
    elif isinstance(error, commands.MissingRequiredArgument):
        await message.channel.send('必須の引数がありません')
    elif isinstance(error, commands.CommandInvokeError):
        print(error)
        pass
    else:
        await message.channel.send(f'Error {error}')
        pass


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
    if isinstance(error, app_commands.errors.MissingRole):
        await interaction.response.send_message("権限がありません")
    else:
        print (error)
        if not interaction.response.is_done:
            await interaction.response.send_message(f'Error {error}')
            pass

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != target_meassage_id:
        return
    guild = bot.get_guild(payload.guild_id)
    if payload.emoji.name == '👍':
        role = discord.utils.get(guild.roles, name='tits licker')
        await payload.member.add_roles(role)
    elif payload.emoji.name == '‼️':
        role = discord.utils.get(guild.roles, name='cock sucker')
        await payload.member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != target_meassage_id:
        return
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    
    if payload.emoji.name == '👍':
        role = discord.utils.get(guild.roles, name='tits licker')
        await member.remove_roles(role)
    elif payload.emoji.name == '‼️':
        role = discord.utils.get(guild.roles, name='cock sucker')
        await member.remove_roles(role)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    try:
        front = message.content.index('<:')
        end = message.content.index('>')
        msg_content = message.content[:front] + message.content[end+1:].lower()
    except ValueError:
        msg_content = message.content.lower()
        
    if message.channel.name == 'doraemon':
        role = discord.utils.find(lambda r: r.name == '我在搞',
                            message.guild.roles)
        if role not in message.author.roles:
            await message.delete()
            return
    
    curseWord = ['fk', 'fuck', 'tf', 'mom', 'nmsl', 'bitch', 'pussy' , 'mother', 'shit']
    
    if any(word in msg_content for word in curseWord):
        await message.delete()
        writer = str(message.author).split("#")[0]
        await message.channel.send(f'{writer} だめですよ')
        return
    
    role = discord.utils.find(lambda r: r.name == 'cock sucker',message.guild.roles)
    if role in message.author.roles:
        await message.add_reaction('\U0001F90F')
        
    if '!!' not in message.content:
        await bot.process_commands(message)

@bot.tree.command(name="oppai", description="oppai")
async def self(interation: discord.Integration):
	embed = discord.Embed(
		color=discord.Colour.red())
	embed.set_image(url='https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/aa5ac6d0-9bc7-40fd-ba34-b9c36388bbd0/d8echfc-f06f9444-90d8-48b5-8c22-9fc2dae773fc.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2FhNWFjNmQwLTliYzctNDBmZC1iYTM0LWI5YzM2Mzg4YmJkMFwvZDhlY2hmYy1mMDZmOTQ0NC05MGQ4LTQ4YjUtOGMyMi05ZmMyZGFlNzczZmMucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.Ug_91_nIwEJuv0VZhZkU8eJudFS5Daj3ajnyHKqXhmw')
	await interation.response.send_message(embed=embed)


@bot.tree.command(name="断る", description="断る")
async def self(interation: discord.Integration):
	embed = discord.Embed(
        color=discord.Colour.blue())
	embed.set_image(url='https://pbs.twimg.com/media/CuLSuuDVMAAWB6p.jpg')
	await interation.response.send_message(embed=embed)

@bot.tree.command(name="pray", description="pray everyday")
async def self(interation: discord.Integration):
	embed = discord.Embed(
		color=discord.Colour.teal())
	embed.set_image(url='https://media.tenor.com/YdDEOK6wfvUAAAAC/mushoku-tensei-roxy-migurdia.gif')
	await interation.response.send_message(embed=embed)


@bot.tree.command(name="help", description="show all help")
async def self(interation: discord.Integration):
	embed = discord.Embed(
        title='百鬼あやめです',
		description=
		'Please subscribe あやめ on YouTube\n https://www.youtube.com/@NakiriAyame',
		color=discord.Colour.red())
	embed.set_image(url='https://w0.peakpx.com/wallpaper/190/23/HD-wallpaper-anime-virtual-youtuber-hololive-nakiri-ayame.jpg')
	embed.set_thumbnail(
		url=
		'https://static.wikia.nocookie.net/virtualyoutuber/images/0/09/Nakiri_Ayame_Portrait.png/revision/latest?cb=20190215184953'
	)
	embed.add_field(name='!info',
        value='infomation about this server',
		inline=False)
	embed.add_field(name=' ', value=' -------------------------------------',inline=False)
	embed.add_field(name='!おっぱい/oppai', value='晉見おっぱい教主', inline=False)
	embed.add_field(name='!断る', value='だが断る！', inline=False)
	embed.add_field(name='!pray', value='pray everyday!!!', inline=False)
	embed.add_field(name=' ', value=' -------------------------------------',inline=False)
	embed.add_field(name='!lol', value='mentions league players', inline=False)
	embed.add_field(name='!build (champion) (position)', value= 'get (champion) build from OP.GG', inline=False)
	embed.add_field(name='!probuild (champion) (position)', value= 'get (champion) build from probuild', inline=False)
	embed.add_field(name='!check (summoner name)', value= 'get sumoner\'s history from OP.GG', inline=False)
	embed.add_field(name=' ', value=' -------------------------------------',inline=False)
	embed.add_field(name='!anime (anime name)', value= 'get anime\'s release date', inline=False)
	embed.add_field(name='!hangman', value='start Hangman',inline=False)
	embed.add_field(name='!guess (word or character)', value='guess a word or character in Hangman',inline=False)
	embed.add_field(name='!quit (game)', value='quit that game',inline=False)
	embed.add_field(name='!bj', value='use **H**it, **S**tand, or 🃏(split) to play blackjack',inline=False)
	embed.add_field(name='!credit', value='see everyone\'s credits', inline=False)
  
	await interation.response.send_message(embed=embed)


@bot.tree.command(name="info", description="show info")
async def self(interation: discord.Integration):
	await interation.response.send_message(f'{interation.user.name}\n這是一個被<@465746027941724161>拋棄的伺服器')
#------------------------------------------------------------------------------------------------------------

@bot.tree.command(name="lol", description="lol")
async def self(interation: discord.Integration):
	"""
	This command mentions league players
	"""
	player = [465746027941724161,586052628807417878,748079858587795456,191052169569370113,191052169569370113,330695143273267201]
	if interation.user.id in player:
		player.remove(interation.user.id)
	player = ['<@'+str(x)+'>' for x in player]
	await interation.response.send_message('who wants to be carried '+" ".join(player))
        
@bot.command(name='clear', aliases=["purge"])
@commands.has_role('我在搞')
async def clear(message, limit=1):
	await message.channel.purge(limit = limit + 1)


@bot.command()
@commands.has_role('我在搞')
async def delete(message, arg):
	msg = await message.channel.fetch_message(arg)
	await msg.delete()
	await message.message.delete()

#---------------------League----------------------------------------------------------------

@bot.tree.command(name="check", description="check")
async def self(interation: discord.Integration, name:str):
	await interation.response.defer()
	screenshot.screenshot_name(name)
	file = discord.File('screenshot.png', filename='champion.png')
	await interation.followup.send(file=file)

 
@bot.tree.command(name="build", description="build")
@app_commands.describe(role = "roles")
@app_commands.choices(role = [
	discord.app_commands.Choice(name='top', value=1),
	discord.app_commands.Choice(name='jungle', value=2),
	discord.app_commands.Choice(name='mid', value=3),
	discord.app_commands.Choice(name='adc', value=4),
	discord.app_commands.Choice(name='sup', value=5),

])
async def self(interation: discord.Integration, champion:str, role: discord.app_commands.Choice[int]):
	await interation.response.defer()
	screenshot.screenshot(champion, role.name)
	file = discord.File('screenshot.png', filename='champion.png')
	await interation.followup.send(file=file)

@bot.tree.command(name="probuild", description="probuild")
@app_commands.describe(role = "roles")
@app_commands.choices(role = [
    discord.app_commands.Choice(name='top', value=1),
    discord.app_commands.Choice(name='jungle', value=2),
    discord.app_commands.Choice(name='mid', value=3),
    discord.app_commands.Choice(name='adc', value=4),
    discord.app_commands.Choice(name='supp', value=5),

])
async def self(interation: discord.Integration, champion:str, role: discord.app_commands.Choice[int]):
    await interation.response.defer()
    ben = discord.utils.find(lambda r: r.name == 'tits licker',interation.guild.roles)
    if ben in interation.user.roles:
       lpl = True
    else:
        lpl = False
    screenshot.screenshot_pro(champion, role.name, lpl)
    file = discord.File('screenshot.png', filename='champion.png')
    await interation.followup.send(file=file)
    

@bot.tree.command(name="anime", description="search anime")
async def self(interation: discord.Integration, name:str):
    await interation.response.defer()
    screenshot.screenshot_anime(name.split())
    file = discord.File('screenshot.png', filename=f'{name}.png')
    await interation.followup.send(file=file)

#----------------------HangMan-----------------------------------------------------------------------

@bot.tree.command(name="hangman", description="play hangman")
async def self(interation: discord.Integration):
    if interation.channel.id in HangmanGame.games:
        await interation.response.send_message("There's already a game in progress in this channel!")
    else:
        HangmanGame.games[interation.channel.id] = HangmanGame.HangmanGame(interation.channel)
        await interation.response.send_message('Starting a new game of Hangman! The word has {} letters.'.format(len(HangmanGame.games[interation.channel.id].word)))
        await HangmanGame.games[interation.channel.id].start_game()

@bot.tree.command(name="g", description="guess hangman")
async def self(interation: discord.Integration, guess:str):
    await interation.response.defer()
    if interation.channel.id not in HangmanGame.games:
        await interation.followup.send('START FIRST')
        return
    if (len(guess)>len(HangmanGame.games[interation.channel.id].word)):
        await interation.followup.send('Didn\'t ur parents teach u how to play hangman?')
        return
    if not guess.isalpha():
        await interation.followup.send('Didn\'t ur parents teach u how to play hangman?')
        return
    if len(guess)==1:
        if not guess.isalpha():
            await interation.followup.send('Didn\'t ur parents teach u how to play hangman?')
            return
    guess = guess.lower()
    await interation.followup.send(f'{interation.user.name} guesses **{guess}**')
    await HangmanGame.games[interation.channel.id].guess(guess)
  
@bot.tree.command(name="quit", description="quit game")
@app_commands.checks.has_role('我在搞')
@app_commands.describe(game = "games")
@app_commands.choices(game = [
    discord.app_commands.Choice(name='hangman', value=1),
    discord.app_commands.Choice(name='blackjack', value=2),
])
async def self(interation: discord.Integration, game:discord.app_commands.Choice[int]):
    if (game.value == 1):
        await interation.response.send_message(f'The answer is {HangmanGame.games[interation.channel.id].word}')
        HangmanGame.games[interation.channel.id].end_game(interation.channel.id)
    if (game.value == 2):
        del BlackjackGame.games[interation.channel.id]
        await interation.response.send_message('Blackjack ends')
#----------------------BlackJack-----------------------------------------------------------------------

@bot.tree.command(name="blackjack", description="blackjack")
async def self(interation: discord.Integration):
	data = pd.read_csv('credit.csv')
	data = data.set_index('ID')
	target = 0
	if (interation.channel.id in BlackjackGame.games):
		await interation.response.send_message("There's already a game in progress in this channel!")
		pass
	await interation.response.send_message('Place your bets if u want to play BlackJack')
	async for msg in interation.channel.history(limit=1):
		target = msg.id
		await msg.add_reaction('5️⃣')
		await msg.add_reaction('🔟')
	await asyncio.sleep(5)
	msg = await interation.channel.fetch_message(target)
	await msg.remove_reaction('5️⃣', bot.user)
	await msg.remove_reaction('🔟', bot.user)
	five = [user async for user in msg.reactions[0].users()]
	ten = [user async for user in msg.reactions[1].users()]
	for player in five:
		if data.loc[player.id].values[0] < 5:
			await interation.channel.send(f'{player.name} don\'t have enongh credits!')
			five.remove(player)
	for player in ten:
		if data.loc[player.id].values[0] < 10:
			await interation.channel.send(f'{player.name} don\'t have enongh credits!')
			ten.remove(player)
	users = five + ten
	if len(users) == 0:
		await interation.channel.send('おまえらはみんな小心者だ')
		end = discord.File('ayame_image/ayame_victory.jpg', filename='loser.jpg')
		await interation.channel.send(file = end)
		return
	BlackjackGame.games[interation.channel.id] = BlackjackGame.Blackjack(interation.channel,bot.user, five, ten)
	await BlackjackGame.games[interation.channel.id].start_game()
	result, no_one_win = await BlackjackGame.games[interation.channel.id].end()
	if not no_one_win:
		end = discord.File('ayame_image/ayame_ya.jpg', filename='ya.jpg')
		await interation.channel.send(file = end)
	else:
		end = discord.File('ayame_image/ayame_victory.jpg', filename='loser.jpg')
		await interation.channel.send(file = end)
	await interation.channel.send(result)
	del BlackjackGame.games[interation.channel.id]
        

@bot.tree.command(name="credit", description="see credit")
async def self(interation: discord.Integration):
	data = pd.read_csv('credit.csv')
	data = data.set_index('ID')
	data = data.sort_values(by = ['credit'], ascending=False)
	result = "```\n"
	for i in data.index:
		result += "{}: {}\n".format(bot.get_user(i).name,data.loc[i].values[0])
	result += "```"
	await interation.response.send_message(result)

@bot.tree.command(name="test", description="test")
@app_commands.checks.has_role('我在搞')
async def self(interation: discord.Integration, id:str, arg:str):
    await interation.response.send_message(arg)
    channel = discord.utils.find(lambda r: r.id == int(id),
                            interation.guild.text_channels)
    await channel.send(f'**{arg}**')
    print(arg)

@bot.command()
@commands.has_role('我在搞')
async def add(message, user, amount):
    data = pd.read_csv('credit.csv')
    data = data.set_index('ID')
    user = await commands.MemberConverter().convert(ctx = message,argument = user)
    data.loc[user.id].values[0] += int(amount)
    data.to_csv('credit.csv')
    await message.channel.send(f'{user.name} now has {data.loc[user.id].values[0]} credits')

bot.run(TOKEN)

