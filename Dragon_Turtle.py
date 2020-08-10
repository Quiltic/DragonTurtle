
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Imports ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#all of the needed imports
import asyncio, subprocess
import time, random, os, sys, requests, math
from datetime import datetime



""" This is to get discord and have it be up to date on startup. This is mostly for my raspberry pi server. I dont update the discord that often there """

try:
    print("Trying to import discord!")
    os.system("python3 -m pip install --upgrade discord.py")
    import discord
    from discord.ext import commands
except:
    print("Cant import just recollecting it.")
    os.system("python3 -m pip install discord.py")
    import discord
    from discord.ext import commands


""" This is to know if I am on the pi or laptop """
from sys import platform
if platform == "linux" or platform == "linux2":
    # linux
    print('Using Linux')
    FilesType = '//'
elif platform == "darwin":
    # OS X
    # OS! OS! WHAT THE HELL!
    print('OS! OS! WHAT!?')
elif platform == "win32":
    # Windows
    print('Using Windows')
    FilesType = '\\'

#print(open('C:\\Users\\Quiltic\\Anaconda3\\lib\\site-packages\\JTools\\DictionaryLines.txt.txt','r').readlines())

from JTools import Save, Load, spellCheck




# get the other main files
from Tools import sendmsg, sendmsgorig, sendmsgorigdirect


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Basic Bot Starting Stuff ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
prefix = ('[] ', '[]') # the prefixes for the commands
bot = commands.Bot(prefix) # start of bot
curr_status = discord.Activity(name="dragon sounds. | []help", type=discord.ActivityType.listening) # for style points
bertle = 275002179763306517 # my id number
pause = False # this is to stop a turtle without achualy stoping it. Nice eah?
cwd = os.getcwd() # get home directory



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Cog Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# load X cog
@commands.is_owner()
@bot.command()
async def loadcog(ctx, name):
    """
    This is a command for turtle that loads a spesific cog.
    BERTLE ONLY!
    """
    await sendmsg(ctx, f"Loading {name}!")
    bot.load_extension(f'Cogs.{name}')
    await sendmsg(ctx, f"Sucsessfully Loaded {name}!")


# unload X Cog
@commands.is_owner()
@bot.command()
async def unloadcog(ctx, name):
    """
    This is a command for turtle that unloads a spesific cog.
    BERTLE ONLY!
    """
    
    await sendmsg(ctx, f"Unloading {name}!")
    bot.unload_extension(f'Cogs.{name}')
    await sendmsg(ctx, f"Sucsessfully Unloaded {name}!")

# reload X Cog
@commands.is_owner()
@bot.command()
async def reloadcog(ctx, name = None):
    """
    This is a command for turtle that reloads a spesific cog.
    BERTLE ONLY!
    """
    if name != None:
        await sendmsg(ctx, f"Reloading {name}!")
        bot.reload_extension(f'Cogs.{name}')
        await sendmsg(ctx, f"Sucsessfully Reloaded {name}!")
    else:
        # reload all cogs
        for filename in os.listdir('./Cogs'):
            if filename.endswith('.py'):
                await sendmsg(ctx, f"Reloading {filename[:-3]}!")
                bot.reload_extension(f'Cogs.{filename[:-3]}')
                await sendmsg(ctx, f"Sucsessfully Reloaded {filename[:-3]}!")
        await sendmsg(ctx, f"Sucsessfully Reloaded All Files!")



# load cogs at beginging of program
for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'Cogs.{filename[:-3]}')



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Owner Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#Turn off
@commands.is_owner()
@bot.command()
async def perish(ctx):
    """Force turns me off. BERTLE ONLY"""
    await sendmsg(ctx,"Im off now.")
    print("Bye!")
    #pi.stop()
    await bot.close()


#Turn off for the bot to use when updating
async def turnoff(ctx):
    await sendmsg(ctx,"Restarting?")
    print("Bye!")
    #pi.stop()
    await bot.close()
        

@commands.is_owner()
@bot.command()
async def update(ctx):
    """This updates Turtle to the latest version of itself from github. BERTLE ONLY"""
    await sendmsg(ctx,"Updating")
    print("On")
    print(cwd)
    #go home you lazy bumb
    os.system(("cd "+ cwd))

    await sendmsg(ctx,"Directory changed")
    print("changed cd")
    #open update
    call_freind = "python3 /home/pi/DragonTurtle/TurtleUpdate.py &"
    print(call_freind)
    os.system(call_freind)
    #subprocess.Popen(callfreind)

    await sendmsg(ctx,"Opened Friend!")
    print("Summoned!")
        
    #turn off
    await turnoff(ctx)


#this uploads turtle to github if enabled.
@commands.is_owner()
@bot.command()
async def upload(ctx):
    """This uploads the current version of Turtle to github. BERTLE ONLY"""
    os.system(("cd "+ cwd))
    os.system("git add .")
    time.sleep(1)
    os.system("git commit -m Turtle pushed me.")
    time.sleep(3)
    os.system("git push")


