import os
import asyncio
from dotenv import load_dotenv
import discord
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


target_meassage_id = 1085077296555249684


@bot.event
async def on_command_error(message, error):
  if isinstance(error, commands.CommandNotFound):
    await message.channel.send('コマンド存在しません')
  elif isinstance(error, commands.CheckFailure):
    await message.channel.send("権限がありません")
  elif isinstance(error,commands.MissingRequiredArgument):
    await message.channel.send('必須の引数がありません')
  else:
    await message.channel.send(f'Error: {error}')
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

  curseWord = ['fk', 'fuck', 'tf', 'mom']

  # delete curse word if match with the list
  if any(word in msg_content for word in curseWord):
    await message.delete()
    writer = str(message.author).split("#")[0]
    await message.channel.send(f'{writer} だめですよ')
    return

  role = discord.utils.find(lambda r: r.name == 'cock sucker',
                            message.guild.roles)
  if role in message.author.roles:
    await message.add_reaction('\U0001F90F')

  if '!!' not in message.content:
    await bot.process_commands(message)

@bot.command(aliases=["oppai"])
async def おっぱい(message):
  embed = discord.Embed(
    color=discord.Colour.red())
  embed.set_image(url='https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/aa5ac6d0-9bc7-40fd-ba34-b9c36388bbd0/d8echfc-f06f9444-90d8-48b5-8c22-9fc2dae773fc.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2FhNWFjNmQwLTliYzctNDBmZC1iYTM0LWI5YzM2Mzg4YmJkMFwvZDhlY2hmYy1mMDZmOTQ0NC05MGQ4LTQ4YjUtOGMyMi05ZmMyZGFlNzczZmMucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.Ug_91_nIwEJuv0VZhZkU8eJudFS5Daj3ajnyHKqXhmw')
  await message.channel.send(embed=embed)

@bot.command()
async def 断る(message):
  embed = discord.Embed(
    color=discord.Colour.blue())
  embed.set_image(url='https://pbs.twimg.com/media/CuLSuuDVMAAWB6p.jpg')
  await message.channel.send(embed=embed)

@bot.command()
async def pray(message):
  embed = discord.Embed(
    color=discord.Colour.teal())
  embed.set_image(url='https://media.tenor.com/YdDEOK6wfvUAAAAC/mushoku-tensei-roxy-migurdia.gif')
  await message.channel.send(embed=embed)

@bot.command()
async def help(message):
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
  embed.add_field(name='!help', value='List all of the command', inline=False)
  embed.add_field(name='!info',
                  value='infomation about this server',
                  inline=False)
  embed.add_field(name=' ', value=' ---------------------------------------',inline=False)
  embed.add_field(name='!おっぱい/oppai', value='晉見おっぱい教主', inline=False)
  embed.add_field(name='!断る', value='だが断る！', inline=False)
  embed.add_field(name='!pray', value='useless command', inline=False)
  embed.add_field(name=' ', value=' --------------------------------------',inline=False)
  embed.add_field(name='!lol', value='mentions league players', inline=False)
  embed.add_field(name='!build (champion) (position)', value= 'get (champion) build from OP.GG', inline=False)
  embed.add_field(name='!probuild (champion) (position)', value= 'get (champion) build from probuild', inline=False)
  embed.add_field(name='!check (summoner name)', value= 'get sumoner\'s history from OP.GG', inline=False)
  embed.add_field(name=' ', value=' ---------------------------------------',inline=False)
  embed.add_field(name='!anime (anime name)', value= 'get anime\'s release date', inline=False)
  embed.add_field(name='!hangman', value='start Hangman',inline=False)
  embed.add_field(name='!guess (word or character)', value='guess a word or character in Hangman',inline=False)
  embed.add_field(name='!quit (game)', value='quit that game',inline=False)
  embed.add_field(name='!bj', value='play blackjack\nuse "H"it or "S"tand',inline=False)
  embed.add_field(name='!credit', value='see everyone\'s credits', inline=False)
  embed.add_field(name=' ', value=' ---------------------------------------',inline=False)
  embed.add_field(name='!delete (message id)', value= 'delete one message by id', inline=False)
  embed.add_field(name='!clear (number)', value= 'delete (number) of message(s)', inline=False)

  await message.send(embed=embed)


@bot.command()
async def info(message):
  """
    This command sends info
    """
  await message.send('おはよう ' + message.author.name)
  await message.send('這是一個被<@465746027941724161>拋棄的伺服器')

#------------------------------------------------------------------------------------------------------------

