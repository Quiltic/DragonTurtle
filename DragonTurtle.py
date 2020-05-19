'''
websites used 
https://emojipedia.org/open-book/
https://cog-creators.github.io/discord-embed-sandbox/
https://leovoel.github.io/embed-visualizer/
https://en.wikipedia.org/wiki/Miscellaneous_Symbols
'''

from Tools.Tools import *
from Tools.Dice import *
from Tools.Player import *

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

deck_of_cards = {'Playing Card': ['A♤', '2♤', '3♤', '4♤', '5♤', '6♤', '7♤', '8♤', '9♤', '10♤', 'J♤', 'Q♤', 'K♤', 'A♡', '2♡', '3♡', '4♡', '5♡', '6♡', '7♡', '8♡', '9♡', '10♡', 'J♡', 'Q♡', 'K♡', 'A♢', '2♢', '3♢', '4♢', '5♢', '6♢', '7♢', '8♢', '9♢', '10♢', 'J♢', 'Q♢', 'K♢', 'A♧', '2♧', '3♧', '4♧', '5♧', '6♧', '7♧', '8♧', '9♧', '10♧', 'J♧', 'Q♧', 'K♧']}
curent_card = {'Playing Card': 0 , 'Poker': 0} # location of current cards
deck_of_cards['Poker'] = deck_of_cards['Playing Card'] * 4

#get home directory
cwd = os.getcwd()

bertle = 275002179763306517 #my id  #bot.get_user(bot.owner_id)
cur_user = 0 # the curent user that is talking to turtle
pause = False

using = Load('ActiveUsing')
if type(using) != dict:
    using = {}

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
###################### Cards Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Shuffle Shuffle
@bot.command()
async def shuffle(ctx, *deck):
    '''
    Suffles a deck of cards
    '''
    global deck_of_cards
    global curent_card
    global using

    # this idea is temparary but the end goal is to remove it based on what server you are in
    for a in using:
        try:
            using[a]['Card Hand'] = ''
        except:
            pass # no hand

    try:
        name = ''.join(deck).lower().capitalize()

        if name == '':
            name = 'Playing Card'
        elif name not in curent_card:
            name = 'No' # No deck suffled
        
        deck_of_cards[name] = shuffleDeck(deck_of_cards[name])
        curent_card[name] = 0
        await sendmsg(ctx,"{} Deck Shuffled!".format(name))
    except Exception as e:
        await sendmsg(ctx,"SHUFFLE ERROR! {}".format(e))


# SEE IM NOT CHEATING!
@bot.command()
async def showdeck(ctx, *deck):
    '''
    Shows a deck of cards
    '''
    global deck_of_cards
    global curent_card
    try:
        name = ''.join(deck).lower().capitalize()

        if name == '':
            name = 'Playing Card'
            print(deck_of_cards[name])
            #deck_of_cards = shuffleDeck(deck_of_cards)
        elif name not in curent_card:
            name = 'No' # No deck suffled

        await sendmsg(ctx,deck_of_cards[name])
        await sendmsg(ctx,"Showed {} Deck!".format(name))
    except Exception as e:
        await sendmsg(ctx,"SHOW ERROR! {}".format(e))


# Hmm yes I do have the ace of spades
@bot.command()
async def draw(ctx, amount = 1, *deck):
    '''
    "Draws" # of cards from a deck into your hand
    '''
    if amount == 'open':
        await drawopen(ctx)
        return # ends this command

    global using
    info = await cards(amount, *deck)
    try:
        using[str(ctx.author)]['Card Hand'] += ', ' + info[0] #add to the hand
    
    except KeyError:
        try:
            using[str(ctx.author)]['Card Hand'] = info[0] # no hand
        except:
            using[str(ctx.author)] = {'Card Hand': info[0]} # user dident exist
            
    except Exception as e:
        print(type(e),e)
            
        
    await sendmsgdirect(ctx, embed= info[1])


# For the lovly croud at home
@bot.command()
async def drawopen(ctx, amount = 1, *deck):
    '''
    "Draws" # of cards from a deck openly
    '''
    info = await cards(amount, *deck)
    #await sendmsg(ctx, embed= info[1]) # mostly to test
    await ctx.send(embed = info[1])
        
    