@commands.is_owner()
@bot.command()
async def ipaddress(ctx):
    """This gives the current IP for the Server that it is running on. BERTLE ONLY"""
    #Yoinked from https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib/24564613#24564613
    if os.name != "nt":
        import fcntl #this only works on luinex dont know why
        import struct
        def get_interface_ip(ifname):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(
                    s.fileno(),
                    0x8915,  # SIOCGIFADDR
                    struct.pack('256s', bytes(ifname[:15], 'utf-8'))
                    # Python 2.7: remove the second argument for the bytes call
                )[20:24])

    import socket
    IPAddr = socket.gethostbyname(socket.gethostname())
    if IPAddr.startswith("127.") and os.name != "nt":
        interfaces = ["eth0","eth1","eth2","wlan0","wlan1","wifi0","ath0","ath1","ppp0"]
        for ifname in interfaces:
            try:
                IPAddr = get_interface_ip(ifname)
                break
            except IOError:
                pass    

    await ctx.send(IPAddr)
    

    
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Start up ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# this may still be needed if I ever want to remove the helper cog
#@bot.event
#async def on_ready():
    #global guilds
#    await bot.change_presence(activity=curr_status)

#    print("Let's Do This!")


# I will maby use this eventualy I think
class TurtleException(Exception):
    """Use this exception to halt command processing if a different error is found.
    Only use if the original error is gracefully handled and you need to stop
    the rest of the command from processing. E.g. a file is not found or args
    are invalid."""
    def __init__(self, error, msg):
        self.error = error
        self.message = msg
        #super.__init__(error)

    def __str__(self):
        return self.error

@bot.event
async def on_command_error(ctx, e):
    if type(e) is commands.errors.CommandInvokeError:
        e = e.original
        if type(e) is TurtleException:
            print('Caught TurtleException: ' + str(e))
            await ctx.send(e.message)
    else:
        raise e


# i will have to redo this from the ground up. sadly. ... When i get to it.. eventualy
#'''
@bot.event
async def on_message(message):

    global pause

    if message.content.startswith(prefix):
        print("Command!")
        print(f'{message.author.name} - {message.guild} #{message.channel}: {message.content}')

    elif message.author == bot.user:
        print("Im talking:")
        print(f'{message.author.name} - {message.guild} #{message.channel}: {message.content}')


    #elif message.author == cur_user:
    #    await conversate(message)

    #elif ("hey turtle" in message.content.lower()):
    #    await sendmsgorig(message,"What?!")
    #    cur_user = message.author
    #    print(cur_user)

    elif "thanks turtle" in message.content.lower(): 
        if message.author.id == bertle:
            await sendmsgorig(message, "No problem Boss!")
        else:
            await sendmsgorig(message, "Your welcome!")

    elif "smite" in message.content.lower(): 
        await sendmsgorig(message, "⚡**SMITE!**⚡")

    elif "please" in message.content.lower(): 
        if message.author.id == bertle: # this was too iritating otherwise
            await sendmsgorig(message, "PRETTY PLEASE!")

    elif "hi turtle" in message.content.lower(): 
        await sendmsgorig(message, "Hello!")

    elif "fuck you" in message.content.lower(): 
        await sendmsgorig(message, "Well ok then.")

    #elif message.content.startswith("[] "): 
    #    if message.author.id == bertle:
    #        await sendmsgorig(message, "PRETTY PLEASE!")


    # so I can have multiple turtles running one on my laptop and one on the pi 
    # this is not a command because otherwise it would achualy be a nightmare to use
    elif "pause running turtle" in message.content.lower(): 
        if message.author.id == bertle:
            await sendmsgorig(message, "Paused.")
            pause = True
    
    elif "play running turtle" in message.content.lower(): 
        if message.author.id == bertle:
            await sendmsgorig(message, "Playing!")
            pause = False

    # i dont know if this is finished yet. Please dont use this
    elif "turtle end me" in message.content.lower(): 
        if message.author.id != bertle:
            await sendmsgorig(message, "Rocks fall. Lightning strikes. Your dead, get fucked.")

            await sendmsgorigdirect(message,"Rocks fall. Lightning strikes. Your dead, get fucked.")

            await sendmsgorigdirect(message,"You where kicked from the server. Here is the link back.")
            inviteLink = await message.channel.create_invite(max_uses = 1)
            
            await sendmsgorigdirect(message,inviteLink)

            await message.author.kick()
            
        else:
            await sendmsgorig(message, "Sorry Boss. Can't kill Gods.")


    else:
        print(f"{message.author.name} - {message.guild} #{message.channel}: ", message.content.split('\n'))

    if not pause:
        await bot.process_commands(message)

#'''

if __name__ == '__main__':
    global source_path
    source_path = os.path.dirname(os.path.abspath(__file__)) # /a/b/c/d/e

    #logging.basicConfig(level=logging.ERROR)

    try:
        file = open("Token.txt")
    except:
        file = open('/home/pi/Turtle/Token.txt')
    token = file.read()
    file.close()

    bot.run(token.strip())