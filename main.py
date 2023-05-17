from datetime import datetime, timedelta
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
import openai
import requests

load_dotenv()
TOKEN = os.getenv('TOKEN')
openai.api_key = os.getenv('KEY')
openai.api_base = 'https://api.pawan.krd/v1'

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
conversation_history = []
last_message_time = datetime.now()

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


'''@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
    if isinstance(error, app_commands.errors.MissingRole):
        await interaction.response.send_message("権限がありません")
    else:
        print (error)
        if not interaction.response.is_done:
            await interaction.response.send_message(f'Error {error}')
            pass'''

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != target_meassage_id:
        return
    guild = bot.get_guild(payload.guild_id)
    if payload.emoji.name == '👍':
        role = discord.utils.get(guild.roles, id=1085071207981907969)
        await payload.member.add_roles(role)
    elif payload.emoji.name == '‼️':
        role = discord.utils.get(guild.roles, id=1085070784843751454)
        await payload.member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != target_meassage_id:
        return
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if payload.emoji.name == '👍':
        role = discord.utils.get(guild.roles, id=1085071207981907969)
        await member.remove_roles(role)
    elif payload.emoji.name == '‼️':
        role = discord.utils.get(guild.roles, id=1085070784843751454)
        await member.remove_roles(role)

class curse_buttom(discord.ui.View):
    def __init__(self, message:str):
        super().__init__()
        self.message = message
        self.add_item(discord.ui.Button(label="Yes",style=discord.ButtonStyle.link, url='https://www.youtube.com/@NakiriAyame?sub_confirmation=1'))

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

    if bot.user.mentioned_in(message):
        await message.channel.send('どのようにお手伝いしましょうか')

    if message.channel.name == 'doraemon':
        role = discord.utils.find(lambda r: r.name == '我在搞',
                            message.guild.roles)
        if role not in message.author.roles:
            await message.delete()
            return
        
    curseWord = ['fk', 'fuck', 'tf', 'mom', 'nmsl', 'bitch', 'pussy' , 'shit']

    if any(word in msg_content for word in curseWord):
        await message.delete()
        writer = str(message.author).split("#")[0]
        # await message.channel.send(f'{writer} だめですよ')
        view = curse_buttom(message=message)
        await message.channel.send(f"**{writer}**,\ndo u actually want to say ||{message.content}||?")
        await message.channel.send(view=view)

    role = discord.utils.find(lambda r: r.id == 1085070784843751454,message.guild.roles)
    if role in message.author.roles:
        await message.add_reaction('\U0001F90F')

    await bot.process_commands(message)

@bot.tree.command(name="oppai", description="晉見おっぱい教主")
async def self(interation: discord.Integration):
	embed = discord.Embed(
		color=discord.Colour.red())
	embed.set_image(url='https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/aa5ac6d0-9bc7-40fd-ba34-b9c36388bbd0/d8echfc-f06f9444-90d8-48b5-8c22-9fc2dae773fc.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2FhNWFjNmQwLTliYzctNDBmZC1iYTM0LWI5YzM2Mzg4YmJkMFwvZDhlY2hmYy1mMDZmOTQ0NC05MGQ4LTQ4YjUtOGMyMi05ZmMyZGFlNzczZmMucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.Ug_91_nIwEJuv0VZhZkU8eJudFS5Daj3ajnyHKqXhmw')
	await interation.response.send_message(embed=embed)


@bot.tree.command(name="断る", description="だが断る！")
async def self(interation: discord.Integration):
	embed = discord.Embed(
        color=discord.Colour.blue())
	embed.set_image(url='https://pbs.twimg.com/media/CuLSuuDVMAAWB6p.jpg')
	await interation.response.send_message(embed=embed)

@bot.tree.command(name="pray", description="pray everyday!!!")
async def self(interation: discord.Integration):
	embed = discord.Embed(
		color=discord.Colour.teal())
	embed.set_image(url='https://media.tenor.com/YdDEOK6wfvUAAAAC/mushoku-tensei-roxy-migurdia.gif')
	await interation.response.send_message(embed=embed)


@bot.tree.command(name="help", description="show all commands")
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
    embed.add_field(name='!info',value='infomation about this server',inline=False)
    embed.add_field(name='/chat', value='chat with あやめ', inline=False)
    embed.add_field(name='/search', value='search', inline=False)
    embed.add_field(name=' ', value=' -------------------------------------',inline=False)
    embed.add_field(name='/oppai', value='晉見おっぱい教主', inline=False)
    embed.add_field(name='/断る', value='だが断る！', inline=False)
    embed.add_field(name='/pray', value='pray everyday!!!', inline=False)
    embed.add_field(name=' ', value=' -------------------------------------',inline=False)
    embed.add_field(name='/lol', value='mentions league players', inline=False)
    embed.add_field(name='/build (champion) (position)', value= 'get (champion) build from OP.GG', inline=False)
    embed.add_field(name='/probuild (champion) (position)', value= 'get (champion) build from probuild', inline=False)
    embed.add_field(name='/check (summoner name)', value= 'get sumoner\'s history from OP.GG', inline=False)
    embed.add_field(name=' ', value=' -------------------------------------',inline=False)
    embed.add_field(name='/anime (anime name)', value= 'get anime\'s release date', inline=False)
    embed.add_field(name='/hangman', value='start Hangman',inline=False)
    embed.add_field(name='/g (word or character)', value='guess a word or character in Hangman',inline=False)
    embed.add_field(name='/quit (game)', value='quit that game',inline=False)
    embed.add_field(name='/bj', value='use **H**it, **S**tand, or 🃏(split) to play blackjack',inline=False)
    embed.add_field(name='/credit', value='see everyone\'s credits', inline=False)

    await interation.response.send_message(embed=embed)