# Deck of Deck of Dek of De of Cards
async def cards(amount, *deck):
    """
    Draws the achual cards
    """
    global deck_of_cards
    global curent_card

    try:
        name = ''.join(deck).lower().capitalize()

        if type(amount) == str: # in case you give it a name instead of a value
            name = amount + name
            

        if name == '':
            name = 'Playing Card'
        elif name not in curent_card:
            name = 'No' # No deck suffled

        visuals = str(deck_of_cards[name][curent_card[name]:curent_card[name]+amount]).replace("'",'').replace('[','').replace(']','') # cleanup
        #await sendmsg(ctx,"Drew **{}**!".format(visuals))
        curent_card[name] += amount

        

        hand=discord.Embed(title="Drew from {}".format(name), description="Drew **{}**!".format(visuals))
        hand.set_footer(text="{}/{} cards left. {} drawn from deck.".format(len(deck_of_cards[name])-curent_card[name],len(deck_of_cards[name]), curent_card[name]))

        return((visuals,hand))


    except Exception as e:
        await sendmsg(ctx,"DRAW ERROR! {}".format(e))


# Readem and weep boys!
@bot.command()
async def hand(ctx):
    '''
    Shows your hand in whatever chat you use this
    '''
    global using
    
    try:
        hand = using[str(ctx.author)]['Card Hand']

        if hand == '':
            await sendmsg(ctx, "You have no hand! Use `[]draw`!")
            return
            #hand = "Nothing!"

        
        hand=discord.Embed(title="{} hand!".format(str(ctx.author)), description="Holding **{}**!".format(hand))
        await sendmsg(ctx, embed= hand)

    except KeyError:
        await sendmsg(ctx, "You have no hand! Use `[]draw`!")

    except Exception as e:
        print(e, type(e))
        await sendmsg(ctx, "Error Hand: {}".format(e))
    

# No I dont want that 2 of hearts
@bot.command()
async def discard(ctx, *cards):
    """
    Discrard ___ cards from your hand.
    """
    global using
    try:
        hand = using[str(ctx.author)]['Card Hand']

        if hand == '':
            await sendmsg(ctx, "You have no hand to discard from! Use `[]draw`!")
            return
            #hand = "Nothing!"

        # remove the cards
        for card in cards:
            print(card)
            #if ('♤' not in card) and ('♤' not in card) and('♤' not in card) and ('♡' not in card): # dont know If i want this   
            using[str(ctx.author)]['Card Hand'] = using[str(ctx.author)]['Card Hand'].replace(card,'') # its a string so we can cheeze this


        """ Cleanup """
        while '  ' in using[str(ctx.author)]['Card Hand']: # cleanup multiple spaces
            using[str(ctx.author)]['Card Hand'] = using[str(ctx.author)]['Card Hand'].replace('  ',' ') 

        while ',,' in using[str(ctx.author)]['Card Hand']: # cleanup multiple commas
            using[str(ctx.author)]['Card Hand'] = using[str(ctx.author)]['Card Hand'].replace(',,',',') 
        
        try: # if there is no string to use this with
            if (using[str(ctx.author)]['Card Hand'][-1] == ' '): # weird end spaces
                using[str(ctx.author)]['Card Hand'] = using[str(ctx.author)]['Card Hand'][:-2]

            elif (using[str(ctx.author)]['Card Hand'][-1] == ','): # weird end commas
                using[str(ctx.author)]['Card Hand'] = using[str(ctx.author)]['Card Hand'][:-1]

            
            if (using[str(ctx.author)]['Card Hand'][0] == ' '): # weard start spaces
                using[str(ctx.author)]['Card Hand'] = using[str(ctx.author)]['Card Hand'][1:]

            elif (using[str(ctx.author)]['Card Hand'][0] == ','): # weard start commas
                using[str(ctx.author)]['Card Hand'] = using[str(ctx.author)]['Card Hand'][2:]
        
        except Exception as e:
            print(e) # typicly just says ''


        # Double Check
        hand = using[str(ctx.author)]['Card Hand']
        print(type(hand), "'{}'".format(hand))
        
        if (hand == '') or (hand == ',') or (hand == ' ') or (hand == ', '): # encase I missed something
            using[str(ctx.author)]['Card Hand'] = '' # safty override
            await sendmsg(ctx, "You have no hand left! Use `[]draw`!")
            return
            #hand = "Nothing!"


        hand=discord.Embed(title="{} hand!".format(str(ctx.author)), description="Holding **{}**!".format(hand))
        await sendmsg(ctx, embed= hand)

    except KeyError:
        await sendmsg(ctx, "You have no hand to discard from! Use `[]draw`!")

    except Exception as e:
        print(e, type(e))
        await sendmsg(ctx, "Error discard: {}".format(e))



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Player Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# CASH MONY BABY! 
@bot.command()
async def gold(ctx, val = 0.0):
    """
    Change your gold count!
    []gold # 
    """
    global using

    try:
        amount = float(val)
        print(amount)


        gold = int(amount) # off the idea that gold = 1
        #print(round((amount-gold),2))
        silver = int(round((amount-gold),2)*10) # off the idea that silver = .1
        copper = int(round((amount-gold-(silver/10)),3)*100) # off the idea that copper = .01

        print(gold,silver,copper)

        try:
            using[str(ctx.author)]['Gold'] += gold
        except:
            using[str(ctx.author)]['Gold'] = gold

        try:
            using[str(ctx.author)]['Silver'] += silver
        except:
            using[str(ctx.author)]['Silver'] = silver

        try:
            using[str(ctx.author)]['Copper'] += copper
        except:
            using[str(ctx.author)]['Copper'] = copper

        #'''

        if amount != 0:
            pass
            
            cash = discord.Embed(title="{}'s Cash Money".format(using[str(ctx.author)]["Name"][:-1]), description="Gold: **{}**".format(using[str(ctx.author)]['Gold']), color=0xedd030)
            
            if using[str(ctx.author)]['Silver']:
                cash.add_field(name="Silver: `{}`".format(using[str(ctx.author)]['Silver']), value="Silver change: {} + {}".format(using[str(ctx.author)]['Silver']-silver,silver), inline=True)
            if using[str(ctx.author)]['Copper']:
                cash.add_field(name="Copper: `{}`".format(using[str(ctx.author)]['Copper']), value="Copper change: {} + {}".format(using[str(ctx.author)]['Copper']-copper,copper), inline=True)

            cash.set_footer(text="Gold Change: {} + {}".format(int(using[str(ctx.author)]['Gold'])-gold,gold))

            save_charicter(ctx,using)
            #using[str(ctx.author)]['Card Hand'] = [] # failsafe
            #Save(('Players\\'+str(ctx.author).replace('#','_').replace(' ','') + using[str(ctx.author)]['Name'].lower().replace(' ','')), using[str(ctx.author)])
            Save('ActiveUsing',using)
            
        else:
            cash = discord.Embed(title="{}'s Cash Money".format(using[str(ctx.author)]["Name"][:-1]), description="Gold: **{}**".format(using[str(ctx.author)]['Gold']), color=0xedd030)
            
            if using[str(ctx.author)]['Silver']:
                cash.add_field(name="Silver", value='`{}`'.format(using[str(ctx.author)]['Silver']), inline=True)
            if using[str(ctx.author)]['Copper']:
                cash.add_field(name="Copper", value='`{}`'.format(using[str(ctx.author)]['Copper']), inline=True)
        
        #'''
        #await sendmsg(ctx,"{} {} {}".format(gold,silver,copper))
        await sendmsg(ctx, embed=cash)

    except Exception as e:
        print(e)
        await sendmsg(ctx, "GOLD ERROR: {}".format(e))    


