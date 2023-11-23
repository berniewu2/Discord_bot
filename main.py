from datetime import datetime, timedelta
import os
import json
import asyncio
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands, tasks
import screenshot
import HangmanGame
import BlackjackGame
import pandas as pd
import openai
import requests as r
from myanimelistAPI import MyAnimeListAPI
from jikan4pyAPI import JikanAPI
from utilities import print_bot, isInteger, jsonOP
from AnilistPython import Anilist
from bs4 import BeautifulSoup
from random import choice, randint


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
openai.api_key = os.getenv('API_KEY')
openai.api_base = os.getenv('API_BASE')
ANIME_API_ID = os.getenv('ANIME_API_ID')

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
    scrapeAiringAnime.start()

@bot.event
async def setup_hook():
    cogslist =["cogs.admin_commands","cogs.customized"]
    for ext in cogslist:
        await bot.load_extension(ext)
        print(f'{ext} is ready')


with open("useragents.txt", 'r') as f:
    HEADERS = [{'User-Agent': header} for header in f.read().splitlines()]

DOMAIN = "https://gogoanimehd.io/"
MAL_DOMAIN = "https://myanimelist.net/anime/"
JSONFILENAME = "series.json"
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
MAL_CLIENT_ID = os.getenv("MAL_CLIENT_ID")
DISCORD_TAG = "<@465746027941724161>"

mal_api = MyAnimeListAPI(MAL_CLIENT_ID)
jikan_api = JikanAPI()
anilist_api = Anilist()
jsonOP = jsonOP(JSONFILENAME)
malID_to_aniListID = {}

target_meassage_id = 1085077296555249684
conversation_history = []
last_message_time = datetime.now()
curseWord = ['fk', 'fuck', 'wtf', 'mom', 'nmsl', 'bitch', 'pussy' , 'shit']

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

    # if bot.user.mentioned_in(message):
    #     global last_message_time
    #     current_time = datetime.now()
    #     if current_time - last_message_time > timedelta(minutes=5):
    #         conversation_history.clear()
    #     print(message.content)
    #     front = message.content.index('<')
    #     end = message.content.index('>')
    #     msg_content = message.content[:front] + message.content[end+1:]
    #     conversation_history.append(f"{message.author.name}: {msg_content}")
    #     print(conversation_history)
    #     last_message_time = current_time
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         max_tokens=256,
    #         messages = [
    #             {"role": "system", "content": f"You are 百鬼あやめ, admin of this discord server. Now is {datetime.now().isoformat(' ', 'seconds')}"},
    #             {"role": "user", "content": f"{conversation_history}"}]
    #     )
    #     conversation_history.append(f"{response['choices'][0]['message']['content']}")
    #     print(conversation_history)
    #     answer = response['choices'][0]['message']['content']
    #     if len(answer) > 1000:
    #         answer = answer[:999] 
    #     await message.channel.send(answer)
    #     print(response)

    if message.channel.name == 'doraemon':
        role = discord.utils.find(lambda r: r.name == '我在搞',
                            message.guild.roles)
        if role not in message.author.roles:
            await message.delete()
            return
        
    # global curseWord

    # if any(word in msg_content for word in curseWord):
    #     await message.delete()
    #     writer = str(message.author.global_name)
    #     view = curse_buttom(message=message)
    #     if writer == "None":
    #         writer == str(message.author.name)
    #     await message.channel.send(f"**{writer}**,\ndo u actually want to say ||{message.content}||?")
    #     await message.channel.send(view=view)

    role = discord.utils.find(lambda r: r.id == 1085070784843751454,message.guild.roles)
    if role in message.author.roles:
        await message.add_reaction('\U0001F90F')

    await bot.process_commands(message)



