import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from screenshot import screenshot

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
    await message.channel.send('コマンド がありません')
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
    await message.delete()
    return

  curseWord = ['fk', 'fuck', 'tf']

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

  if message.channel.name == '一般':
    await bot.process_commands(message)


@bot.command()
async def help(message):
  embed = discord.Embed(
    title='百鬼あやめです',
    description=
    'Please subscribe あやめ on YouTube\n https://www.youtube.com/@NakiriAyame',
    color=discord.Colour.red())
  embed.set_image(url='https://i.imgur.com/V2csjKc.png')
  embed.set_thumbnail(
    url=
    'https://static.wikia.nocookie.net/virtualyoutuber/images/0/09/Nakiri_Ayame_Portrait.png/revision/latest?cb=20190215184953'
  )
  embed.add_field(name='!help', value='List all of the command', inline=False)
  embed.add_field(name='!info',
                  value='infomation about this server',
                  inline=False)
  embed.add_field(name='!punch', value='Punch another player', inline=True)
  embed.add_field(name='!roundhouse_kick',
                  value='kick some players',
                  inline=True)
  embed.add_field(name='!lol', value='mentions league players', inline=False)
  await message.send(embed=embed)


@bot.command()
async def info(message):
  """
    This command sends info
    """
  await message.send(message.author)
  await message.send('這是一個被<@465746027941724161>拋棄的伺服器')


@bot.command()
async def punch(message, arg):
  """
    This command punches another player
    """
  await message.send(f'Punched👊 {arg}')


@bot.command()
async def lol(message):
  """
    This command mentions league players
    """
  await message.send(
    'who wants to be carried <@465746027941724161> <@586052628807417878> <@748079858587795456> <@191052169569370113> <@808356393216114688>'
  )


@bot.command()
async def roundhouse_kick(message, *args):
  if len(args) == 0:
    await message.channel.send('who do u want to kick?')
    return
  everyone = ', '.join(args)
  await message.send(f'{message.author} roundhouse kicked {everyone}')


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

@bot.command()
async def build(message, champion, role):
  screenshot(champion, role)
  file = discord.File('\\home\\ubuntu\\Discord_bot\\screenshot.png', filename='champion.png') 
  await message.channel.send(file=file)


@bot.command()
async def test(message, arg):
  await message.send(arg)


bot.run(TOKEN)