# Less impressive cash
@bot.command()
async def silver(ctx, val = 0.0):
    """
    Change your silver count!
    []silver # 
    """
    await gold(ctx,float(val/10))
# even less impresive cash
@bot.command()
async def copper(ctx, val = 0.0):
    """
    Change your copper count!
    []copper # 
    """
    await gold(ctx,float(val/100))


# Holy sounds
@bot.command()
async def heal(ctx, damage):
    '''
    Heal or damage
    '''
    try:
        if str(damage) == 'max': # kill
            damage = int(using[str(ctx.author)]['HP']) - int(using[str(ctx.author)]['Current HP'])

        using[str(ctx.author)]['Current HP'] = int(using[str(ctx.author)]['Current HP']) + int(damage)
        await sendmsg(ctx,"{}now has {}/{} HP".format(using[str(ctx.author)]['Name'],using[str(ctx.author)]['Current HP'],using[str(ctx.author)]['HP']))
    
    except KeyError:
        await sendmsg(ctx,"You havent taken on a character yet!")
        await sendmsg(ctx,"Do []player CHARACTER_NAME!")
        await sendmsg(ctx,"OR if you havent made a character yet do []character!")
    except Exception as e:
        await sendmsg(ctx,"Op something went wrong.")
        print('Error: ', e)

# Demonic sounds
@bot.command()
async def hurt(ctx, damage):
    '''
    Heal or damage
    '''
    try:
        if str(damage) == 'max': # kill
            damage = int(using[str(ctx.author)]['Current HP'])

        using[str(ctx.author)]['Current HP'] = int(using[str(ctx.author)]['Current HP']) - int(damage)
        await sendmsg(ctx,"{}now has {}/{} HP".format(using[str(ctx.author)]['Name'],using[str(ctx.author)]['Current HP'],using[str(ctx.author)]['HP']))
    
    except KeyError:
        await sendmsg(ctx,"You havent taken on a character yet!")
        await sendmsg(ctx,"Do []player CHARACTER_NAME!")
        await sendmsg(ctx,"OR if you havent made a character yet do []character!")
    except Exception as e:
        await sendmsg(ctx,"Op something went wrong.")
        print('Error: ', e)


