

from Tools.Tools import *
from Tools.Dice import *

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


"""
Todo:


"""


#from pydub import AudioSegment
#from guild_info import GuildInfo

#from help import helpEmbed, get_list_embed, make_sounds_dict, get_rand_activity

#tts_path = 'resources/voice.exe'


""" Basic startup for a discord bot"""
prefix = ('[] ', '[]')
bot = commands.Bot(prefix)#, connector=aiohttp.TCPConnector(ssl=False)
curr_status = discord.Activity(name="dragon sounds. | []help", type=discord.ActivityType.listening)

#get home directory
cwd = os.getcwd()

bertle = 275002179763306517 #my id  #bot.get_user(bot.owner_id)
cur_user = 0 # the curent user that is talking to turtle
pause = False

using = jt.Load('ActiveUsing')


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Custom Admin Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
@bot.command()
async def showTerminal(ctx, *args):
    """ Basicly is an ssh into the rasberry pi """
    cmd = []
    for a in args:
        cmd.append(a)
    print(cmd)

    if await check_perms(ctx):
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE ).communicate() # the part that runs the command into the terminal
        #output = pipe.read()
        for out in output:
            #words = "```" + out + "```"
            await ctx.send(out) # Print the output of the terminal, it will look weard because it keeps the "b " and \n dont know why
    else:
        await ctx.send("Failed!")

@bot.command()
async def update(ctx):
    """This updates Turtle to the latest version of itself from github. BERTLE ONLY"""
    if await check_perms(ctx):
        await sendmsg(ctx,"Updating")
        print("On")
        print(cwd)
        #go home you lazy bumb
        os.system(("cd "+ cwd))

        await sendmsg(ctx,"Directory changed")
        print("changed cd")
        #open update
        call_freind = "python3 /home/pi/Turtle/TurtleUpdate.py &"
        print(call_freind)
        os.system(call_freind)
        #subprocess.Popen(callfreind)

        await sendmsg(ctx,"Opened Friend!")
        print("Summoned!")
        
        #turn off
        await turnoff(ctx)
    else:
        await ctx.send("Failed!")


#this uploads turtle to github if enabled.
@bot.command()
async def upload(ctx):
    """This uploads the current version of Turtle to github. BERTLE ONLY"""
    if await check_perms(ctx):
        os.system(("cd "+ cwd))
        os.system("git add .")
        time.sleep(1)
        os.system("git commit -m Turtle pushed me.")
        time.sleep(3)
        os.system("git push")
    else:
        await ctx.send("Failed!")


@bot.command()
async def ipadress(ctx):
    """This gives the current IP for the PI that it is running on. BERTLE ONLY"""
    if await check_perms(ctx):
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
    else:
        await ctx.send("Failed!")




async def check_perms(ctx):
    """ This gets weather or not the persion is me (Bertle) """
    print("Checking")
    user = ctx.author.id
    print(bertle,user) #see id of user vs my id
    if bertle == user:
        return(True)
    else:
        print("Cant give acsess to user: %s" % (ctx.author))
        await ctx.send("Sorry pal, but you dont have access.")
        return(False)



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Player Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
@bot.command()
async def save(ctx, tpe):
    '''
    Roll a save (STR, DEX, CON, INT, WIS, CHA)
    '''
    try:    
        lst = {'fighter':['STR','CON'], 'druid': ['WIS','INT'], 'artificer':['INT','CON'], 'barbarian':['STR','CON'], 'bard':['DEX','CHA'], 'cleric':['WIS','CHA'], 'monk':['STR','DEX'], 'paladin':['WIS','CHA'], 'ranger':['STR','DEX'], 'rouge':['DEX','INT'], 'sorcerer':['CON','CHA'], 'warlock':['WIS','CHA'], 'wizard':['INT','WIS']}
        
        mod = get_modifyer(using[str(ctx.author)],tpe.upper())
        dice = randomnum(1,20)

        if tpe.upper() in lst[using[str(ctx.author)]['Main Class'].lower().replace(' ','')]:
            mod += int(using[str(ctx.author)]['Proficiency'])

        speak = '**Rolled:** 1d20 [{}] +{}'.format(dice,mod)

        embed=discord.Embed(title="Saves!", color=0xe33604)
        embed.add_field(name=speak.replace('[1]','[**1**]').replace('[20]','[**20**]'), value='**Total**: '+ str(dice + mod), inline=False)
        
        await ctx.send(embed = embed)

    except KeyError as e:
        await sendmsg(ctx,"You havent taken on a character yet!")
        await sendmsg(ctx,"Do []player CHARACTER_NAME!")
        await sendmsg(ctx,"OR if you havent made a character yet do []character!")
        print('Error: ', e)
    except Exception as e:
        await sendmsg(ctx,"Op something went wrong.")
        print('Error: ', e)
    