@bot.tree.command(name="help", description="show all commands")
async def self(interation: discord.Integration):
    embed = discord.Embed(
        title='百鬼あやめです',
        description=
        'Mention あやめ to chat \n https://www.youtube.com/@NakiriAyame',
        color=discord.Colour.red())
    embed.set_image(url='https://w0.peakpx.com/wallpaper/190/23/HD-wallpaper-anime-virtual-youtuber-hololive-nakiri-ayame.jpg')
    embed.set_thumbnail(
        url=
        'https://static.wikia.nocookie.net/virtualyoutuber/images/0/09/Nakiri_Ayame_Portrait.png/revision/latest?cb=20190215184953'
    )
    embed.add_field(name='/info',value='infomation about this server',inline=False)
    embed.add_field(name='/search', value='search', inline=False)
    embed.add_field(name=' ', value=' -------------------------------------',inline=False)
    embed.add_field(name='/oppai', value='晉見おっぱい教主', inline=False)
    embed.add_field(name='/断る', value='だが断る！', inline=False)
    embed.add_field(name='/pray', value='pray everyday!!!', inline=False)
    embed.add_field(name=' ', value=' -------------------------------------',inline=False)
    embed.add_field(name='/lol', value='mentions league players', inline=False)
    embed.add_field(name='/tft', value='mentions tft players', inline=False)
    embed.add_field(name='/check', value= 'check summoner from OP.GG', inline=False)
    embed.add_field(name=' ', value=' -------------------------------------',inline=False)
    embed.add_field(name='/anime (anime name)', value= 'get anime\'s info', inline=False)
    embed.add_field(name='/add_anime (anime name)', value= 'add an anime to the list', inline=False)
    embed.add_field(name='/remove_anime', value= 'remove an anime from the list', inline=False)
    embed.add_field(name='/list_anime', value= 'see all tracking anime', inline=False)
    embed.add_field(name=' ', value=' -------------------------------------',inline=False)
    embed.add_field(name='/hangman', value='start Hangman',inline=False)
    embed.add_field(name='/g (word or character)', value='guess a word or character in Hangman',inline=False)
    embed.add_field(name='/quit (game)', value='quit that game',inline=False)
    embed.add_field(name='/bj', value='use **H**it, **S**tand, or 🃏(split) to play blackjack',inline=False)
    embed.add_field(name='/credit', value='see everyone\'s credits', inline=False)

    await interation.response.send_message(embed=embed)


@bot.tree.command(name="info", description="show info")
async def self(interation: discord.Integration):
    await interation.response.send_message(f'{interation.user.global_name}\n這是一個被<@465746027941724161>拋棄的伺服器')
#------------------------------------------------------------------------------------------------------------

@bot.tree.command(name="lol", description="mentions league players")
async def self(interation: discord.Integration, message:str = 'who wants to be carried '):
    """
    This command mentions league players
    """
    global curseWord
    if any(word in message for word in curseWord):
        message = 'who wants to be carried '
    player = [465746027941724161,586052628807417878,808356393216114688,330695143273267201]
    if interation.user.id in player:
        player.remove(interation.user.id)
    player = ['<@'+str(x)+'>' for x in player]
    await interation.response.send_message(message+" ".join(player))

@bot.tree.command(name="tft", description="mentions tft players")
async def self(interation: discord.Integration, message:str = ' 同行演我8'):
    """
    This command mentions league players
    """
    global curseWord
    if any(word in message for word in curseWord):
        message = ' 同行演我8'
    player = [465746027941724161,586052628807417878,808356393216114688]
    if interation.user.id in player:
        player.remove(interation.user.id)
    player = ['<@'+str(x)+'>' for x in player]
    await interation.response.send_message(" ".join(player)+ message)

#---------------------League----------------------------------------------------------------

# @bot.tree.command(name="build", description="get (champion) build from OP.GG")
# @app_commands.describe(role = "roles")
# @app_commands.choices(role = [
# 	discord.app_commands.Choice(name='top', value=1),
# 	discord.app_commands.Choice(name='jungle', value=2),
# 	discord.app_commands.Choice(name='mid', value=3),
# 	discord.app_commands.Choice(name='adc', value=4),
# 	discord.app_commands.Choice(name='sup', value=5),

# ])
# async def self(interation: discord.Integration, champion:str, role: discord.app_commands.Choice[int]):
# 	await interation.response.defer()
# 	screenshot.screenshot(champion, role.name)
# 	file = discord.File('screenshot.png', filename='champion.png')
# 	await interation.followup.send(file=file)