# Newby huh?
@bot.command()
async def character(ctx, *args):
    info = {'Spell Save': 10, 'Proficiency': 1,'Spell Attack': 1,'Name': 'NAMELESS', 'URL': None, 'AC': 10, 'Alignment': 'Unaligned', 'CHA': 10, 'CON': 10, 'Challenge Rating': 0, 'DEX': 10, 'HP': 10, 'INT': 10, 'Passive Perception': 10, 'STR': 10, 'Total Level': 1, 'Skills': 'Perception, Stealth', 'Speed': '30ft', 'Main Class': 'Fighter', 'WIS': 10,'Expertise': '__'}
    print('start')
    magic = {"monk":'wis',"rogue":'INT',"fighter":'INT',"warlock":'CHA','wizard': 'INT', 'druid': 'WIS', 'sorcerer': 'CHA', 'bard': 'CHA', 'paladin': 'CHA', 'ranger': 'WIS', 'artificer': 'INT', 'cleric': 'WIS'}
    try:
        if len(args) == 0: # basic help
            stuff = """```\n[]character |Name: __\n|Main Class: __\n|Total Level: __\n|AC: __\n|HP: __\n|Speed: __ft\n|STR: __\n|DEX: __\n|CON: __\n|INT: __\n|WIS: __\n|CHA: __\n|Skills: __\n|Expertise: __\n|URL: __```"""
            await sendmsg(ctx,stuff)
            await sendmsg(ctx,"Copy the above then replace __ and send back") # with []player
            await sendmsg(ctx,"**If you dont have anything for that slot leave it blank __(EXCEPT NAME!!)__**")
            #await sendmsg(ctx,"Leaving __ will result with its default")

        elif len(args) == 1:
            info = Load(('Players\\'+str(ctx.author).replace('#','_').replace(' ','') + args[0].lower().replace(' ','')))

            spl=discord.Embed(title=info['Name'], url=info['URL'], description="{}{}: {}".format(info['Main Class'],info['Total Level'],info['Alignment']), color=0x25ae11)
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
            #print(info)
            try:
                print("Old Save")
                info = Load(('Players\\'+str(ctx.author).replace('#','_').replace(' ','') + args[0].lower().replace(' ','')))
                data = make_charicter(ctx, *args)
                for stuff in data:
                    if stuff != 'hand':
                        info[stuff] = data[stuff] 
                #save char
                Save(('Players\\'+str(ctx.author).replace('#','_').replace(' ','') + info['Name'].lower().replace(' ','')), info)
            except Exception as e:
                print(e)
                info = make_charicter(ctx, *args)
                #save char
                print("New Save")
                Save(('Players\\'+str(ctx.author).replace('#','_').replace(' ','') + info['Name'].lower().replace(' ','')), info)
            await sendmsg(ctx,"Created Charicter Save.")
            await player(ctx,info['Name'])

    except Exception as e:
        await sendmsg(ctx,"Op something went wrong.")
        print('Error: ', e)
            
        #print(*args)
        