@bot.command()
async def init(ctx, *args):
    '''
    Initiative
    '''
    try:    
        await roll(ctx,*('+' + str(using[str(ctx.author)]['Initiative'])))
        #await sendmsg(ctx,"{} now has {}/{} HP".format(using[str(ctx.author)]['Name'],using[str(ctx.author)]['Current HP'],using[str(ctx.author)]['HP']))
    
    except KeyError:
        await sendmsg(ctx,"You havent taken on a character yet!")
        await sendmsg(ctx,"Do []player CHARACTER_NAME!")
        await sendmsg(ctx,"OR if you havent made a character yet do []character!")
    except Exception as e:
        await sendmsg(ctx,"Op something went wrong.")
        print('Error: ', e)


@bot.command()
async def heal(ctx, damage):
    '''
    Heal or damage
    '''
    try:
        using[str(ctx.author)]['Current HP'] += int(damage)
        await sendmsg(ctx,"{}now has {}/{} HP".format(using[str(ctx.author)]['Name'],using[str(ctx.author)]['Current HP'],using[str(ctx.author)]['HP']))
    
    except KeyError:
        await sendmsg(ctx,"You havent taken on a character yet!")
        await sendmsg(ctx,"Do []player CHARACTER_NAME!")
        await sendmsg(ctx,"OR if you havent made a character yet do []character!")
    except Exception as e:
        await sendmsg(ctx,"Op something went wrong.")
        print('Error: ', e)


@bot.command()
async def harm(ctx, damage):
    '''
    Heal or damage
    '''
    try:
        using[str(ctx.author)]['Current HP'] -= int(damage)
        await sendmsg(ctx,"{}now has {}/{} HP".format(using[str(ctx.author)]['Name'],using[str(ctx.author)]['Current HP'],using[str(ctx.author)]['HP']))
    
    except KeyError:
        await sendmsg(ctx,"You havent taken on a character yet!")
        await sendmsg(ctx,"Do []player CHARACTER_NAME!")
        await sendmsg(ctx,"OR if you havent made a character yet do []character!")
    except Exception as e:
        await sendmsg(ctx,"Op something went wrong.")
        print('Error: ', e)