@bot.tree.command(name="info", description="show info")
async def self(interation: discord.Integration):
	await interation.response.send_message(f'{interation.user.name}\n這是一個被<@465746027941724161>拋棄的伺服器')
#------------------------------------------------------------------------------------------------------------

@bot.tree.command(name="lol", description="mentions league players")
async def self(interation: discord.Integration):
	"""
	This command mentions league players
	"""
	player = [465746027941724161,586052628807417878,748079858587795456,191052169569370113,808356393216114688,330695143273267201,329554464736280577]
	if interation.user.id in player:
		player.remove(interation.user.id)
	player = ['<@'+str(x)+'>' for x in player]
	await interation.response.send_message('who wants to be carried '+" ".join(player))

@bot.command(name='clear', aliases=["purge"])
@commands.has_role('我在搞')
async def clear(message, limit:int =1):
	await message.channel.purge(limit = limit + 1)


@bot.command()
@commands.has_role('我在搞')
async def delete(message, arg:str):
	msg = await message.channel.fetch_message(int(arg))
	await msg.delete()
	await message.message.delete()

#---------------------League----------------------------------------------------------------

@bot.tree.command(name="check", description="get sumoner\'s history from OP.GG")
async def self(interation: discord.Integration, name:str):
	await interation.response.defer()
	screenshot.screenshot_name(name)
	file = discord.File('screenshot.png', filename='champion.png')
	await interation.followup.send(file=file)


@bot.tree.command(name="build", description="get (champion) build from OP.GG")
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

@bot.tree.command(name="probuild", description="get (champion) build from probuild")
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


@bot.tree.command(name="anime", description="get anime\'s release date")
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

@bot.tree.command(name="g", description="guess a word or character in Hangman")
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

@bot.tree.command(name="quit", description="quit a game")
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

@bot.tree.command(name="blackjack", description="play blackjack")
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


@bot.tree.command(name="credit", description="see everyone\'s credits")
async def self(interation: discord.Integration):
	data = pd.read_csv('credit.csv')
	data = data.set_index('ID')
	data = data.sort_values(by = ['credit'], ascending=False)
	result = "```\n"
	for i in data.index:
		result += "{}: {}\n".format(bot.get_user(i).name,data.loc[i].values[0])
	result += "```"
	await interation.response.send_message(result)

@bot.tree.command(name="podcast", description="podcast")
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



@bot.tree.command(name="chat", description="chat with あやめ")
async def self(interation: discord.Integration, *, message:str):
    await interation.response.defer()
    global last_message_time
    current_time = datetime.now()
    if current_time - last_message_time > timedelta(minutes=5):
        conversation_history.clear()
    conversation_history.append(f"User: {message}")
    print(conversation_history)
    last_message_time = current_time
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=1000,
        messages = [{"role": "user", "content": f"{conversation_history}"}]
    )
    conversation_history.append(f"{response['choices'][0]['message']['content']}")
    embed = discord.Embed(color = discord.Colour.red())
    embed.set_author(name = interation.user, icon_url = interation.user.avatar)
    if not len(message) >= 100:
        embed.add_field(name=' ',value = f"{message}\n",inline=False)
    embed.add_field(name='百鬼あやめ : ',value = f"{response['choices'][0]['message']['content']}",inline=False)
    await interation.followup.send(embed = embed)
    print(response)


@bot.tree.command(name="search", description="search")
async def self(interation: discord.Integration, message:str, output:int = 1):
    await interation.response.defer()
    # Replace with your Bing API key
    if output > 5:
        output = 3
    api_key = os.getenv('BING_KEY')
    headers = {'Ocp-Apim-Subscription-Key': api_key}
    params = {'q': message}
    response = requests.get('https://api.bing.microsoft.com/v7.0/search', headers=headers, params=params)
    data = response.json()
    embed = discord.Embed(color = discord.Colour.red())
    embed.set_author(name = interation.user, icon_url = interation.user.avatar)
    embed.add_field(name='Search results for ',value = f"{message}\n",inline=False)
    print(data)
    await interation.followup.send(embed = embed)
    try:
        results = data['webPages']['value'][:output]
        for result in results:
            title = result['name']
            url = result['url']
            await interation.channel.send(f'{title}\n{url}')
    except KeyError:
        await interation.channel.send('Sorry, no results were found.')

@bot.command()
@commands.has_role('我在搞')
async def sendfile(message, id:str, file:str):
    channel = discord.utils.find(lambda r: r.id == int(id),message.guild.text_channels)
    file = discord.File(f'ayame_image/{file}.jpg', filename='ayame.jpg')
    await channel.send(file=file)

@bot.command()
@commands.has_role('我在搞')
async def test(message, arg:str):
    await message.channel.send(arg)
    print(arg)

bot.run(TOKEN)