# SUP IM NASND
@bot.command()
async def player(ctx, *args):
    global using
    if len(args) != 0:
        if args[0] == 'update':
            try:
                stuff = """```\n[]character |Name: {}\n|Main Class: {}\n|Total Level: {}\n|AC: {}\n|HP: {}\n|Speed: {}\n|STR: {}\n|DEX: {}\n|CON: {}\n|INT: {}\n|WIS: {}\n|CHA: {}\n|Skills: {}\n|Expertise: {}\n|URL: {}```""".format(using[str(ctx.author)]['Name'][:-1],using[str(ctx.author)]['Main Class'][:-1],using[str(ctx.author)]['Total Level'][:-1],using[str(ctx.author)]['AC'][:-1],using[str(ctx.author)]['HP'][:-1],using[str(ctx.author)]['Speed'][:-1],using[str(ctx.author)]['STR'][:-1],using[str(ctx.author)]['DEX'][:-1],using[str(ctx.author)]['CON'][:-1],using[str(ctx.author)]['INT'][:-1],using[str(ctx.author)]['WIS'][:-1],using[str(ctx.author)]['CHA'][:-1],using[str(ctx.author)]['Skills Prof'][:-2],using[str(ctx.author)]['Skills Expertise'][:-2],using[str(ctx.author)]['URL'])
                await sendmsg(ctx,stuff)
                await sendmsg(ctx,"Copy the above update it and send back") # with []player
            except:
                stuff = """```\n[]character |Name: {}\n|Main Class: {}\n|Total Level: {}\n|AC: {}\n|HP: {}\n|Speed: {}\n|STR: {}\n|DEX: {}\n|CON: {}\n|INT: {}\n|WIS: {}\n|CHA: {}\n|Skills: {}\n|Expertise: {}\n|URL: {}```""".format(using[str(ctx.author)]['Name'][:-1],using[str(ctx.author)]['Main Class'][:-1],using[str(ctx.author)]['Total Level'][:-1],using[str(ctx.author)]['AC'][:-1],using[str(ctx.author)]['HP'][:-1],using[str(ctx.author)]['Speed'][:-1],using[str(ctx.author)]['STR'][:-1],using[str(ctx.author)]['DEX'][:-1],using[str(ctx.author)]['CON'][:-1],using[str(ctx.author)]['INT'][:-1],using[str(ctx.author)]['WIS'][:-1],using[str(ctx.author)]['CHA'][:-1],using[str(ctx.author)]['Skills Prof'][:-2],"__",using[str(ctx.author)]['URL'])
                await sendmsg(ctx,stuff)
                await sendmsg(ctx,"Copy the above update it and send back") # with []player
        else:
            try:
                try:
                    if ''.join(args).lower().replace(' ','') != using[str(ctx.author)]['Name'].lower().replace(' ',''):
                        save_charicter(ctx,using)
                        #using[str(ctx.author)]['Card Hand'] = [] # failsafe
                        #Save(('Players\\'+str(ctx.author).replace('#','_').replace(' ','') + using[str(ctx.author)]['Name'].lower().replace(' ','')), using[str(ctx.author)])
                except:
                    pass
                
                # Failsafe
                try:
                    if type(using[str(ctx.author)]) != dict:
                        using[str(ctx.author)] = {}
                except:
                    pass

                using[str(ctx.author)] = Load('Players\\'+str(ctx.author).replace('#','_').replace(' ','') + ''.join(args).lower().replace(' ',''))
                await sendmsg(ctx,"Linked!")

                Save('ActiveUsing',using)
            except Exception as e:
                await sendmsg(ctx,"Linking Error: {}".format(e))
                print(e)
                
    else:
        try:
            await character(ctx,using[str(ctx.author)]['Name'])
            
        except KeyError:
            await sendmsg(ctx,"You havent taken on a character yet!")
            await sendmsg(ctx,"Do []player CHARACTER_NAME!")
            await sendmsg(ctx,"OR if you havent made a character yet do []character!")
        except Exception as e:
            await sendmsg(ctx,"Op something went wrong.")
            print(type(e), e)
            
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Dice Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# How do you dodge a FIREBALL!
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
    

# Check. Your turn
@bot.command()
async def check(ctx, *stuff):
    '''
    Make a ___ check
    '''
    await r(ctx, *stuff)


# IM FAST AS #*$& BOIIII
@bot.command()
async def init(ctx, *args):
    '''
    Initiative
    '''
    try:    
        thing = '+' + str(using[str(ctx.author)]['Initiative'])
        print(thing)
        stuff = diceBase(thing)
        stuff['speak'] = quick_combiner(stuff)
        #await roll(ctx,(thing))


        embed=discord.Embed(title="{} Init!".format(using[str(ctx.author)]['Name']), color=0xe33604)
        embed.add_field(name=stuff['speak'].replace('[1]','[**1**]').replace('[20]','[**20**]'), value='**Total**: `'+ str(stuff['total']) + '`', inline=False)

        await sendmsg(ctx, embed= embed) # send msg

        #print(stuff["Total"])
        try:
            using[ctx.guild.name]['init'] += [ctx.author,stuff["total"]]
        except:
            using[ctx.guild.name] = {'init': [[ctx.author,stuff["total"]]]}
        #await sendmsg(ctx,"{} now has {}/{} HP".format(using[str(ctx.author)]['Name'],using[str(ctx.author)]['Current HP'],using[str(ctx.author)]['HP']))
    
    except KeyError as e:
        print(e)
        await sendmsg(ctx,"You havent taken on a character yet!")
        await sendmsg(ctx,"Do []player CHARACTER_NAME!")
        await sendmsg(ctx,"OR if you havent made a character yet do []character!")
    except Exception as e:
        await sendmsg(ctx,"Op something went wrong.")
        print(type(e), e)




@bot.command()
async def customroll(ctx, *args):
    '''
    Create custom rolls and tables
    '''
    await cr(ctx,*args)


