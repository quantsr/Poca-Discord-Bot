import discord
import os
import random
import requests
import json
import sqlite3
from discord.ext import commands
#for bot hosting in replit
from keep_alive import keep_alive

from music_cog import music_cog

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(intents=intents, command_prefix = '!')
bot.add_cog(music_cog(bot))

def write_json(new_data, filename='data.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        #file_data['players'].append(new_data)
        file_data['players'].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

def edit_json(new_data, position,filename='data.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        #file_data['players'].append(new_data)
        file_data['players'][position] = (new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

message_second = [", with fury in their eyes.", ", scanning the room with suspicious eyes.", ", while walking slowly through the saloon.", ", lying through their teeth.", ", avoiding everyone's gazes.", ", in an awkward fashion.", ", turning red on their face.", " rhetorically.", ", seeking attention.", ", while trying to make themselves small.", ", the youngest Henderson boy.", ", with a distant look in their eyes.", ", sarcastically staring at the screen.", ", frustrated with that statement.", ", jealous of the previous message.", ", irritated at everyone.", ", skeptical at best.", ", bewildered with the possibilities.", ", discouraged to say anything more.", ", rejecting what they previously wanted to say.", ", embarassingly looking at the ground.", ", fascinated by cheese.", ", amusing themselves with the last word.", ", flirting playfully.", ", confident in finally revealing such information.", ", with tired eyes.", ", trying to not breath the air." , " unapologetically.", ", based on their own experience.", ", while loading their guns for more.", ", preparing to do a backflip.", ".", ", when the gloop went bloop.", ", ready to kick the bot out of the server.", ", raising their hands in a threathening manner.", ", regreting the creation of this bot.", ", going back to being afk.",
 ", choosing to ignore all the following questions."]

is_muted = False

@bot.event
async def on_ready():
  #db=sqlite3.connect("main.sqlite")
  #cursor = db.cursor()
  #cursor.execute("CREATE TABLE playlists(discord_id integer, discord_name text, song_url text)")
  print("Bot is combat ready!")

  

##############start of bot commands##############


@bot.event
async def on_message(message):
  message_str = (message.content).lower()
  """
    The bot used to have a command to count words spoken by a specific user. Due to being too obnoxious, its function was retired. 
  """


  #if " lol " in (" " + message_str + " "):
    # and len(message.content) == 3:    #message containsthe  word lol
    #if message.author != bot.user:                           #message wasn't sent by bot
      #if message.author.id == 161323552761577472:               #message was sent by user
        #db["lolcounter"] = db["lolcounter"] + 1
        #await message.channel.send(f'LORDO COUNTER: {db["lolcounter"]}') 
        #await message.channel.send('https://tenor.com/view/thats-it-yes-thats-it-that-right-there-omg-that-thats-what-i-mean-gif-17579879')

  #if "lmao" in (" " + message_str + " "):   #message contains the word lmao
    #if message.author != bot.user:                           #message wasn't sent by bot
      #if message.author.id == 161323552761577472:               #message was sent by user
        #db["lolcounter"] = db["lolcounter"] + 1
        #await message.channel.send(f'LORDO COUNTER: {db["lolcounter"]}') 
        #await message.channel.send('https://tenor.com/view/thats-it-yes-thats-it-that-right-there-omg-that-thats-what-i-mean-gif-17579879')

  if " heck " in (" " + message_str + " ") or " hecking " in (" " + message_str + " ") or " fudge " in (" " + message_str + " "):
    if message.author != bot.user:
      await message.channel.send("Watch your language! Only real swears are permitted!")
  
  if " deez nuts ".lower() in (" " + message_str + " ") or " these nuts ".lower() in (" " + message_str + " "):
   if message.author != bot.user:
      await message.channel.send("https://media0.giphy.com/media/dWfkLpnrZN3QQ/giphy.gif?cid=ecf05e47ybrj2xnxht67yadqqpjql1u11ucnz2a46w1cfkkb&rid=giphy.gif&ct=g")


  if message.author != bot.user and not is_muted:
    chance = random.randint(1,200)
    
    if chance <= 3:
      message_name = message.author.display_name
      await message.channel.send(f"*{message_name}{random.choice(message_second)}*", tts = True, delete_after = 0)
      await message.channel.send(f"*Said {message_name}{random.choice(message_second)}*")
  
  await bot.process_commands(message)

#mention a random member(Bot including) in the server.
@bot.command()
async def ping(ctx):
  target = random.choice(ctx.guild.members)
  await ctx.send(target.mention)

@bot.command()
async def marco(ctx):
  await ctx.send("Polo.", tts = True)

@bot.command()
async def mute(ctx):
  global is_muted
  if is_muted == False:
    is_muted = True
    await ctx.send("*I'll stay quiet for now until you need me*")
  else:
    is_muted = False
    await ctx.send("*Hello again*")

@bot.command(aliases = ["Read"])
async def read(ctx):
  resp = requests.get("https://api.kanye.rest/")
  data = resp.json()
  twitt = data["quote"]
  await ctx.send(twitt)
  await ctx.send("https://upload.wikimedia.org/wikipedia/commons/1/10/Kanye_West_at_the_2009_Tribeca_Film_Festival_%28cropped%29.jpg")
  
@bot.command()
async def fuckoff(ctx, target:discord.Member = None):
  resp = requests.get("https://www.foaas.com/operations")
  data = resp.json()

  #handling url exceptions
  from_str = (ctx.message.author.display_name)
  from_str = from_str.replace(" ", "%20")
  if target is None:
    name_str = "buddy"
  else:
    name_str = target.display_name
  name_str = name_str.replace(" ", "%20")
  company_str = "this%20server"
  reference_str = "God"

  #filtering available /operations from foaas API
  forbidden_list = [":tool", ":do", ":something", ":noun", ":reaction", ":behaviour", ":thing", ":language", "/version"]

  redo = True
  while redo:
      url_append = data[random.randint(1,99)]["url"]
      redo = False
      for forbidden_word in forbidden_list:
          if forbidden_word in url_append:
              redo = True 
  
  #constructing url_append
  url_append = url_append.replace(":from", from_str)
  url_append = url_append.replace(":name", name_str)
  url_append = url_append.replace(":company", company_str)  
  url_append = url_append.replace(":reference", reference_str)
  my_url = "https://www.foaas.com" + url_append
  
  #check if screenshot api is has remaining slots
  quota_resp = requests.get("https://api.apiflash.com/v1/urltoimage/quota?access_key=925167706eea4598a302b9db41a86420")
  quota = quota_resp.json()
  if quota["remaining"] > 0:
    my_screenshot = f"https://api.apiflash.com/v1/urltoimage?access_key=925167706eea4598a302b9db41a86420&height=900&url={my_url}"
    #sending message
    await ctx.send(my_screenshot)
    await ctx.send(f'we have {quota["remaining"]} screenshots left')
  else:
    await ctx.send(my_url)
    
  

@bot.command()
async def duel(ctx, target:discord.Member):
  author_name = ctx.message.author.name
  target_name = target.name
  #sending message to the author
  await ctx.message.author.send(f'sup {author_name}. {target.name} received(hopefully) your challenge. Make your choice here:\nR -> Rock\nP -> Paper\nS -> Scissors')
  #sending message to the target
  await target.send(f'sup homie, {author_name} challenged you to a rock-paper-scissors match. Make your choice here:\nR -> Rock\nP -> Paper\nS -> Scissors')
  # 
  #
  #STILL HAVE TO CHECK MESSAGE EXCEPTION
  def check_message_exception(message):
    approved = True
    return approved

  def check_1(m):
    return m.author == ctx.message.author # checks if the person who sent it is the message's author

  msg1 = await bot.wait_for('message', check = check_1)

  def check_2(m):
    return m.author == target # checks if the person who send it is the target

  msg2 = await bot.wait_for('message', check = check_2)

  print(f'{author_name} chose {msg1.content}')
  print(f'{target_name} chose {msg2.content}')

  jankenpo = {'R' : 'Rock', 'P': 'Paper', 'S': 'Scissors'}

  await ctx.send(f'{author_name} chose {jankenpo[msg1.content]}\n{target_name} chose {jankenpo[msg2.content]}')

@bot.command()
async def jstris(ctx, *, arg):
  username = arg
  url = f"https://jstris.jezevec10.com/api/u/{username}/records/1?mode=1rule="
  payload = {}
  headers= {}
  response = requests.request("GET", url, headers=headers, data = payload)

  #print(response.text.encode('utf8'))
  response = json.loads(response.text.encode('utf8'))
  print(response["name"])
  #await ctx.send(response["name"])

  await ctx.send(f"40 LINES SPRINT\nName: {response['name']}\nMin: {response['min']}\nMax: {response['max']}\nAvg: {response['avg']}\nSum: {response['sum']}\nGames: {response['games']}\nDays: {response['days']}")

#will remove this one later
@bot.command()
async def cock(ctx, target:discord.Member = None):
  sfw = 'off'
  if target is None:
    targets = random.sample(ctx.guild.members, 10)
    #filtering "427661488392503296" user under personal request
    id_presence = True
    while id_presence == True:
      id_presence = False
      for i in range(10):
        if str(targets[i].id) == "427661488392503296":
          id_presence = True
          targets[i] = random.choice(ctx.guild.members)
          break
    end_of_string = f"{targets[0].mention} {targets[1].mention} {targets[2].mention} {targets[3].mention} {targets[4].mention} {targets[5].mention} {targets[6].mention} {targets[7].mention} {targets[8].mention} {targets[9].mention}"
  else:
    if str(target.id) == "427661488392503296":
      sfw = 'on'
    end_of_string = f"{target.mention}"
  ascart = "/    イ              (((ヽ\n(    ノ                 ￣Y  \\\n|   ( \      (.       /)     |     )\nヽ   ヽ `  ( ͡° ͜ʖ ͡°)  _ノ    /\n     ＼\   |   ⌒Ｙ⌒   /  /\n         | ヽ     |      ﾉ ／\n         ＼トー仝ーイ\n              | ミ土彡/\n            ) \\      °   /\n           (     \\      /     )\n          /       / ѼΞΞΞΞΞΞΞD\n       /  /     /      \\ \\   \\ \n       ( (    ).           ) ).  )\n      (      ).            ( |    | \n       |    /                \    |"
  if sfw == 'off':
    await ctx.send(f"SURPRISE! You have been slapped by a BIG COCK in the middle of your face! * CLASS * This is The Ultimate Dick War of All Times 2021! There is ONE rule. You can not cock someone who has already cocked you !! Try to cock as many as possible before they cock you. I've slapped you in the face already, so you can not cock me. Good luck!\n{ascart}\nPass the Christmas Cockmonster to 10 of your tightest bros to give them big cock and massive gains this 2022 and thank them for everything they've done {end_of_string}")
  else:
    await ctx.send(f"Sorry, I don't want to hurt {target.nick if target.nick is not None else target.name}'s feelings. Can I please not do that ;-;")
  

@bot.command()
async def protec(ctx):
  file = open('database.txt', 'r')
  i = int(file.read())
    
  images = ["https://i.redd.it/hu7mjjlx3gr61.jpg", "https://pbs.twimg.com/media/Esq7v8nW8AAxOwP.jpg", "https://pbs.twimg.com/media/EtJRXYOUYAAfnm0.jpg", "https://preview.redd.it/iuxvmplvqfi61.jpg?auto=webp&s=407ddafc9b42c84c243981ca9ff7233b07d36344", "https://cdn.donmai.us/sample/fe/d8/sample-fed83e166fd299f69e8bff4273c9faac.jpg", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTPxwOy908hXavnEnqfJq4VLKDBj9S-M3tHTA&usqp=CAU", "https://pbs.twimg.com/media/EvcFVULXAAIW_Vp.jpg", "https://i.ytimg.com/vi/vk2mDtaykso/mqdefault.jpg"]
  await ctx.send(images[i])
  i = i + 1
  if i == len(images):
    i = 0
  file = open('database.txt', 'w')
  file.write(str(i))
  file.close()


 
##############end of bot commands##############

keep_alive()
print(bot.run(os.environ['TOKEN']))

