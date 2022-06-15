import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup as bsp
import random
from keep_alive import keep_alive
from replit import db
import time
import json

up = [0, 3,3,5,5,10, 10,20,20,30,50 ,100, "inf"]
#print(db["words_list"])
client = commands.Bot(command_prefix='!')

#db["words_list"]=["assign","assassin","continue","attach","relentless","ruthless","except","lonely","pneumonoultramicroscopicsilicovolcanoconiosis","employee","sin","appeal","quantity","impose","confront","dodge","part","immortal","substitute","framework","sorry","on","at","notify","authority","threat","thread","by"]
ans_for_wordle=""
guess_count = 0 
mode = 0;
transform = [":regional_indicator_a:",":regional_indicator_b:",":regional_indicator_c:"]

@client.event
async def return_ans():
  return discord.Embed(title="wordle",                      description="answer: "+ans_for_wordle)


@client.event
async def insert_new(word):
    global db
    added = ""
    try:    
      words_for_insert = word.lower().split(",")
      if(len(words_for_insert) > 5):
        return discord.Embed(title="wordle",                      description="Insert failed.\nYou can't insert more than 5 words at once.")
      for i in words_for_insert:
        if await validator(i.strip())==True:
          db["words_list"].append(i.strip())
          added+=(i.strip()+" ")
        time.sleep(1)
      if len(added) == 0:
        return discord.Embed(title="wordle",                      description="Insert failed.\nMaybe the word is wrong?")
      return discord.Embed(title="wordle",                      description="New words: "+added+"were added.")
    except:
      return discord.Embed(title="wordle",                      description="Insert failed.\nSome errors occured.")
      
  
@client.event
async def remove_word(word):
    global db
    deled = ""
    v = ""
    try:
      words_for_remove = word.lower().split(",")
      if(len(words_for_remove) > 5):
        return discord.Embed(title="wordle",                      description="Remove failed.\nYou can't remove more than 5 words at once.")
      for j in words_for_remove:
        v = j.strip()
        for i in db["words_list"]:
          if i == v :
            db["words_list"].remove(v)
            deled += v
            deled += " "
      if len(deled) == 0:
        return discord.Embed(title="wordle",                      description="Remove failed.\nMaybe the word is wrong?")
      return discord.Embed(title="wordle",                      description="The words: "+deled+"have been removed.")
    except:
      return discord.Embed(title="wordle",                      description="Remove failed.\nSome errors occured")
  
@client.event
async def validator(word):
    global db
    try:
        r = requests.get("https://www.dictionary.com/browse/"+word, timeout=4)
        if(str(r)=="<Response [200]>"):
          for i in db["words_list"]:
            if i == word :
              return False
          return True
        else:
          return False

    except:
       return False
          
          
@client.event
async def check(word):
    global guess_count, ans_for_wordle
    if(len(word)!=len(ans_for_wordle)):
       return discord.Embed(title="wordle",                      description="Command failed.\nThe length of the word is wrong")
    try:
        r = requests.get("https://www.dictionary.com/browse/"+word, timeout=4)
        if(str(r)=="<Response [200]>"):
          guess_count += 1
          verdict = ""
          a=list(word.lower())
          b=list(ans_for_wordle)
          ver=[0]*len(ans_for_wordle)
          for i in range(0,len(ans_for_wordle)):
            if(a[i]==b[i]):
              ver[i]=2
              a[i]="!"
              b[i]="?"
          for i in range(0,len(ans_for_wordle)):
            for j in range(0,len(ans_for_wordle)):
              if(a[i]==b[j]):
               ver[i]=1
               a[i]="!"
               b[j]="?"
          if mode==0:
            for i in range(0,len(ans_for_wordle)):
              if(ver[i]==0):
                verdict+=":black_large_square: " 
              if(ver[i]==1):
                verdict+=":yellow_square: " 
              if(ver[i]==2):
                verdict+=":green_square: " 
          if mode==1:
            for i in range(0,len(ans_for_wordle)):
              if(ver[i]==0):
                verdict+=transform[0]
              if(ver[i]==1):
                verdict+=transform[1] 
              if(ver[i]==2):
                verdict+=transform[2]
          return discord.Embed(title="wordle",                      description="Your guess: "+word+"\nResult: "+verdict+"\nGuess count: "+str(guess_count))
        else:
          return discord.Embed(title="wordle",                      description="Command failed.\nThe word doesn't exist")
    except:
        return discord.Embed(title="wordle",                      description="Command failed.\nSomething went wrong...")
