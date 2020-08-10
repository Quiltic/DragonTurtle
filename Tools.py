# this is for the basic tools for turtle the ones that i use all the time but dont have to have clutering the main file

if __name__ == "__main__":
    # the gunk that is needed for this file. Mostly here so i dont have to get error messages for this file
    import discord
    from discord.ext import commands
    bot = commands.Bot(";")
    bertle = 275002179763306517


    #all of the needed imports
    import asyncio, subprocess
    import time, os, sys, requests, math
    from datetime import datetime

from random import randrange # achual needed import
 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Basic Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#this is to send complex messages and its from old turtle
async def sendmsg(ctx, msg = 'test', embed = None):
    if embed:
        await ctx.send(embed=embed)
    else:
        await ctx.send(msg)


async def sendmsgdirect(ctx, msg = 'embd', embed = None):
    if embed:
        await ctx.author.send(embed=embed)
    else:
        await ctx.author.send(msg)



#this is for old commands that dont work without it from message event yeah
async def sendmsgorig(message,msg):
    await message.channel.send(msg)

#this is for old commands that dont work without it from message event yeah
async def sendmsgorigdirect(message,msg):
    await message.author.send(msg)





# random number, I frankly just wanted this, dont remember why
def randomnum(low,high):
    return randrange(low,high+1)