@bot.command()
async def character(ctx, *args):
    info = {'Spell Save': 10, 'Proficiency': 1,'Spell Attack': 1,'Name': 'NAMELESS', 'URL': None, 'AC': 10, 'Alignment': 'Unaligned', 'CHA': 10, 'CON': 10, 'Challenge Rating': 0, 'DEX': 10, 'HP': 10, 'INT': 10, 'Passive Perception': 10, 'STR': 10, 'Total Level': 1, 'Skills': 'Perception +3, Stealth +4', 'Speed': '30ft', 'Main Class': 'Fighter', 'WIS': 10}
    print('start')
    magic = {"monk":'wis',"rogue":'INT',"fighter":'INT',"warlock":'CHA','wizard': 'INT', 'druid': 'WIS', 'sorcerer': 'CHA', 'bard': 'CHA', 'paladin': 'CHA', 'ranger': 'WIS', 'artificer': 'INT', 'cleric': 'WIS'}
    try:
        if len(args) == 0: # basic help
            stuff = """```\n[]character |Name: __\n|Main Class: __\n|Total Level: __\n|AC: __\n|HP: __\n|Speed: __ft\n|STR: __\n|DEX: __\n|CON: __\n|INT: __\n|WIS: __\n|CHA: __\n|Skills: __\n|URL: __```"""
            await sendmsg(ctx,stuff)
            await sendmsg(ctx,"Copy the above then replace __ and send back") # with []player
            #await sendmsg(ctx,"Leaving __ will result with its default")

        elif len(args) == 1:
            info = jt.Load(('Players\\'+str(ctx.author).replace('#','_').replace(' ','') + args[0].lower().replace(' ','')))

            spl=discord.Embed(title=info['Name'], url=info['URL'], description="{}{}: {}".format(info['Main Class'],info['Total Level'],info['Alignment']), color=0x2778c0)
            #embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
            spl.add_field(name="AC", value=info['AC'], inline=True)
            spl.add_field(name="HP", value=str(info['Current HP'])+'/'+info['HP'], inline=True)
            spl.add_field(name="Speed", value=info['Speed'], inline=True)
            spl.add_field(name="Proficiency Bonus", value=info['Proficiency'], inline=False)
            spl.add_field(name="STR", value=info['STR'], inline=True)
            spl.add_field(name="DEX", value=info['DEX'], inline=True)
            spl.add_field(name="CON", value=info['CON'], inline=True)
            spl.add_field(name="INT", value=info['INT'], inline=True)
            spl.add_field(name="WIS", value=info['WIS'], inline=True)
            spl.add_field(name="CHA", value=info['CHA'], inline=True)

            if info['Main Class'][:-1].lower() in magic:
                spl.add_field(name="Spell Save", value=info['Spell Save'], inline=False)
                spl.add_field(name="Spell Attack", value=info['Spell Attack'], inline=False)
            #spl.set_footer(text="Challenge Rating: {}".format(info['Challenge Rating']))
            await ctx.send(embed = spl)
            
        else:
            info = make_charicter(ctx, *args)
            await sendmsg(ctx,"Created Charicter Save.")
            await player(ctx,info['Name'])

    except Exception as e:
        await sendmsg(ctx,"Op something went wrong.")
        print('Error: ', e)
            
        #print(*args)
        

#
@bot.command()
async def player(ctx, *args):
    global using
    if len(args) != 0:
        if args[0] == 'update':
            stuff = """```\n[]character |Name: {}\n|Main Class: {}\n|Total Level: {}\n|AC: {}\n|HP: {}\n|Speed: {}\n|STR: {}\n|DEX: {}\n|CON: {}\n|INT: {}\n|WIS: {}\n|CHA: {}\n|Skills: {}\n|URL: {}```""".format(using[str(ctx.author)]['Name'][:-1],using[str(ctx.author)]['Main Class'][:-1],using[str(ctx.author)]['Total Level'][:-1],using[str(ctx.author)]['AC'][:-1],using[str(ctx.author)]['HP'][:-1],using[str(ctx.author)]['Speed'][:-1],using[str(ctx.author)]['STR'][:-1],using[str(ctx.author)]['DEX'][:-1],using[str(ctx.author)]['CON'][:-1],using[str(ctx.author)]['INT'][:-1],using[str(ctx.author)]['WIS'][:-1],using[str(ctx.author)]['CHA'][:-1],using[str(ctx.author)]['Skills Prof'][:-2],using[str(ctx.author)]['URL'])
            await sendmsg(ctx,stuff)
            await sendmsg(ctx,"Copy the above update it and send back") # with []player
        else:
            using[str(ctx.author)] = jt.Load('Players\\'+str(ctx.author).replace('#','_').replace(' ','') + ''.join(args).lower().replace(' ',''))
            await sendmsg(ctx,"Linked!")
            jt.Save('ActiveUsing',using)
                
    else:
        try:
            await character(ctx,using[str(ctx.author)]['Name'])
            
        except KeyError:
            await sendmsg(ctx,"You havent taken on a character yet!")
            await sendmsg(ctx,"Do []player CHARACTER_NAME!")
            await sendmsg(ctx,"OR if you havent made a character yet do []character!")
        except Exception as e:
            await sendmsg(ctx,"Op something went wrong.")
            print('Error: ', e)
            
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### D&D Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# for rolling
@bot.command()
async def roll(ctx, *args):
    await r(ctx, *args)