@bot.command()
async def lol(message):
  """
    This command mentions league players
    """
  player = [465746027941724161,586052628807417878,748079858587795456,191052169569370113,191052169569370113,330695143273267201]
  if message.author.id in player:
    player.remove(message.author.id)
  player = ['<@'+str(x)+'>' for x in player]
  await message.send(
    'who wants to be carried '+" ".join(player)
  )


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

@bot.command()
async def check(message, name):
  loading = discord.File('Discord_bot/ayame_image/loading.gif', filename='loading.gif') 
  await message.channel.send(file=loading)
  screenshot.screenshot_name(name)
  file = discord.File('screenshot.png', filename='champion.png')
  await message.invoke(bot.get_command('clear'), limit = 0)
  await message.channel.send(file=file)
  
@bot.command()
async def build(message, champion, role):
  loading = discord.File('Discord_bot/ayame_image/loading.gif', filename='loading.gif') 
  await message.channel.send(file=loading)
  if role=='jg':
    role = 'jungle'
  elif (role=='bot') | (role=='ad'):
    role = 'adc'
  elif role == 'sup':
    role = 'support'
    
  roles = ['top', 'jungle', 'mid', 'adc', 'support']
  if role not in roles:
    await message.channel.send('wrong position')
    return
  screenshot.screenshot(champion, role)
  file = discord.File('screenshot.png', filename='champion.png')
  await message.invoke(bot.get_command('clear'), limit = 0)
  await message.channel.send(file=file)

@bot.command()
async def probuild(message, champion, role):
  loading = discord.File('Discord_bot/ayame_image/loading.gif', filename='loading.gif') 
  await message.channel.send(file=loading)
  ben = discord.utils.find(lambda r: r.name == 'tits licker',
                            message.guild.roles)
  if ben in message.author.roles:
    lpl = True
  else:
    lpl = False

  if role=='jg':
    role = 'jungle'
  elif role=='bot':
    role = 'adc'
  elif (role=='sup') or (role == 'support'):
    role = 'supp'
  elif role =='ad':
    role =='adc'
  
  roles = ['top', 'jungle', 'mid', 'adc', 'supp']
  if role not in roles:
    await message.channel.send('wrong position')
    return
  screenshot.screenshot_pro(champion, role, lpl)
  file = discord.File('screenshot.png', filename='champion.png')
  await message.invoke(bot.get_command('clear'), limit = 0)
  await message.channel.send(file=file)

@bot.command()
async def anime(message, *name):
  loading = discord.File('ayame_image//loading.gif', filename='loading.gif') 
  await message.channel.send(file=loading)
  screenshot.screenshot_anime(name)
  file = discord.File('screenshot.png', filename=f'{name}.png')
  await message.invoke(bot.get_command('clear'), limit = 0)
  await message.channel.send(file=file)  

#----------------------HangMan-----------------------------------------------------------------------

@bot.command()
async def hangman(message):
  if message.channel.id in HangmanGame.games:
    await message.channel.send("There's already a game in progress in this channel!")
  else:
    HangmanGame.games[message.channel.id] = HangmanGame.HangmanGame(message.channel)
    await HangmanGame.games[message.channel.id].start_game()

@bot.command()
async def guess(message, guess):
  data = pd.read_csv('credit.csv')
  data = data.set_index('ID')
  if message.channel.id not in HangmanGame.games:
    await message.channel.send('START FIRST')
    return
  if (len(guess)>len(HangmanGame.games[message.channel.id].word)):
    await message.channel.send('Didn\'t ur parents teach u how to play hangman?')
    return
  if not guess.isalpha():
    await message.channel.send('Didn\'t ur parents teach u how to play hangman?')
    return
  if len(guess)==1:
    if not guess.isalpha():
      await message.channel.send('Didn\'t ur parents teach u how to play hangman?')
      return
  guess = guess.lower()
  if guess == HangmanGame.games[message.channel.id].word:
      data.loc[message.author.id].values[0] += 20
      data.to_csv('credit.csv')
      await HangmanGame.games[message.channel.id].channel.send('Congratulations! You won!')
      await HangmanGame.games[message.channel.id].channel.send(f'**{message.author.name}** wins 20 credits')
      end = discord.File('ayame_image/ayame(hangman_end).jpg', filename='loading.gif')
      await message.channel.send(file = end)
      HangmanGame.games[message.channel.id].end_game(message.channel.id)
  elif guess in HangmanGame.games[message.channel.id].guesses:
      await HangmanGame.games[message.channel.id].channel.send('You already guessed that letter.')
  elif guess in HangmanGame.games[message.channel.id].word:
      HangmanGame.games[message.channel.id].guesses.append(guess)
      await message.channel.send(HangmanGame.games[message.channel.id].get_board())
      if '_' not in HangmanGame.games[message.channel.id].get_board():
          data.loc[message.author.id].values[0] += 20
          data.to_csv('credit.csv')
          await HangmanGame.games[message.channel.id].channel.send('Congratulations!')
          await HangmanGame.games[message.channel.id].channel.send(f'**{message.author.name}** wins 20 credits')
          end = discord.File('ayame_image/ayame(hangman_end).jpg', filename='loading.gif')
          await message.channel.send(file = end)
  else:
    HangmanGame.games[message.channel.id].guesses.append(guess)
    HangmanGame.games[message.channel.id].max_guesses-=1
    if HangmanGame.games[message.channel.id].max_guesses == 0:
      await message.channel.send(f'You are bad\n The answer is {HangmanGame.games[message.channel.id].word}')
      HangmanGame.games[message.channel.id].end_game(message.channel.id)
      return
    await message.channel.send(HangmanGame.games[message.channel.id].get_board())
  