@bot.command()
async def cr(ctx, *args):
    '''
    Create custom rolls and tables
    '''
    global using
    if len(args) != 0:
        if args[0] == 'update':
            # If global____ is name then it will remove the global and give all users acsess to it 
            stuff = """```\n[]customroll |Name: {}\n|Main Roll: {}\n|Second Roll: {}\n|Table info:\n```""".format(using[str(ctx.author)]['Name'][:-1], using[str(ctx.author)]['Main'][:-1], using[str(ctx.author)]['Second'][:-1], using[str(ctx.author)]['Table'][:-1])
            await sendmsg(ctx,stuff)
            await sendmsg(ctx,"Copy the above update it and send back") # with []player
        else:
            for a in using[str(ctx.author)]['Rolls']:
                print(a) 
            
            try:
                custRoll = CustomRollMaker(ctx,*args)
                try:
                    #savename = using[str(ctx.author)]['Name'] + custRoll['Name'][:-1]
                    #savename = custRoll['Name']
                    
                    try:
                        using[str(ctx.author)]['Rolls'][custRoll['Name']] = custRoll
                    except:
                        using[str(ctx.author)]['Rolls'] = {custRoll['Name']: custRoll}

                    save_charicter(ctx,using)
                    #Save(('Players\\'+str(ctx.author).replace('#','_').replace(' ','') + using[str(ctx.author)]['Name'].lower().replace(' ','')), using[str(ctx.author)])
                    Save('ActiveUsing',using)
                except:
                    await sendmsg(ctx,"You havent taken on a character yet!")
                    await sendmsg(ctx,"Do []player CHARACTER_NAME!")
                    await sendmsg(ctx,"OR if you havent made a character yet do []character!")
                

            except Exception as e:
                await sendmsg(ctx,"Custom roll Error: {}, {}".format(type(e),e))
                print(e)
                
    else:
        try:
            stuff = """```\n[]customroll |Name: __\n|Main Roll: __\n|Second Roll: __\n|Table info (do * # DOES):\n* __ __```"""
            
            await sendmsg(ctx,stuff)
            await sendmsg(ctx,"Copy the above then replace __ and send back") # with []player
            await sendmsg(ctx,"If you dont have anything for that slot leave it blank (EXCEPT NAME!!)")
            await sendmsg(ctx,"For the table put it inside a code block **```**.")
            await sendmsg(ctx,"Table rolls are done off the Second Roll")
            await sendmsg(ctx,"For rolls inside the table put it inside two **`**.")

        except Exception as e:
            await sendmsg(ctx,"Op something went wrong.")
            print('Error: ', e)

    await sendmsg(ctx,"Roll {} Made".format(custRoll['Name']))



# R's older brother
@bot.command()
async def roll(ctx, *args):
    await r(ctx, *args)