# dice
@bot.command()
async def r(ctx, *args):
    """This rolls a # of dice and gives the output. Usage: []r 1d4 +4"""
    global using
    await ctx.message.add_reaction("🎲")
    specialTypes = ['strength','dexterity','constitution','intelligence','wisdom','charisma','acrobatics','animalhandling','arcana','athletics','deception','history','insight','intimidation','investigation','medicine','nature','perception','performance','persuasion','religion','sleightofhand','stealth','survival'] # thease are all skills in D&D... 
    try:
        things = list(args)
        for a in range(len(args)):
            for b in specialTypes:
                if args[a].lower() in b:
                    print(b)
                    things[a] = str(using[str(ctx.author)]['Skills'][b])
                    #print('hi')
                    if '-' not in things[a]:
                        things[a] = '+'+things[a]

                    await sendmsg(ctx,"Rolling for {}! {}".format(b,things[a]))
                    break
                    #print('hi')
    except KeyError:
        await sendmsg(ctx,"Improper skill name!")
    except Exception as e:
        print(e)
    print(things)

    stuff = diceBase(*things) # this is the raw data
    #await sendmsg(ctx,data)
    stuff['speak'] = '**Rolled:**'

    if 'try1' in stuff: # adv or disadv
        for a in stuff['try1']:
            if (a != 'total') and (a != 'speak'):
                stuff['speak'] += ' ' + a 
                if 'd' in a:
                    stuff['speak'] += ' ' + str(stuff['try1'][a])
        
        stuff['speak'] += ' &'

        for a in stuff['try2']:
            if (a != 'total') and (a != 'speak'):
                stuff['speak'] += ' ' + a 
                if 'd' in a:
                    stuff['speak'] += ' ' + str(stuff['try2'][a])

    else:    
        for a in stuff:
            if (a != 'total') and (a != 'speak'):
                stuff['speak'] += ' ' + a 
                if 'd' in a:
                    stuff['speak'] += ' ' + str(stuff[a])



    embed=discord.Embed(title="Rolls", color=0xe33604)
    embed.add_field(name=stuff['speak'].replace('[1]','[**1**]').replace('[20]','[**20**]'), value='**Total**: '+ str(stuff['total']), inline=False)
    

    await ctx.send(embed = embed)
    '''
    msg = ' '.join(args).lower()
    vals = tuple(msg.split(' ')[1:]) # + or - if there
    #print(vals)

    if 'adv' in msg: # advantage
        # cant do this nicely because of await
        if len(vals) > 0:
            diceA = await dice(True, *vals) 
            diceB = await dice(True, *vals)
        else:
            diceA = await dice(True) 
            diceB = await dice(True)

        stuff = ('Rolls: {} & {} : Best: {}'.format(diceA[1],diceB[1],max(diceA[1], diceB[1])), max(diceA[1], diceB[1]))

    elif 'dis' in msg: # disadvantage
        # cant do this nicely because of await
        if len(vals) > 0:
            diceA = await dice(True, *vals) 
            diceB = await dice(True, *vals)
        else:
            diceA = await dice(True) 
            diceB = await dice(True)

        stuff = ('Rolls: {} & {} : Worst: {}'.format(diceA[1],diceB[1],min(diceA[1], diceB[1])), min(diceA[1], diceB[1]))

    else:
        stuff = await dice(True, *args) # normal roll
    


    if len(stuff[0]) > 2000: # apparently this is discords max char limit
        await sendmsg(ctx, "Discord doesent like long stuffs so here is the summup.")
        #print(stuff[1])
        stuff = ('Total: {}'.format(stuff[1]),stuff[1]) # no overflow from numbers technicly could overflow but at that point
        if len(stuff[0]) > 2000:
            await sendmsg(ctx, "Why would you do this?")
            stuff = ('Its over 2000 charicters long.', None)

    await sendmsg(ctx,stuff[0])
    '''