# @bot.tree.command(name="probuild", description="get (champion) build from probuild")
# @app_commands.describe(role = "roles")
# @app_commands.choices(role = [
#     discord.app_commands.Choice(name='top', value=1),
#     discord.app_commands.Choice(name='jungle', value=2),
#     discord.app_commands.Choice(name='mid', value=3),
#     discord.app_commands.Choice(name='adc', value=4),
#     discord.app_commands.Choice(name='supp', value=5),

# ])
# async def self(interation: discord.Integration, champion:str, role: discord.app_commands.Choice[int]):
#     await interation.response.defer()
#     ben = discord.utils.find(lambda r: r.name == 'tits licker',interation.guild.roles)
#     if ben in interation.user.roles:
#        lpl = True
#     else:
#         lpl = False
#     screenshot.screenshot_pro(champion, role.name, lpl)
#     file = discord.File('screenshot.png', filename='champion.png')
#     await interation.followup.send(file=file)

@bot.tree.command(name="check", description="check")
async def self(interation: discord.Integration, name:str, games:int = 5):
    if games > 10:
        games = 5
    api = os.getenv('ROIT_API')
    await interation.response.defer()
    request = r.get(f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={api}')
    print(request)
    if request.status_code == 404 or request.status_code == 403:
        await interation.followup.send(name + " " + request.reason)
        return
    request = (request.json())
    print(request)
    id = request['puuid']
    req = r.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{id}/ids?start=0&count=20&api_key={api}')
    embed = discord.Embed(
        title=f'{request["name"]}',
        color=discord.Colour.dark_gold())
    await interation.followup.send(name)
    pages = []
    for i in range(games):
        game = r.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/{req.json()[i]}?api_key={api}').json()
        if game['info']['participants'][game['metadata']['participants'].index(id)]['win']:
            embed = discord.Embed(color=discord.Colour.blue())
        else:
            embed = discord.Embed(color=discord.Colour.red())
        embed.add_field(name=game['info']['gameMode']+f'            {i+1}/{games}',value=str(datetime.fromtimestamp(round(game['info']['gameCreation']/1000))),inline=False)
        for i in range(int(len(game['info']['participants'])/2)): #[game['metadata']['participants'].index(id)]
            player = game['info']['participants'][i]
            if player['puuid'] == id:
                embed.add_field(name='',value=f'\t**{player["championName"]}   {player["kills"]}/{player["deaths"]}/{player["assists"]}**',inline=True)
            else:
                embed.add_field(name='',value=f'\t{player["championName"]}   {player["kills"]}/{player["deaths"]}/{player["assists"]}',inline=True)
            player = game['info']['participants'][i+5]
            if player['puuid'] == id:
                embed.add_field(name='',value=f'\t**{player["championName"]}   {player["kills"]}/{player["deaths"]}/{player["assists"]}**',inline=True)
            else:
                embed.add_field(name='',value=f'\t{player["championName"]}   {player["kills"]}/{player["deaths"]}/{player["assists"]}',inline=True)
            embed.add_field(name='\u200B', value='\u200B')
            print(player["championName"])
        pages.append(embed)
        

    buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end
    current = 0
    msg = await interation.channel.send(embed=pages[current])
    
    for button in buttons:
        await msg.add_reaction(button)
        
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == interation.user and reaction.emoji in buttons, timeout=60.0)

        except asyncio.TimeoutError:
            return print("test")

        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0
                
            elif reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1
                    
            elif reaction.emoji == u"\u27A1":
                if current < len(pages)-1:
                    current += 1

            elif reaction.emoji == u"\u23E9":
                current = len(pages)-1

            for button in buttons:
                await msg.remove_reaction(button, interation.user)

            if current != previous_page:
                await msg.edit(embed=pages[current])