@bot.command()
@commands.has_role('我在搞')
async def quit(message, game):
  if (game == 'hangman'): 
    await message.channel.send(f'The answer is {HangmanGame.games[message.channel.id].word}')
    HangmanGame.games[message.channel.id].end_game(message.channel.id)
  if (game == 'bj'):
    del BlackjackGame.games[message.channel.id]

#----------------------BlackJack-----------------------------------------------------------------------

@bot.command()
async def bj(message):
  data = pd.read_csv('credit.csv')
  data = data.set_index('ID')
  target = 0
  if message.channel.id in BlackjackGame.games:
    await message.channel.send("There's already a game in progress in this channel!")
  else:
    await message.channel.send('Place you bets if u want to play BlackJack')
    async for msg in message.channel.history(limit=1):
      target = msg.id
      await msg.add_reaction('5️⃣')
      await msg.add_reaction('🔟')
    await asyncio.sleep(5)
    msg = await message.channel.fetch_message(target)
    await msg.remove_reaction('5️⃣', bot.user)
    await msg.remove_reaction('🔟', bot.user)
    five = [user async for user in msg.reactions[0].users()]
    ten = [user async for user in msg.reactions[1].users()]
    for player in five:
        if data.loc[player.id].values[0] < 5:
          await message.channel.send(f'{player.name} don\'t have enongh credits!')
          five.remove(player)
    for player in ten:
        if data.loc[player.id].values[0] < 10:
          await message.channel.send(f'{player.name} don\'t have enongh credits!')
          ten.remove(player)
    users = five + ten
    BlackjackGame.games[message.channel.id] = BlackjackGame.Blackjack(message.channel, five, ten)
    users = [user.name for user in users]
    if len(users) == 0:
      await message.channel.send('おまえらはみんな小心者だ')
    else:
      await message.channel.send(f'{users} playing blackjack')
    while len(BlackjackGame.games[message.channel.id].hands)>0:
      users = []
      await message.channel.send(BlackjackGame.games[message.channel.id].get_game_state())
      async for msg in message.channel.history(limit=1):
        target = msg.id
        await msg.add_reaction('🇭')
        await msg.add_reaction('🇸')
      await asyncio.sleep(5)
      msg = await message.channel.fetch_message(target)
      users = [user async for user in msg.reactions[0].users()]
      if len(users)>1:
        for user in users:
          if user == bot.user:
            continue
          await BlackjackGame.games[message.channel.id].hit(user)
      else:
        break
    result, no_one_win = await BlackjackGame.games[message.channel.id].end(bot.user)
    if not no_one_win:
      await message.channel.send(BlackjackGame.games[message.channel.id].get_game_state())
      end = discord.File('ayame_image/ayame_ya.jpg', filename='ya.jpg')
      await message.channel.send(file = end)
    else:
      end = discord.File('ayame_image/ayame_victory.jpg', filename='loser.jpg')
      await message.channel.send(file = end)
    await message.channel.send(result)
    del BlackjackGame.games[message.channel.id]

@bot.command()
async def credit(message):
  data = pd.read_csv('credit.csv')
  data = data.set_index('ID')
  data = data.sort_values(by = ['credit'], ascending=False)
  result = "```\n"
  for i in data.index:
      result += "{}: {}\n".format(bot.get_user(i).name,data.loc[i].values[0])
  result += "```"
  await message.channel.send(result)

@bot.command()
async def test(message, *,arg):
  await message.send(arg)
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