# spells
@bot.command()
async def spell(ctx, *spell):
    """This finds and gives a spell. Usage: []spell fireball"""

    spell = ' '.join(spell).lower()

    async with ctx.channel.typing():
        await ctx.message.add_reaction("📖")
        #await sendmsg(ctx,"Refactoring spell list")

        #reloadSpellList()
        data = SpellBook(spell)

        print(data)
        #'''
        if (data != None) and (data != 'None'):
            spl=discord.Embed(title=data['name'], url=data['url'], description="School: {}".format(data['school']), color=0x2778c0)
            #embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
            spl.add_field(name="Level", value=data['cast']['level'], inline=True)
            spl.add_field(name="Casting Time", value=data['cast']['casting time'], inline=True)
            spl.add_field(name="Range", value=data['cast']['range'], inline=True)
            spl.add_field(name="Components", value=data['cast']['components'], inline=True)
            spl.add_field(name="Duration", value=data['cast']['duration'], inline=True)

            if len(data['does']) < 1000:
                spl.add_field(name="What Do", value=data['does'].replace('|n','\n'), inline=False)
            else:
                spl.add_field(name="What Do", value=(data['does'][:1000]).replace('|n','\n'), inline=False)

            spl.set_footer(text="Page: {}    |:|    Classes: {}".format(data['page'],data['classes']))
            await ctx.send(embed = spl)
        else:
            await sendmsg(ctx,"Cant get spell: {}".format(spell))
       


# book loader
@bot.command()
async def reloadSpells(ctx, book = 'Spells'):
    """This reloads a spell list. Usage: []reloadSpells"""
    if await check_perms(ctx):
        async with ctx.channel.typing():
            await sendmsg(ctx,"Reloading spell list")
            reloadSpellList(book)
            await sendmsg(ctx,"Finished")


# Monsters
@bot.command()
async def monster(ctx, *name):
    """This finds and gives a spell. Usage: []spell fireball"""

    name = ' '.join(name).lower()

    async with ctx.channel.typing():
        await ctx.message.add_reaction("📖")
        #await sendmsg(ctx,"Refactoring spell list")

        #reloadSpellList()
        Monster = findMonster(name)
        if type(Monster) == str:
            await sendmsg(ctx,"Cant get creature: link given.")
            await sendmsg(ctx,Monster)
        elif Monster == None:
            await sendmsg(ctx,"{} : Not found.".format(name.capitalize()))
            #await sendmsg(ctx,Monster)
        else:
            #print(data)
            #'''
            spl=discord.Embed(title=Monster['Name'], url=Monster['url'], description="{}{}:{}".format(Monster['Size'],Monster['Type'],Monster['Alignment']), color=0x2778c0)
            #embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
            spl.add_field(name="AC", value=Monster['AC'], inline=True)
            spl.add_field(name="HP", value=Monster['HP'], inline=True)
            spl.add_field(name="Speed", value=Monster['Speed'], inline=True)
            spl.add_field(name="STR DEX CON INT WIS CHA", value="  {}  {}  {}  {}  {}  {}".format(Monster['STR'],Monster['DEX'],Monster['CON'],Monster['INT'],Monster['WIS'],Monster['CHA']), inline=False)
            spl.set_footer(text="Challenge Rating: {}".format(Monster['Challenge Rating']))
            await ctx.send(embed = spl)
        
        print(Monster)
        #'''


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Custom Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@bot.command()
async def dragon(ctx):
    """Makes me react with 🐉🐢"""
    await ctx.message.add_reaction("🐉")
    await ctx.message.add_reaction("🐢")