@bot.tree.command(name="anime", description="get anime\'s info")
async def self(interation: discord.Integration, name:str):
    channel = interation.channel
    await interation.response.defer()
    request = r.get(f'https://api.jikan.moe/v4/anime?q={name}&sfw')
    data = request.json()['data']
    data = list(filter(lambda x: x['status']=='Not yet aired' or x['status']== 'Currently Airing',data))
    
    name = (data[0]['title_english'] or data[0]['title'])
    await interation.followup.send(name)
    req = r.get(f'https://api.simkl.com/search/anime?q={name}&client_id={ANIME_API_ID}')
    print(req.json()[0]["ids"]["simkl_id"])

    request = r.get(f'https://api.simkl.com/anime/episodes/{req.json()[0]["ids"]["simkl_id"]}?client_id={ANIME_API_ID}')
    print(request.json())

    
    pages = []
    for anime in data:
        embed = discord.Embed(
        title=f'{name}',
        color=discord.Colour.dark_gold())
        embed.add_field(name="",value=f'{data.index(anime)+1}/{len(data)}',inline=False)

        embed.set_image(url=anime['images']['jpg']['large_image_url'])
        title = anime['title_japanese']
        if anime['title_english'] != None:
            title += " / "
            title += anime['title_english']
        embed.add_field(name='title',value=title,inline=False)
        embed.add_field(name='status',value=anime['status'],inline=False)
        embed.add_field(name='score',value=anime['score'],inline=False)
        embed.add_field(name='episodes',value=anime['episodes'],inline=False)
        embed.add_field(name='date',value=anime['aired']['string'],inline=False)

        pages.append(embed)
    print(len(pages))
    if len(pages) == 0:
        await channel.send("Not found")
        return
    buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end
    current = 0
    msg = await interation.channel.send(embed=pages[current])
    
    for button in buttons:
        await msg.add_reaction(button)
        
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == interation.user and reaction.emoji in buttons, timeout=60.0)

        except asyncio.TimeoutError:
            return print("TimeoutError")

        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0
                
            elif reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1
                    
            elif reaction.emoji == u"\u27A1":
                if current < len(pages)-1:
                    current += 1

            elif reaction.emoji == u"\u23E9":
                current = len(pages)-1

            for button in buttons:
                await msg.remove_reaction(button, interation.user)

            if current != previous_page:
                await msg.edit(embed=pages[current])
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
        await interation.followup.send('長すぎ')
        return
    if not guess.isalpha():
        await interation.followup.send('英語だけお願いします')
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
    await message.channel.send(f'{user.global_name} now has {data.loc[user.id].values[0]} credits')

'''@bot.tree.command(name="image", description="generate image")
async def self(interation: discord.Integration, message:str, amount:int = 1):
    channel = interation.channel
    if (amount > 3) | (amount < 1):
        amount = 1
    await interation.response.defer()
    response = openai.Image.create(
        prompt=message,
        n=amount,
        size="1024x1024",
    )
    image_url = response['data'][0]['url']
    await interation.followup.send(image_url)
    print(response)
    if amount > 1:
        await channel.send(response['data'][1]['url'])
    if amount > 2:
        await channel.send(response['data'][2]['url'])
'''

@bot.tree.command(name="search", description="search")
async def self(interation: discord.Integration, message:str, output:int = 1):
    await interation.response.defer()
    # Replace with your Bing API key
    if output > 5:
        output = 3
    api_key = os.getenv('BING_KEY')
    headers = {'Ocp-Apim-Subscription-Key': api_key}
    params = {'q': message}
    response = r.get('https://api.bing.microsoft.com/v7.0/search', headers=headers, params=params)
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



def malIDtoAniListID(anime_id):
    """
    Converts the MAL ID to AniList ID
    using GraphQL
    """
    if anime_id in malID_to_aniListID:
        return malID_to_aniListID[anime_id]

    query = """query
        ($id: Int, $type: MediaType) {
            Media(idMal: $id, type: $type) {
                id}
            }
        """
    variables = {'id': anime_id, 'type': 'ANIME'}
    url = 'https://graphql.anilist.co'
    response = r.post(url, json={'query': query, 'variables': variables})
    malID_to_aniListID[anime_id] = int(response.json()['data']['Media']['id'])
    return malID_to_aniListID[anime_id]