# codeforce
def get_cf(name):
    try:
      r = requests.get("https://codeforces.com/api/user.info?handles="+name, timeout=4)
      data=json.loads(r.text)
      user=data['result'][0]
      rate_name=user['rank']
      print(rate_name)
      rating=str(user['rating'])
      rating2=str(user['maxRating'])
      if (rate_name == "Unrated"):
        return discord.Embed(title=name,
                             url="https://codeforces.com/profile/" + name,
                             description=rate_name)
      else:
        color = discord.Color.light_gray()
        if (rate_name == "pupil"):
            color = discord.Color.green()
        elif (rate_name == "specialist"):
            color = discord.Color.teal()
        elif (rate_name == "expert"):
            color = discord.Color.blue()
        elif (rate_name == "candidate master"):
            color = discord.Color.purple()
        elif (rate_name == "master" or rate_name == "international Master"):
            color = discord.Color.gold()
        elif (rate_name == "grandmaster"
              or rate_name == "international grandmaster"
              or rate_name == "legendary grandmaster"):
            color = discord.Color.dark_red()
        return discord.Embed(
          title="Codeforces - "+name,url="https://codeforces.com/profile/" + name, description="Ranking: " +rate_name+"\nCurrent rating: "+rating+"\nHighest rating: "+rating2, color=color)

    except:
        return discord.Embed(title="Exception",description = "no such rated user or something wrong")


#ZJ
def num(a):
    try:
      int(a)
      return True
    except:
      return False


def fill_with_zero(x):
    if x < 10: return "00" + str(x)
    if x < 100: return "0" + str(x)
    return str(x)


async def get_zj():
    s = ""
    c = ""
    cnt = 0
    while (s == "" and (cnt < 10)):
        ran = random.randint(1, 999)
        ch = random.randint(1, 9)
        if (ch == 1): c = "a"
        if (ch == 2): c = "b"
        if (ch == 3): c = "c"
        if (ch == 4): c = "d"
        if (ch == 5): c = "e"
        if (ch == 6): c = "f"
        if (ch == 7): c = "g"
        if (ch == 8): c = "h"
        if (ch == 9): c = "i"
        s = "https://zerojudge.tw/ShowProblem?problemid=" + c + str(
            fill_with_zero(ran))
        try:
            r = requests.get(s, timeout=4)
        except:
            return "Exception occurred. "
        data = bsp(r.text, "html.parser")
        L = len(data.getText())
        if (L < 900):
            s = ""
            cnt += 1
            time.sleep(0.5)
        else:
            box = data.find("div", {"class": "container"})
            box_again = box.find("div", {"class": "h1"})
            title = box_again.find("span", {"id": "problem_title"})
            title2 = title.getText()
            if title2 == "Unfinished!":
                s = ""
                cnt += 1
                time.sleep(1)
    return s


#atcoder
def get_ac(name):
    color = discord.Color.light_gray()
    try:
        r = requests.get("https://atcoder.jp/users/" + name, timeout=4)
    except:
      return discord.Embed(title=name,description="404 not found", color=color)

    data = bsp(r.text, "html.parser")
    box = data.find("div", {
        "class": "col-md-9 col-sm-12"
    })
    if(box==None):
      return discord.Embed(title="Exception",description="not found", color=color)
    boxx = box.getText().strip(" ")
    cnt = 0
    ok = False
    list = []
    for i in boxx:
        if ok == False:
            if (num(i)):
                cnt = int(i)
                ok = True
        else:
            if (num(i)):
                cnt *= 10
                cnt += int(i)
            else:
                ok = False
                list.append(cnt)
    if (len(list) < 2):
        return discord.Embed(title=name,
                             url="https://atcoder.jp/users/" + name,
                             description="not rated",
                             color=color)
    if (list[1] >= 400):
        color = discord.Color.dark_orange()
    if (list[1] >= 800):
        color = discord.Color.green()
    if (list[1] >= 1200):
        color = discord.Color.teal()
    if (list[1] >= 1600):
        color = discord.Color.dark_blue()
    if (list[1] >= 2000):
        color = discord.Color.gold()
    if (list[1] >= 2400):
        color = discord.Color.orange()
    if (list[1] >= 2800):
        color = discord.Color.dark_red()
    return discord.Embed(title="AtCoder - "+name,
                         url="https://atcoder.jp/users/" + name,
                         description="rank: " + str(list[0]) +
                         "\ncurrent rating: " + str(list[1]) +
                         "\nhighest rating: " + str(list[2]),
                         color=color)
#random shuffle
def rs():
  global transform  
  random.shuffle(transform)
  print(transform)

def select_word():
  global ans_for_wordle,db
  ans_for_wordle=db["words_list"][random.randint(0,len(db["words_list"])-1)]
  
  
async def wcheck(user):
  global db, up
  tmp=discord.Embed(title="wordle")
  if(db['wordler_status'].get(user)==None):
      return discord.Embed(title="wordle",description="not found in database.")
  tmp.add_field(name="User name", value=str(user), inline=False)
  tmp.add_field(name="Current level", value="level "+str(db['wordler_status'][user][0]), inline=False)
  tmp.add_field(name="Progress", value=str(db['wordler_status'][user][1])+" / "+str(up[db['wordler_status'][user][0]]), inline=False)
  tmp.add_field(name="Total score", value=str(db['wordler_status'][user][2]), inline=False)
  return tmp
  
  
    
  