@bot.command()
async def Yell(ctx):
    """Turtle just Yells at you"""
    await sendmsg(ctx,"AGGGG")

@bot.command()
async def GitURL(ctx):
    """This gives the git repository on github."""
    await ctx.send("My repository is: https://github.com/Quiltic/DragonTurtle")


# this is from old turtle but i still love it
async def conversate(message):
    global cur_user

    if "make me a sandwich" in message.content.lower(): # simple ping with a file
        await sendmsgorig(message, "Here you go!")
        await message.channel.send(file=discord.File('Sandwich.jpg'))

    elif "bubble" in message.content.lower(): # simple ping
        await sendmsgorig(message, "BUBBLES!")

    elif "random" == message.content.lower():
        await sendmsgorig(message, "RANDOM NUMBERS YOU SAY!?")
        for a in range(randomnum(2,24)):
            await sendmsgorig(message,randomnum(10,10000))
        await sendmsgorig(message, "Fin.")

    elif "what time is it" in message.content.lower():
        await sendmsgorig(message, "TURTLE TIME!")
        msg = "🐢"
        for a in range(randomnum(2,24)):
            msg = msg + "🐢"
        await sendmsgorig(message, msg)

    elif "i need an army" in message.content.lower():
        await sendmsgorig(message, "On it boss!")
        msg = "🐢"
        rand = randomnum(100,200)
        for a in range(rand):
            msg = msg + "🐢"
        await sendmsgorig(message, msg)
        msg = "I was able to get " + str(rand) + " Turtles for the cause!"
        await sendmsgorig(message, msg)

    elif "yell at " in message.content.lower():
        msg = ("They arnt here, sorry %s." % (message.author.name))
        for users in bot.users:
            for b in message.guild.members:
                if b == users:
                    if message.content.lower()[8:] in users.name.lower():
                        msg = "Hey <@%s>! %s wants you." % (users.id,message.author.name)
        await sendmsgorig(message, msg)

    elif "help" in message.content.lower():
        await sendmsgorig(message, "I can yell at someone, make a sandwich, I like bubbles, and randomness..., help rase an army, get the time")
        await sendmsgorig(message, "Helpful?")
    else:# simple ping
        await sendmsgorig(message, "Ok then!") 
    
    cur_user = 0

@bot.command()
async def loadFile(ctx, NAME):
    for l in printFile(NAME):
        await ctx.send(l)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Basic Sound Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

'''
def source_factory(filename):
    op = '-guess_layout_max 0'
    return discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename, before_options=op))


def get_sound(sound):
    try:
        return os.path.join('//sounds', (sound.lower()+'.mp3'))
    except KeyError:
        return None


def delete_sound(sound):
    path = '//sounds'
    os.remove(sound)

async def add_sound_to_guild(sound, guild):
    folder = '//sounds'
    filename = sound.filename.lower()

    path = os.path.join(folder, filename)

    await sound.save(path)


def play_sound_file(sound, vc, output=True):
    source = source_factory(sound)
    source.volume = guilds[vc.channel.guild.id].volume
    stop_audio(vc)
    vc.play(source)

    if output:
        c = t.CYAN
        print(f'Playing {sound} | at volume: {source.volume} | in: {c}{vc.guild} #{vc.channel}')


@bot.command()
async def play(ctx, *args):
    """Play a sound."""
    if not args:
        raise TurtleException('No sound specified in play command.',
                             'GIMY FILE!')

    sound = ' '.join(args)
    current_sound = get_sound(sound, ctx.guild)
    if not current_sound:
        raise TurtleException('Sound ' + sound + ' not found.',
                             "That sound doesn't exist.")

    vc = await connect_to_user(ctx)
    play_sound_file(current_sound, vc)
'''



