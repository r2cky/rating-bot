import discord
from discord.ext import commands
from keep_alive import keep_alive
from replit import db
import crawl

client = commands.Bot(command_prefix='!', help_command=None)
q = []
ok = 1
playing = 0
lim = 20
st = "查詢囉"
ans_for_wordle=""
#db['wordler_status'] ={}
up = [1, 3,3,5,5,10, 10,20,20,30,50 ,100, "inf"]
class Req:  
    def __init__(self, q, t): 
       self.q = q
       self.t = t
       
      
@client.event
async def queue():
    #codeforce = 0 + name
    #atcoder = 1 + name
    #zerojudge = 2
    #wordle:
    #start = 3
    #guess = 4 + ans
    #mode = 5
    #add new words = 6 + words(split by,)
    #remove words = 7 +words(split by ,)
   global q,ok
   try:
      channel = client.get_channel(966216697176543252)
      global st, playing,guess_count,db
      ok = 0
      game = discord.Game("Please wait...")
      await client.change_presence(status=discord.Status.online,activity=game)
      while (len(q) != 0 and ok == 0):
         #o = q.pop(0)
         #a = o.q
         #b = o.t
         o = q.pop(0)
         a = o.q
         b = o.t
         if a == 0:
            await channel.send(embed=crawl.get_cf(b))
         if a == 1:
            await channel.send(embed=crawl.get_ac(b))
         if a == 2:
            await channel.send(await crawl.get_zj())
         if a == 3:
            if(playing==1) :
              playing=0
              await channel.send(embed=await crawl.return_ans())
              continue;
            else:
              playing=1
              crawl.guess_count=0
              crawl.select_word()
              ans_for_wordle=crawl.ans_for_wordle
              print(crawl.ans_for_wordle)
              await channel.send(embed =discord.Embed(title="wordle",                      description="A new round has started!\nLength of the word: "+str(len(ans_for_wordle))))
            
         if a == 4:
            print(b)
            if(playing == 1) :
               await channel.send(embed = await crawl.check(b[0]))
               if(b[0] == crawl.ans_for_wordle):
                  print("test")
                  await reward_user(b[1])
                  playing = 0
            else:
               await channel.send("You haven't start a round.")
         if a == 5: 
           if playing==0:await channel.send("You haven't start a round.")
           elif crawl.mode == 0:
             crawl.mode=1
             await channel.send(embed =discord.Embed(title="wordle",                       description="You have switched to special mode!"))
             crawl.rs()
           else:
             crawl.mode=0
             await channel.send(embed =discord.Embed(title="wordle",                      description="You have switched to normal mode!"))

         if a == 6:
           await channel.send(embed = await crawl.insert_new(b))
           #print(db["words_list"])

         if a == 7:
           await channel.send(embed = await crawl.remove_word(b))
         if a == 8:
           await channel.send(embed = await crawl.wcheck(b))
      await ret()
      ok = 1
   except:
      print("err")
      q.clear()
      ok = 1
      return 

#declare commands
@client.command()
async def cf_rating(ctx, arg):
    global q, ok
    i = Req(0,arg.strip())
    q.append(i)
    if ok == 1: await queue()


@client.command()
async def ac_rating(ctx, arg):
    global q, ok
    i = Req(1,arg.strip())
    q.append(i)
    if ok == 1: await queue()


@client.command()
async def give_me_zj(ctx):
    global q, ok
    i = Req(2,0)
    q.append(i)
    if ok == 1: await queue()


@client.command()
async def cf_me(ctx):
    global q, ok
    key=""
    try:
       key=db["c" + ctx.message.author.name][0]
    except:
       await ctx.send("You haven't assigned to any account yet." )
       return
    i = Req(0,key)
    q.append(i)
    if ok == 1: await queue()


@client.command()
async def ac_me(ctx):
    global q, ok
    key=""
    try:
       key=db["a" + ctx.message.author.name][0]
    except:
       await ctx.send("You haven't assigned to any account yet." )
       return
    i = Req(1,key)
    q.append(i)
    if ok == 1: await queue()


@client.command()
async def assign_cf_account(ctx, arg):
    try:
      db["c" + ctx.message.author.name] = [arg]
      await ctx.send("You have been assigned to codeforce account: " + arg)
    except:
      print("err")


@client.command()
async def assign_ac_account(ctx, arg):
    try:
      db["a" + ctx.message.author.name] = [arg]
      await ctx.send("You have been assigned to atcoder account: " + arg)
    except:
      print("err")


