import discord
import asyncio
import random
from discord import Member
from discord.ext import commands
from discord.ext.commands import has_permissions #, MissingPermissions
import sqlite3
import config
import dice
import hat
## TODO: Replace all appearances of ctx.messagen.contents
## TODO: replace appearances of ctx.message.channel.send
## TODO: add advantage rolls for dice
## TODO: have rolls ping rollee
## TODO: beautify bot responses in rolls 
description = 'Homunculus Bot, advanced version'
playlist = []

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description=description)

helpdict = {
        'roll' : 'Rolls dice with a variety of options. The format is \'!roll [x]d[y]+[modifier], x being the number of dice to roll, and y being the number of sides on the dice. Append -e for exploding dice, -s for shadowrun style dice, and -se for both. Roll fudge dice by typing in [x]df, x being the number of dice.',
        'help' : 'Good God it is a help command. If you need help using it I have no hope for you.',
        'fight' : 'Creates a random arena fight for magic school.',
        'rollWeeks' : 'Rolls weeks for magic school. Input data in this order: \n [Number of weeks to roll for] \n [Number of days  in a week (exclude weekend)] \n [Number of actions in a weekday] \n [Number of days on the weekend] \n [number of actions on weekend] \n [total modifier to roll with]' 
        } 

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------------------------------')

@bot.command(pass_context = True, description='Roll x number of dice with y faces, using the \'X\'d\'Y\' format')
async def roll(ctx, arg):
    # rolls = dice.dice(ctx.message.content[6:])
    # await ctx.message.channel.send(rolls.toString)
    rolls = dice.dice(arg)
    await ctx.send(rolls.toString)

@bot.command(pass_context=True, no_pm=True, description='Joins user in current voice chat channel')
async def join(ctx):
    channel = ctx.message.author.voice_channel
    if channel is None:
        await bot.send('Join a channel first dingus')
    else:
        global vc
        vc = await bot.join_voice_channel(channel)

@bot.command(pass_context=True, description='Leaves current voice channel. Must be in a voice chat')
async def disconnect(ctx):
    if bot.is_voice_connected(ctx.message.server):
        await vc.disconnect()
    else:
        await bot.say("Not in a voice channel, and I wouldn't want to be in the same one as you turd")

@bot.command(pass_context=True, description='Try it while in a voice chat channel :)')
async def airhorn(ctx):
    vc = await bot.join_voice_channel(ctx.message.author.voice_channel)
    player = await vc.create_ytdl_player('https://www.youtube.com/watch?v=2Tt04ZSlbZ0')
    player.start()
    #vc.disconnect()


@bot.command()
async def createPlayList(message : str):
    # TODO fix
    global player
    player = await vc.create_ytdl_player('https://www.youtube.com/watch?v=lMAxL7ef_A8')
    player.start()


@bot.command()
async def play(message : str):
    # TODO fix
    if player.is_live:
        playlist.append(message)
    else:
        player = vc.create_ytdl_player(message)
        #player(message)
        player.start()

@bot.command(description='Creates a randomized fighter for arena fights in Magic School roleplaying game')
async def fight():
    genders = ('male', 'female')
    magics = ('aeromancer', 'geomancer', 'hydromancer', 'shaman', 'summoner')
    gender = random.choice(genders)
    magic = random.choice(magics)
    powerLevel = random.randint(1, 100)
    willingnessToFight = random.randint(1, 100)
    await ctx.send('You are fighting a ' + gender + ' ' + magic + ', who has a power level (between 1 and 100) of ' +
                  str(powerLevel) + ' and on a scale of 1 to 100, is about ' + str(willingnessToFight)
                  + ' on their willingness to fight')



@bot.command(pass_context=True, description='Function that rolls multiple weeks of actions in Magic School Roleplaying Game')
async def rollWeeks(ctx, numberOfWeeks, normalDays, normalDayActions, numberOfWeekendDays, weekendActions, modifier):
    # needs to pass 6 parameters:
    # number of weeks, 
    # number of normal days, 
    # actions during a normal day,
    # number of weekend days,
    # number of actions on weekend,
    # and then the modifier 
    # inputString = ctx.message.content[10:]
    ## TODO
    pass

@bot.command()
async def rollStats(ctx):
    # rolls 4d6, dropping the lowest number, six times to allow for D&D 5e character creation
    # TODO 
    statList = []
    for i in range(0, 6):
        rollList = []
        stat = 0
        for j in range(0, 4):
            rollList.append(random.randint(1, 6))
        rollList.remove(min(rollList))
        for roll in rollList:
            stat = stat + roll
        statList.append(stat)
    await ctx.send(statList)
    
@bot.listen()
async def on_message(message): 
    if 'your' in message.content.lower() and message.author.id != bot.user.id:
        await message.channel.send("Hey you big fucking idiot, did you use the proper form of your/you're? I bet not you buffoon, you coward, you cretin you imbecile. Fuck you.")
        

bot.run(config.token)