@bot.command()
async def join(ctx):
    """Join the user's voice channel."""
    await connect_to_user(ctx)


@bot.command()
async def leave(ctx):
    """Leave the voice channel, if any."""
    if ctx.voice_client and ctx.voice_client.is_connected():
        #loc = os.path.join('resources', 'soundclips', 'leave')
        #sounds = make_sounds_dict(loc)
        #soundname = random.choice(list(sounds.values()))
        #sound = os.path.join(loc, soundname)
        #play_sound_file(sound, ctx.voice_client)
        #time.sleep(1)
        await ctx.guild.voice_client.disconnect()


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
######################  This and Main Stuff was taken from Ben Rucker it has been modifyed ######################
                         https://github.com/benrucker
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#Turn off
@bot.command()
async def perish(ctx):
    """Force turns me off. BERTLE ONLY"""
    if await check_perms(ctx):
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
    

@bot.event
async def on_command_error(ctx, e):
    if type(e) is commands.errors.CommandInvokeError:
        e = e.original
        if type(e) is TurtleException:
            print('Caught TurtleException: ' + str(e))
            await ctx.send(e.message)
    else:
        raise e




"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
######################  Main Stuff  ######################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



@bot.event
async def on_ready():
    #global guilds
    await bot.change_presence(activity=curr_status)

    print("Let's Do This!")


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
async def on_message(message):
    global cur_user
    global pause

    if message.content.startswith(prefix):
        print("Command!")
        print(f'{message.author.name} - {message.guild} #{message.channel}: {message.content}')

    elif message.author == bot.user:
        print("Im talking:")
        print(f'{message.author.name} - {message.guild} #{message.channel}: {message.content}')


    elif message.author == cur_user:
        await conversate(message)

    elif ("hey turtle" in message.content.lower()):
        await sendmsgorig(message,"What?!")
        cur_user = message.author
        print(cur_user)

    elif "thanks turtle" in message.content.lower(): 
        if message.author.id == bertle:
            await sendmsgorig(message, "No problem Boss!")
        else:
            await sendmsgorig(message, "Your welcome!")

    elif "please" in message.content.lower(): 
        if message.author.id == bertle:
            await sendmsgorig(message, "PRETTY PLEASE!")

    elif "hi turtle" in message.content.lower(): 
        await sendmsgorig(message, "Hello!")


    elif message.content.startswith("[] "): 
        if message.author.id == bertle:
            await sendmsgorig(message, "PRETTY PLEASE!")


    # so I can have multiple turtles running one on my laptop and one on the pi
    elif "pause running turtle" in message.content.lower(): 
        if message.author.id == bertle:
            await sendmsgorig(message, "Paused.")
            pause = True
    
    elif "play running turtle" in message.content.lower(): 
        if message.author.id == bertle:
            await sendmsgorig(message, "Playing!")
            pause = False

    elif "turtle end me" in message.content.lower(): 
        if message.author.id != bertle:
            await sendmsgorig(message, "Rocks fall. Lightning strikes. Your dead, get fucked.")
            await message.author.kick()
        else:
            await sendmsgorig(message, "Sorry Boss. Can't kill Gods.")

    elif message.content.startswith("save "):
        await sendmsg(message,"Not avalable yet.")

        #data = message.content.split('\n')
        #data = data[1:len(data)-1]
        #SaveFile('data.txt', data)


    else:
        print(message.content.split('\n'))

    #else:
    #   print(message.content)

    if not pause:
        await bot.process_commands(message)


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

    #try:
    #    os.makedirs(os.path.join('resources','soundclips','temp'))
    #except:
    #    pass
    #print(token.strip())
    #input()
    bot.run(token.strip())
