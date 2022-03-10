import discord
import random
import sqlite3
from discord.ext import commands
from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

    self.is_playing = False

    

    self.music_queue = []
    self.YDL_OPTIONS = {'format':'bestaudio', 'noplaylist': 'True'}
    self.FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options':'-vn'}

    self.vc = ""

    self.now_playing = ""

  def search_yt(self,item):
    with YoutubeDL(self.YDL_OPTIONS) as ydl:
      try:
        info = ydl.extract_info("ytsearch:%s" % item, download = False)['entries'][0]
      except Exception:
        return False
    
    return {'source': info['formats'][0]['url'], 'title': info['title']}
  
  def play_next(self):
    
    if len(self.music_queue) > 0:
      self.is_playing = True

      #get the first Url
      m_url = self.music_queue[0][0]['source']

      #remove the first element as you are currently playing it
      #self.music_queue.pop(0)
      self.now_playing = self.music_queue.pop(0)
      
      #tryin this to change volume:
      #self.vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(m_url)), after = lambda e: self.play_next())
      self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
    else:
        self.is_playing = False


  
  async def play_music(self):
    if len(self.music_queue) > 0:
      self.is_playing = True
      m_url = self.music_queue[0][0]['source']

      #try to connect to voice channel if you are not already Connected
      #if self.vc == "" or not self.vc.is_connected():
      if self.vc == "" or not self.vc.is_connected() or self.vc == None:
        self.vc = await self.music_queue[0][1].channel.connect()
        #print(self.vc)
      #else:
        #self.vc = await self.bot.move_to(self.music_queue[0][1])
        
      
      #print(self.music_queue)
      #remove the first element as you are currently playing it
      self.now_playing = self.music_queue.pop(0)
  
      #tryin this to change volume:
      #self.vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(m_url)), after = lambda e: self.play_next())
      self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
    else:
      self.is_playing = False

  @commands.group(invoke_without_command = True)
  async def playlist(self, ctx):
    await ctx.send("*Use '!playlist save' followed by the song name or url to add a song to your own playlist. '!playlist load' to listen to your playlist.*")
    
    
  @playlist.command()
  async def save(self, ctx, *args):
    song_url = " ".join(args)
    if song_url == "":
      return await ctx.send("*Please, don't forget to add the song name or url link for me.*")
    
    author = str(ctx.author.display_name)
    table_name = str(ctx.author.id)
    
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"CREATE TABLE if not exists '{table_name}' (song_id integer primary key autoincrement, song_url text)")
    cursor.execute(f"INSERT INTO '{table_name}' (song_url) VALUES('{song_url}')")
    
    db.commit()
    await ctx.send(f"*I've successfuly added '{song_url}' to {author}'s playlist. I hope you enjoy.*")

  @playlist.command()
  async def load(self, ctx, target:discord.Member = None):
    if ctx.author.voice is None:
      #you need to be connected to a voice channel so that the bot knows where to go
      return await ctx.send("Please, could you connect to a voice channel?")
    if target is None:
      table_owner = str(ctx.author.display_name)
      table_name = str(ctx.author.id)
    else:
      table_owner = str(target.display_name)
      table_name = str(target.id)

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    
    for row in cursor.execute(f"SELECT song_url FROM '{table_name}'"):
      #('song name',) needs splicing for formatting reasons
      song = str(row)
      await ctx.invoke(self.bot.get_command('play'), args= song)
    
    await ctx.send(f"*loaded {table_owner}'s playlist :)*")

  @commands.command(aliases = ["p"])
  #async def play(self, ctx, *args):
  async def play(self, ctx, *, args): #despacito version. original above 
    #query = " ".join(args)
    query = args #despacito version. original above
    print(f"query is {query}")
        
    #voice_channel = ctx.author.voice.channel
    voice_channel = ctx.author.voice
    

    if voice_channel is None:
      #you need to be connected so that the bot knows where to go
      await ctx.send("Please, could you connect to a voice channel?")
    else:
      song = self.search_yt(query)
      if type(song) == type(True):
        await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
      else:
        
        self.music_queue.append([song, voice_channel])
        await ctx.send(f"[{self.music_queue[-1][0]['title']}] added to the queue!")      
        if self.is_playing == False:
          await self.play_music()
  
  @commands.command(aliases = ["q"])
  async def queue(self, ctx):
    retval = ""
    for i in range(0, len(self.music_queue)):
      retval += f"{i+1} - " + self.music_queue[i][0]['title'] + "\n"

    print(retval)
    if retval != "":
      await ctx.send(retval)
    else:
      await ctx.send("No music in queue")

  @commands.command()
  async def shuffle(self, ctx):
    random.shuffle(self.music_queue)
    await ctx.send("...Can I really? Thanks!")

  @commands.command()
  async def skip(self, ctx):
    if self.vc != "" and self.vc:
      self.vc.stop()
      #try to play next in the queue if it exists
      await self.play_music()

  @commands.command(aliases = ["disconnect", "leave"])
  async def dc(self, ctx):
    #await self.vc.disconnect()
    if ctx.message.author.id == 161323552761577472:
      await ctx.send("I'm sorry. But I don't like you.")
      return
    else:
      await ctx.voice_client.disconnect()
      await ctx.send("Good bye...")

  @commands.command(aliases = ["now playing"])
  async def np(self, ctx):
    if self.is_playing == True: 
      await ctx.send(f"{self.now_playing[0]['title']}")
    else:
      self.now_playing = ""
      await ctx.send("I'm not playing anything at the moment. But I can if you want me to?")

  @commands.command()
  async def pause(self, ctx):
    ctx.voice_client.pause()
    await ctx.send("Paused </3")

  @commands.command()
  async def resume(self, ctx):
    ctx.voice_client.resume()
    await ctx.send("*Resumed <3*")

  '''
  Play_despacito will be used to load playlists.
  When I finish making a playlist database with the song link values, I'll just replace (args= "despacito") with the song link value in database.
  '''
  @commands.command()
  async def play_despacito(self, ctx):
    await ctx.invoke(self.bot.get_command('play'), args= "despacito")
    await ctx.send("*Whyyy.... ;_;*")

#async def play(self, ctx, *, args):
#async def play(self, ctx, *args):
#await ctx.invoke(self.bot.get_command('play'), query='hi'
# await bot.get_command('exampleArgsCommand').callback(ctx, message)
'''#deprecated
  @commands.command(aliases = ["vol", "v"])
  async def volume(self, ctx, volume: int):
    if ctx.voice_client is None:
      return await ctx.send("I'm not connected to voice channel. I'm sorry...")
    
    print(volume/100)
    #ctx.voice_client.source = discord.PCMVolumeTransformer(ctx.voice_client.source)
    ctx.voice_client.source.volume = volume / 100
    print(ctx.voice_client.source.volume)
    await ctx.send(f"increased volume to {volume}%")
'''


 
    

    