def timeTillNextEpisode(anime_id):
    """
    Returns the time till the next episode of the anime airs
    """
    query = """query ($id: Int) {
                    Media(idMal: $id, type: ANIME) {
                        id
                        nextAiringEpisode {
                        timeUntilAiring
                        }
                    }
                }
    """
    variables = {'id': anime_id, 'type': 'ANIME'}
    url = 'https://graphql.anilist.co'
    data = r.post(url, json={'query': query, 'variables': variables}).json()

    try: # if parsing fails, then the anime is not airing
        time_data = data['data']['Media']['nextAiringEpisode']
    except:
        time_data = None

    if time_data is not None:
        seconds = time_data['timeUntilAiring']
    else:
        return {"days": 0,
                "hours": 0,
                "minutes": 0,
                "seconds": 0,
                "total_seconds": 0,
                "isNull": True}

    time = timedelta(seconds=seconds)
    return {"days": time.days,
            "hours": time.seconds//3600,
            "minutes": (time.seconds//60) % 60,
            "seconds": time.seconds % 60,
            "total_seconds": seconds,
            "isNull": False}


def isAnimeAiring(anime_id, api="mal"):
    """
    Checks if the anime is airing
    using the MyAnimeList API (atleast more updated then the Jikan API due to less caching)
    """
    if api == "mal":
        try:
            result = mal_api.getAnimeByID(anime_id)
            return (result['status'] != "finished_airing")
        except Exception as e:
            print_bot(
                f"Error: Mal API ID check failed, so switching to Jikan API.\n'{e}'")
            result = jikan_api.getAnimeByID(anime_id)
            return result["status"] != "Finished Airing"
    else:
        result = jikan_api.getAnimeByID(anime_id)
        return result["status"] != "Finished Airing"


def episodeEmbedCard(anime_id, episode_number, video_link, airing=True):
    """
    Creates an embed card for the episode
    """
    anime = jikan_api.getAnimeByID(anime_id)

    description = f"Episode {episode_number}"
    if not airing:
        description += " (Final Episode)"

    embed = discord.Embed(title=anime['title'],
                  description=description, color=0x00ff00)
    embed.set_thumbnail(url=anime['images']['jpg']['image_url'])
    embed.set_footer(text="by あやめ")
    embed.set_image(url=anime['images']['jpg']['image_url'])
    embed.add_field(name="MyAnimeList",
                    value=f"[Link](https://myanimelist.net/anime/{anime_id})", inline=False)
    embed.add_field(name="Episode", value=f"[Link]({video_link})", inline=True)
    return embed


def animeListEmbedCard(anime_series):
    """
    Creates an embed card for the anime list
    """
    embed = discord.Embed(title="Currently Tracking Anime", color=0xff0000)
    embed.set_footer(text="by あやめ")

    fields = []
    for anime in anime_series:
        anime_name, episode_number, anime_id = anime
        mal_anime_link = MAL_DOMAIN + str(anime_id)

        nextEpTime = timeTillNextEpisode(anime_id)
        if nextEpTime["isNull"]:
            time = "N/A"
        elif nextEpTime["days"] == 0 and nextEpTime["hours"] == 0 and nextEpTime["minutes"] == 0:
            time = f"{nextEpTime['seconds']} seconds"
        elif nextEpTime["days"] == 0 and nextEpTime["hours"] == 0:
            time = f"{nextEpTime['minutes']} minutes"
        elif nextEpTime["days"] == 0:
            time = f"{nextEpTime['hours']} hours and {nextEpTime['minutes']} minutes"
        else:
            time = f"{nextEpTime['days']} days, {nextEpTime['hours']} hours and {nextEpTime['minutes']} minutes"

        episode_field = f"Episode {episode_number}" if episode_number != - \
            1 else "Episode Did Not Air"
        episode_field += "\n" + f"Airing in {time}"
        episode_field += "\n" + f"[anime]({mal_anime_link})"
        fields.append((anime_name, episode_field, nextEpTime["total_seconds"]))

    fields.sort(key=lambda x: x[2])
    for anime_name, episode_field, _ in fields:
        embed.add_field(name=anime_name, value=episode_field, inline=True) #format
    return embed


def animeSelectionEmbedCards(animes):
    embeds = [discord.Embed(title="Which Anime to Add?", color=0xffff00)]
    anime_titles = [anime["title"] for anime in animes]
    longest_title_length = max([len(title) for title in anime_titles])
    en_space = " "
    invisible_space = "‎"
    for i, title in enumerate(anime_titles, 1):
        embed = discord.Embed(url=f"https://www.lol{i}.com", color=0xff00ff)
        space_length = longest_title_length - len(title) + title.count(":")
        embed.add_field(name=f"{i}.\n{title}"+space_length*en_space+invisible_space, value=invisible_space, inline=False)
        embed.set_thumbnail(url = animes[i-1]["images"]["jpg"]["image_url"])
        embeds.append(embed)
    return embeds

# bot.slash_command(guild_ids=[id1, id2]) for specific commands in specific guilds
def animeSelectionRemoveEmbed(anime_titles):
    # one embed with all the anime titles
    embed = discord.Embed(title="Which Anime to Remove?", color=0xffff00)
    longest_title_length = max([len(title) for title in anime_titles])
    en_space = " "
    invisible_space = "‎"
    for i, title in enumerate(anime_titles, 1):
        space_length = longest_title_length - len(title) + title.count(":")
        embed.add_field(name=f"{i}.\n{title}"+space_length*en_space+invisible_space, value=invisible_space, inline=False)
    return embed


@bot.tree.command(name="add_anime",description="Adds an anime to the list")
async def self(interaction: discord.Integration, name: str):
    channel = interaction.channel
    print_bot(f"Adding New Anime")
    animes = jikan_api.searchAnime(anime_name=name)
    anime_titles = [anime['title_english'] or anime["title"] for anime in animes]
    print_bot(f"Querying for '{name}'")
    print_bot(f"Choices are: '{', '.join(anime_titles)}'")
    options = [discord.SelectOption(label=i, value=i-1)
               for i in range(1, len(anime_titles)+1)]
    select = discord.ui.Select(placeholder="", options=options)

    async def my_callback(interaction: discord.Interaction):
        selectedAnime = anime_titles[int(select.values[0])]
        anime_id = jikan_api.getAnimeIDByName(anime_name=selectedAnime)
        registered_series = jsonOP.loadJSON()["series"]

        if all(selectedAnime not in registeredanime for registeredanime in registered_series):
            registered_series.append([selectedAnime, -1, anime_id])
            jsonOP.saveJSON({"series": registered_series})
            print_bot(f"Added '{selectedAnime}' to the list")
            await channel.send(f"Added {selectedAnime} to the list")
        else:
            print_bot(f"{selectedAnime} is already in the list")
            await channel.send(f"{selectedAnime} is already in the list")

    select.callback = my_callback
    view = discord.ui.View()
    view.add_item(select)

    await interaction.response.send_message("Which Anime To Add?", view=view, embeds=animeSelectionEmbedCards(animes), delete_after = 15)

@bot.tree.command(name="remove_anime", description="Removes an anime from the list")
async def self(interaction: discord.Interaction):
    channel = interaction.channel
    print_bot(f"Removing Anime")
    # anime_titles = jikan_api.searchAnimeTitles(anime_name=name)
    anime_titles = [anime[0] for anime in jsonOP.loadJSON()["series"]]
    # print_bot(f"Querying for '{name}'")
    print_bot(f"Choices are: '{', '.join(anime_titles)}'")
    options = [discord.SelectOption(label=i, value=i-1) for i in range(1, len(anime_titles)+1)]
    select = discord.ui.Select(placeholder="", options=options)

    async def my_callback(interaction: discord.Interaction):
        selectedAnime = anime_titles[int(select.values[0])]
        current_series = jsonOP.loadJSON()["series"]

        for i, anime in enumerate(current_series):
            if anime[0] == selectedAnime:
                current_series.pop(i)
                jsonOP.saveJSON({"series": current_series})
                print_bot(f"Removed '{selectedAnime}' from the list")
                await channel.send(f"Removed {selectedAnime} from the list")
                return

        print_bot(f"{selectedAnime} is not in the list")
        await interaction.followup.send(f"{selectedAnime} is not in the list")

    select.callback = my_callback
    view = discord.ui.View()
    view.add_item(select)

    await interaction.response.send_message("Which Anime to Remove?", view=view, embed=animeSelectionRemoveEmbed(anime_titles), delete_after = 15)


@bot.tree.command(name="list_anime", description="Shows the current tracked anime list")
async def self(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
    except:
        print_bot("Defer failed")
        await interaction.followup.send("Error, please try again.")
        return

    try:
        print_bot(f"Listing Anime")
        current_series = jsonOP.loadJSON()["series"]
        if len(current_series) == 0:
            print_bot("No anime found in list")
            await interaction.followup.send("You are not tracking any anime.")
            return
    except Exception as e:
        print(e)
        await interaction.followup.send("Error occured, please try again.")
        return

    await interaction.followup.send(embed=animeListEmbedCard(current_series))


@tasks.loop(count=1)
async def scrapeAiringAnime():
    """
    Scrapes the GogoPlay website for airing anime
    """
    error = None
    while True:
        try:
            res = r.get(DOMAIN, headers=choice(HEADERS))
            soup = BeautifulSoup(res.text, "html.parser")
            episodes = soup.findAll("p", {"class": "name"})
        except Exception as e:
            if error == e:
                print("Same error, shutting down")
                exit()
            error = e
            print(e)
            await asyncio.sleep(randint(150, 300))
            continue
            # os.system("kill 1")

        for i, episode in enumerate(episodes):
            print(jsonOP.data)
            registeredAnime = jsonOP.loadJSON()["series"]
            episode_text = episode.find("a").get("href")
            print(episode_text)
            for index, [anime, episode_number_db, anime_id] in enumerate(registeredAnime):
                if anime.lower() in episode_text:
                    episode_number = episode_text.split("episode ")[-1]
                    if str(episode_number_db) != str(episode_number):
                        registeredAnime[index][1] = int(episode_number) if isInteger(
                            episode_number) else float(episode_number)

                        link = episodes[i].parent.get("href")
                        video_link = scrapeVideo(DOMAIN + link)

                        airing = isAnimeAiring(anime_id)

                        print_bot(
                            f"Anime '{anime}' has aired a new episode: {episode_number}")
                        await notify(anime, anime_id, episode_number, video_link, airing)

                        if not airing:
                            registeredAnime.pop(index)
                            jsonOP.saveJSON({"series": registeredAnime})
                            print_bot(
                                f"Anime '{anime}' is no longer airing at episode {episode_number_db}")
                        else:
                            jsonOP.saveJSON({"series": registeredAnime})

                        break

        # airing anime check incase the program didn't run for a while and passed over the final episode
        for index, [anime, _, anime_id] in enumerate(registeredAnime):
            airing = isAnimeAiring(anime_id, api="jikan")
            # rate limit of 3 requests per second
            await asyncio.sleep(0.34)
            if not airing:
                registeredAnime.pop(index)
                jsonOP.saveJSON({"series": registeredAnime})
                try:
                    episode_number = mal_api.getAnimeByID(anime_id)["num_episodes"]
                except Exception as e:
                    print_bot(e)
                    episode_number = "unknown"
                print_bot(
                    f"Anime '{anime}' is no longer airing at episode '{episode_number}'")

        await asyncio.sleep(randint(300, 600))


def scrapeVideo(link):
    """
    Scrapes the video link from the GogoPlay website
    """
    res = r.get(link, headers=choice(HEADERS))
    soup = BeautifulSoup(res.text, "html.parser")
    # get the attribute called "src" from the iframe tag
    video_link = soup.find("iframe").get("src")
    return "https://" + video_link.lstrip("/")


async def notify(anime_name, anime_id, episode_number, video_link, airing=True):
    """
    Notifies on Discord when an anime has aired a new episode
    """
    message = DISCORD_TAG + f" {anime_name} Episode {episode_number}"
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(message, embed=episodeEmbedCard(anime_id, episode_number, video_link, airing))



bot.run(TOKEN)