# Snake eyes!
@bot.command()
async def r(ctx, *args):
    """This rolls a # of dice and gives the output. Usage: []r 1d4 +4"""
    global using
    await ctx.message.add_reaction("🎲")

    try:
        things = await bitReplacer(ctx, using, *args)
        if things == None:
            await sendmsg(ctx,"Improper skill name!")

    except KeyError:
        await sendmsg(ctx,"Improper skill name! {}".format(args))
    except Exception as e:
        print(e)


    print(things)

    try:
        stuff = diceBase(*things) # this is the raw data
    except Exception as e:
        await sendmsg(ctx,"Roll Error: {}".format(e))
    #await sendmsg(ctx,data)
    stuff['speak'] = '**Rolled:**'

    if 'try1' in stuff: # adv or disadv
        stuff['speak'] = quick_combiner(stuff['try1'])
        '''
        for a in stuff['try1']:
            if (a != 'total') and (a != 'speak'):
                stuff['speak'] += ' ' + a 
                if 'd' in a:
                    stuff['speak'] += ' ' + str(stuff['try1'][a])
        #'''

        stuff['speak'] += ' &'

        stuff['speak'] += quick_combiner(stuff['try2'])
        '''
        for a in stuff['try2']:
            if (a != 'total') and (a != 'speak'):
                stuff['speak'] += ' ' + a 
                if 'd' in a:
                    stuff['speak'] += ' ' + str(stuff['try2'][a])
        #'''

    else:
        stuff['speak'] = quick_combiner(stuff)
        '''
        for a in stuff:
            if (a != 'total') and (a != 'speak'):
                stuff['speak'] += ' ' + a 
                if 'd' in a:
                    stuff['speak'] += ' ' + str(stuff[a])
        #'''

    #stuff['speak'] = diceCleanup(stuff)
    print(stuff['speak'])
    try:
        embed=discord.Embed(title="{} Rolls".format(using[str(ctx.author)]['Name']), color=0xe33604)
    except:
        embed=discord.Embed(title="{} Rolls".format(ctx.author), color=0xe33604)

    embed.add_field(name=stuff['speak'].replace('[1]','[**1**]').replace('[20]','[**20**]'), value='**Total**: `'+ str(stuff['total']) + '`', inline=False)
    

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


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Spell Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@bot.command()
async def cast(ctx, *spell):
    '''
    Cast a spell with all the pirks of casting.
    '''
    try:
        upcharge = int(spell[-1])
        spell = spell[:-1]
        print(upcharge)
    except Exception as e:
        #print(e)
        upcharge = 0

    spell = ' '.join(spell).lower()

    async with ctx.channel.typing():
        await ctx.message.add_reaction("📖")
        #await sendmsg(ctx,"Refactoring spell list")

        #reloadSpellList()
        data = SpellBook(spell) # get spell
        if (data != None) and (data != 'None'):
            try:
                data['fight'] = offenceSpell(data) # upcast
            except Exception as e:
                print('Error Get fight: {}'.format(data))
                await sendmsg(ctx,'Error Get fight: {}'.format(data))
            
            try:
                # if you need to roll to hit
                if data['fight']['type'] != 'area':
                    hitstuff = diceBase(*('+'+str(using[str(ctx.author)]['Spell Attack']))) # damage roll
                    say = quick_combiner(hitstuff) # cleanup
                    spl=discord.Embed(title=data['name'], url=data['url'], description="**Rolled To Hit:** {} = `{}`".format(say,hitstuff['total']), color=0x07a7af)
                else:
                    spl=discord.Embed(title=data['name'], url=data['url'], description="School: {}".format(data['school']), color=0x07a7af)

                '''
                UPCASTING!
                ITS ACHUAL HELL!
                DONT LOOK TO HARD
                '''
                try:
                    if len(data['fight']['damage']):
                        if data['cast']['level'] == 'Cantrip':
                            if data['fight']['damage'][-1][0][data['fight']['damage'][-1][0].index('d'):] == data['fight']['higherLvl'][data['fight']['higherLvl'].index('d'):]:
                                increase = int(data['fight']['higherLvl'][:data['fight']['higherLvl'].index('d')]) * math.floor((int(using[str(ctx.author)]['Total Level'])+1)/6) # ups at lvl 5, 11, & 17 so this does the charm
                                #print(int(data['fight']['damage'][-1][0][:data['fight']['damage'][-1][0].index('d')]),int(data['fight']['higherLvl'][:data['fight']['higherLvl'].index('d')])*(upcharge-int(data['cast']['level'])))
                                data['fight']['damage'][-1][0] = str(int(data['fight']['damage'][-1][0][:data['fight']['damage'][-1][0].index('d')]) + increase) + data['fight']['damage'][-1][0][data['fight']['damage'][-1][0].index('d'):]

                        elif upcharge > int(data['cast']['level']):
                            print(data['fight']['damage'][-1][0][data['fight']['damage'][-1][0].index('d'):],data['fight']['higherLvl'][data['fight']['higherLvl'].index('d'):])
                            if data['fight']['damage'][-1][0][data['fight']['damage'][-1][0].index('d'):].replace('O','0') == data['fight']['higherLvl'][data['fight']['higherLvl'].index('d'):].replace('O','0'):
                                #print(int(data['fight']['damage'][-1][0][:data['fight']['damage'][-1][0].index('d')]),int(data['fight']['higherLvl'][:data['fight']['higherLvl'].index('d')])*(upcharge-int(data['cast']['level'])))
                                data['fight']['damage'][-1][0] = str(int(data['fight']['damage'][-1][0][:data['fight']['damage'][-1][0].index('d')].replace('O','0')) + int(data['fight']['higherLvl'][:data['fight']['higherLvl'].index('d')].replace('O','0'))*(upcharge-int(data['cast']['level']))) + data['fight']['damage'][-1][0][data['fight']['damage'][-1][0].index('d'):]
                            #data['fight']['damage'][-1] will be increased?
                except:
                    pass


                # damage
                dmg = 0 # total damage
                for damage in data['fight']['damage']: # for each type of damage
                    try:
                        stuff = diceBase(*damage[0]) # this is the raw data
                        dmg += stuff['total']
                    
                        try:
                            say = quick_combiner(stuff)
                            spl.add_field(name="**Rolled:** {}".format(say), value='`' + str(stuff['total'])+ '` ' + damage[1] + ' damage', inline=True)
                        except IndexError:
                            say = quick_combiner(stuff)
                            spl.add_field(name="**Rolled:** {}".format(say), value='`' + str(stuff['total'])+ '` ' + '___ damage', inline=True)
                        except Exception as e:
                            await sendmsg(ctx,"Type Damage Error: {}".format(e))
                            
                    except Exception as e:
                        await sendmsg(ctx,"Damage Error: {}".format(e))
                    

                if dmg > 0: # dont need this if no damage
                    spl.add_field(name='Ouch.', value="**Total:** `{}` damage.".format(dmg), inline=False)
                    spl.description +='\nType: {}'.format(data['fight']['type'])


                # if there is a type of save
                if data['fight']['save']:
                    spl.description +='\nType Save: {}\nSave: `{}`'.format(data['fight']['save'],using[str(ctx.author)]['Spell Save'])
                

                # what do
                if len(data['does']) < 1000:
                    spl.add_field(name="What Do", value=data['does'].replace('|n','\n'), inline=False)
                else:
                    spl.add_field(name="What Do", value=(data['does'][:1000]).replace('|n','\n'), inline=False)
               

                if data['cast']['level'] != 'Cantrip': # CANTRIPS
                    spl.set_footer(text="Cast at level {}".format(max(int(data['cast']['level']),upcharge)))
                else:
                    spl.set_footer(text="Cast at level {}".format(data['cast']['level']))

                await ctx.send(embed = spl)

            except Exception as e:
                await sendmsg(ctx,'Cast Error: {}'.format(e))

        else:
            await sendmsg(ctx,"Cant get spell: {}".format(spell))



