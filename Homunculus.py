import discord
import asyncio
import random
import urllib.request
import urllib.parse
import re
from discord.ext import commands
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# from apiclient.discovery import build
# from apiclient.errors import HttpError
#import google_auth_oauthlib.flow
#import simplejson

description = 'Homunculus Bot, advanced version'
playlist = []

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description=description)
youtube_api_key = 'AIzaSyAZ1AgebKW8w8Nzs__jMpqRBVmVH4jtWe8'
youtube_client_id = '216353908791-qavvvln2vsv1ut1knpuiv0d1oqgd1ogf.apps.googleusercontent.com'
youtube_client_secret = 'rk3CphP4BqL6fQVhYdaNvCjL'
youtube_scopes = 'https://www.googleapis.com/auth/youtube.force-ssl'


def youtube_search(query : str):
    # youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    # #response = youtube.search().list('snippet', '5', query, 'video').execute()
    # #return response
    # response = youtube.search(query)
    # return response
    query_string = urllib.parse.urlencode({"search_query" : query})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    return search_results

	
def rollNormalDice(diceNumber, diceSides, modifier):
    loopIterator = 0
    rollList = []
    total = 0
    while (diceNumber > loopIterator):
        roll = random.randint(1, diceSides)
        total += roll
        rollList.append(str(roll))
        loopIterator = loopIterator + 1
    total += modifier
    rollList.append('__**Final Total: ' + str(total) + '**__')
    finalResult = (', '.join(rollList))
    return finalResult


def rollFudgeDice(diceNumber, modifier):
    rollList = []
    result = []
    #loopIterator = 0
    while diceNumber > loopIterator:
        rollList.append(random.randint(1, 4))
        loopIterator += 1
    while rollList:
        roll = rollList.pop()
        if roll == 1:
            result.append('-')
        elif roll == 2:
            result.append('0')
        else:
            result.append('+')
    positives = rollList.count('+')
    negatives = rollList.count('-')
    total = positives - negatives + modifier
    result.append('__**Total: ' + str(total) + '**__')
    finalResult = (', '.join(result))
    return finalResult


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------------------------------')


@bot.command()
async def roll(dice: str):
    # Rolls dice
    numberOfDice, sidesOfDice = dice.split('d')
    numberOfDice = numberOfDice.strip()
    sidesOfDice = sidesOfDice.strip()
    if 'f' in sidesOfDice:
        if '+' in sidesOfDice:
            sidesOfDice, modifier = sidesOfDice.split('+')
            intModifier = int(modifier)
            await bot.say(rollFudgeDice(int(numberOfDice), intModifier))
        elif '-' in sidesOfDice:
            sidesOfDice, modifier = sidesOfDice.split('-')
            intModifier = int(modifier) - (int(modifier) * 2)
            await bot.say(rollFudgeDice(int(numberOfDice), intModifier))
        else:
            await bot.say(rollFudgeDice(int(numberOfDice), 0))
    else:
        if '+' in sidesOfDice:
            sidesOfDice, modifier = sidesOfDice.split('+')
            intModifier = int(modifier)
            await bot.say(rollNormalDice(int(numberOfDice), int(sidesOfDice), intModifier))
        elif '-' in sidesOfDice:
            sidesOfDice, modifier = sidesOfDice.split('-')
            intModifier = int(modifier) - (int(modifier) * 2)
            await bot.say(rollNormalDice(int(numberOfDice), int(sidesOfDice), intModifier))
        else:
            await bot.say(rollNormalDice(int(numberOfDice), int(sidesOfDice), 0))

@bot.command(pass_context = True)
async def addQuote(ctx):
    quotes = open('quotes.txt', 'r')
    currentQuotes = quotes.read()
    quotes = open('quotes.txt', 'w')
    quote = ctx.message.content[10:]
    quotes.write(currentQuotes + '\n' + quote)
    quotes.write
    quotes.close()
    await bot.say("Quote added!")


@bot.command()
async def quote():
    quoteList = []
    iterator = 0
    quotes = open('quotes.txt', 'r')
    quoteList = quotes.read().split('\n')
    quotes.close()
    await bot.say(random.choice(quoteList))
    quoteList.clear


@bot.command(pass_context=True, no_pm=True)
async def join(ctx):
    channel = ctx.message.author.voice_channel
    if channel is None:
        await bot.say('Join a channel first dingus')
    else:
        global vc
        vc = await bot.join_voice_channel(channel)


@bot.command(pass_context=True)
async def disconnect(ctx):
    if bot.is_voice_connected(ctx.message.server):
        await vc.disconnect()
    else:
        await bot.say("Not in a voice channel, and I wouldn't want to be in the same one as you turd")


# @bot.command()
# async def play(*, searchTerms : str):
#
#     results = youtube_search(searchTerms)
#     resultstring = ''
#     iterator = 1
#
#     player = await vc.create_ytdl_player(results)
#     player.start()


@bot.command(pass_context=True)
async def airhorn(ctx):
    vc = await bot.join_voice_channel(ctx.message.author.voice_channel)
    player = await vc.create_ytdl_player('https://www.youtube.com/watch?v=2Tt04ZSlbZ0')
    player.start()
    #vc.disconnect()


@bot.command(pass_context = True)
async def test(ctx):
    print(ctx.message.content)

@bot.command()
async def createPlayList(message : str):
    global player
    player = await vc.create_ytdl_player('https://www.youtube.com/watch?v=lMAxL7ef_A8')
    player.start()


@bot.command()
async def play(message : str):
    if player.is_live:
        playlist.append(message)
    else:
        player = vc.create_ytdl_player(message)
        #player(message)
        player.start()

@bot.command()
async def fight():
    genders = ('male', 'female')
    magics = ('aeromancer', 'geomancer', 'hydromancer', 'shaman', 'summoner')
    gender = random.choice(genders)
    magic = random.choice(magics)
    powerLevel = random.randint(1, 100)
    willingnessToFight = random.randint(1, 100)
    await bot.say('You are fighting a ' + gender + ' ' + magic + ', who has a power level (between 1 and 100) of ' +
                  str(powerLevel) + ' and on a scale of 1 to 100, is about ' + str(willingnessToFight)
                  + ' on their willingness to fight')
bot.run('MzkzNDE5MzE2NTk2NDQxMDk2.DR3maw.LYHVZPWF1IbHDof0QNvh7kzv-J8')