@client.command()
async def assign_status(ctx, arg):
    try:
      global st
      st = arg
      await ret()
    except:
      print("err")


@client.command()
async def wordle_start(ctx):
    #await ctx.author.roles.add('977099958152994846')
    global q, ok
    i = Req(3,0)
    q.append(i)
    if ok == 1: await queue()

@client.command()
async def wordle_guess(ctx,arg):
    global q, ok
    if(db['wordler_status'].get(ctx.message.author.name) == None):
      db['wordler_status'][ctx.message.author.name] = [0,0,0]
      
    i = Req(4,[arg.strip().lower(),ctx.message.author])
    q.append(i)
    if ok == 1: await queue()

@client.command()
async def wordle_mode_switch(ctx):
    global q, ok
    i = Req(5,0)
    q.append(i)
    if ok == 1: await queue()

@client.command()
async def wordle_insert(ctx,arg):
    global q, ok
    i = Req(6,arg.strip())
    q.append(i)
    if ok == 1: await queue()

@client.command()
async def wordle_remove(ctx,arg):
    global q, ok
    i = Req(7,arg.strip())
    q.append(i)
    if ok == 1: await queue()

@client.command()
async def wordle_rating(ctx):
    global q, ok
    i = Req(8,ctx.message.author.name)
    q.append(i)
    if ok == 1: await queue()
    
@client.event
async def reward_user(user):
    global q, ok, up
    db['wordler_status'][user.name][1]+=1
    db['wordler_status'][user.name][2]+=1
    print(db['wordler_status'][user.name][0])
    print(db['wordler_status'][user.name][1])
    print(db['wordler_status'][user.name][2])
    clv = db['wordler_status'][user.name][0]
    if(clv != 12 and up[clv] <= db['wordler_status'][user.name][1]):
      nlv = clv + 1
      db['wordler_status'][user.name][0] = nlv
      db['wordler_status'][user.name][1] = 0
      role = discord.utils.get(user.guild.roles, name="Lv. "+str(nlv))
      await user.add_roles(role)
      if(nlv != 1):
        role = discord.utils.get(user.guild.roles, name="Lv. "+str(nlv-1))
        await user.remove_roles(role)

@client.command()
async def help(ctx):
    #inlime false
    try:
      text=discord.Embed(title=help, url="https://hw.cheesechi.repl.co/")
      text.add_field(name="!cf_rating + [account]", value="Check a codeforces account's rating.", inline=False)
      text.add_field(name="!assign_cf_account + [account]", value="Assign your discord account to a codeforces account.", inline=False)
      text.add_field(name="!cf_me", value="Check your codeforces statistic(Need to assign first)", inline=False)
      text.add_field(name="!ac_rating + [account]", value="Check an atcoder account's rating.", inline=False)
      text.add_field(name="!assign_ac_account + [account]", value="Assign your discord account to an atcoder account.", inline=False)
      text.add_field(name="!ac_me", value="Check your atcoder's statistic(Need to assign it first)", inline=False)
      text.add_field(name="!assign_status + [status]", value="Change the bot's status.", inline=False)
      text.add_field(name="!wordle_start", value="Start a new round.", inline=False)
      text.add_field(name="!wordle_guess + [word]", value="Guess a word", inline=False)
      text.add_field(name="!wordle_mode_switch", value="Normal mode/special mode", inline=False)
      text.add_field(name="!wordle_insert + [words]", value="Insert some new words to the database. (split the word by , )", inline=False)
      text.add_field(name="!wordle_remove + [words]", value="Remove some words from the database. (split the word by , )",   inline=False)
      text.add_field(name="!wordle_rating", value="Get your own wordle rating.",   inline=False)
      text.add_field(name="!give_me_zj", value="Give you a random ZeroJudge problem.", inline=False)
      text.add_field(name="!help", value="Show this message.", inline=False)
      await ctx.send(embed = text)
      
    except:
      print("err")
   
@client.event
async def ret():
    global st
    game = discord.Game(st)
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_ready():
    global st
    game = discord.Game(st)
    await client.change_presence(status=discord.Status.online, activity=game)

keep_alive()
client.run("OTY2MjE4OTE1ODU0Mjk5MTY5.Yl-jfQ.gclEba1KlI0TSlW8MwfY_znI6lU")