# spells
@bot.command()
async def spell(ctx, *spell):
    """This finds and gives a spell. Usage: []spell fireball"""

    spell = ' '.join(spell).lower()

    if spell == '':
        await sendmsg(ctx, "Here is my Source Spellbook: https://www.dnd-spells.com/spell")

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


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Monster Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


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
            spl.add_field(name="STR", value=Monster['STR'], inline=True)
            spl.add_field(name="DEX", value=Monster['DEX'], inline=True)
            spl.add_field(name="CON", value=Monster['CON'], inline=True)
            spl.add_field(name="INT", value=Monster['INT'], inline=True)
            spl.add_field(name="WIS", value=Monster['WIS'], inline=True)
            spl.add_field(name="CHA", value=Monster['CHA'], inline=True)
            #spl.add_field(name="STR DEX CON INT WIS CHA", value="  {}  {}  {}  {}  {}  {}".format(Monster['STR'],Monster['DEX'],Monster['CON'],Monster['INT'],Monster['WIS'],Monster['CHA']), inline=False)
            spl.set_footer(text="Challenge Rating: {}".format(Monster['Challenge Rating']))
            await ctx.send(embed = spl)
        
        print(Monster)
        #'''


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Custom Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@bot.command()
async def chaos(ctx):
    """
    Good luck.
    """
    await sendmsg(ctx,'THIS ISENT NOT DONE YET!')

    # 1 SMITE!
    # 2 Screem
    # 3 server dephin '60 seconds'
    # 4 server mute '60 seconds'
    # 5 Put into the Corner '
    # 6 Gives Stinky roll
    # 7 You HAD admin 'troll' 'after 4 seconds'
    # 8 THIS ISENT DONE YET! 'line'
    # 9 ROCKS FALL! LIGHTNING STRIKES! YOUR DEAD GET FUCKED! 'direct message'
    # 10 Eah could have been better or worse 'line'
    # 11 Eah could have been better or worse 'line'
    # 12 Huh... neat 'line'
    # 13 Countdown started 'line'
    # 14 So I know what your doing your going mad 'line'
    # 15 Er. No, sorry. 'line'
    # 16 Buy yourself something nice 'line'
    # 17 Here have a sandwitch
    # 18 gives golden roll
    # 19 So CLose. Heres a cookie 'cookie'
    # 20 You have ADMIN! 'for one second'
    


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
        msg = "🐉"
        rand = randomnum(100,200)
        for a in range(rand):
            msg = msg + "🐉"
        await sendmsgorig(message, msg)
        msg = "I was able to get " + str(rand) + " Dragons for the cause!"
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
    # await message.author.send(files=help_files,embed=helpEmbed) # Etan's Help Method
    # await message.add_reaction("✉") # Etan's Help Method
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

    elif "smite" in message.content.lower(): 
        await sendmsgorig(message, "⚡**SMITE!**⚡")

    elif "please" in message.content.lower(): 
        if message.author.id == bertle:
            await sendmsgorig(message, "PRETTY PLEASE!")

    elif "hi turtle" in message.content.lower(): 
        await sendmsgorig(message, "Hello!")

    elif "fuck you" in message.content.lower(): 
        await sendmsgorig(message, "Well ok then.")

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
