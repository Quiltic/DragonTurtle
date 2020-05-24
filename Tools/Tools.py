#this file is literaly just to clean up the main file


#this is so that the IDE doesent yell at me for not having this in the file. Yes its that annoying
if __name__ == "__main__":
    #import os, subprocess, random, asyncio
    import discord
    from discord.ext import commands
    bot = commands.Bot(";")
    bertle = 275002179763306517


#all of the needed imports
import asyncio, subprocess
import time, random, os, sys, requests, math
from datetime import datetime


# beauty soup
try:
    from bs4 import BeautifulSoup
except:
    import os
    os.system("python3 -m pip install beautifulsoup4")
    from bs4 import BeautifulSoup

# jtools
try:
    from JTools import find_all, Load, Save #, flattenList, cutUp
except:
    import os
    os.system("python3 -m pip install git+https://github.com/Quiltic/JTools.git")
    from JTools import find_all, Load, Save #, flattenList, cutUp

#from Tools.MonsterFinder import *
#from Tools.SpellFinder import *
#deck_of_cards = ['A♤', '2♤', '3♤', '4♤', '5♤', '6♤', '7♤', '8♤', '9♤', '10♤', 'J♤', 'Q♤', 'K♤', 'A♡', '2♡', '3♡', '4♡', '5♡', '6♡', '7♡', '8♡', '9♡', '10♡', 'J♡', 'Q♡', 'K♡', 'A♢', '2♢', '3♢', '4♢', '5♢', '6♢', '7♢', '8♢', '9♢', '10♢', 'J♢', 'Q♢', 'K♢', 'A♧', '2♧', '3♧', '4♧', '5♧', '6♧', '7♧', '8♧', '9♧', '10♧', 'J♧', 'Q♧', 'K♧']

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### D&D Tools ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#import Tools.Player

'''
# This is anchent and not to be destrbed
async def dice(Start, *args):
    #print(args) 
    msg = args # achual requested values
    Message = '' # words to be spoken
    Total = [] # grand total

    if len(msg) == 0: # want a flat d20
        Total = randomnum(1,20)
        Message = 'd20: {}'.format(Total)
        return((Message, Total))

    elif len(msg) == 1: # individualised

        msg = msg[0] # cleanup

        #if Start == False: # achualy print what we need kinda dirpy but whatever
        if 'd' in msg: # for dice
            stuff = msg.split('d') # core of thing

            mult = 1 # mult for numbers
            if '-' in stuff[0]:
                mult = -1

            stuff[0] = int(stuff[0].replace('+','').replace('-','')) # dont want + or -

            if len(msg) > 10: # insane number protection to a point
                Total += [mult*randomnum(stuff[0],int(stuff[1])*stuff[0])]
            else:
                Total += [mult*randomnum(1,int(stuff[1])) for _ in range(stuff[0])] # rolls

            Message = ' '.join(['{} +'.format(roll) for roll in Total]) # so we know it is rolling stuff kinda important
            #print(Total)
            if Start: # if its the first and only numbers
                if (msg[0] == '+') or (msg[0] == '-'): # []r +1d6
                    Total = [randomnum(1,20)] + Total
                    Message = str(Total[0]) + ' + '+ Message

                Message = 'Dicerolls: {} = {}'.format(Message[:-1], sum(Total)) # cleanup

            return((Message,Total))

        else: # -# or +#
            args = (' '.join(args)).lower().replace('+  ','+').replace('-  ','-').split(' ')
            msg = msg.replace('+','')

            if Start: # no dice would have been rolled yet
                Total = randomnum(1,20)
                Message = 'd20: {} + {} = {}'.format(str(Total), msg, Total+ int(msg)) # cleanup
                return((Message,Total+ int(msg)))

            #print((msg+' ',[int(msg)]))
            return((msg+' ',[int(msg)])) # the ' ' is there for cleanup

    else:
        #print(msg)
        for a in msg: # individual things
            val = await dice(False, a)
            Message += ' ' + val[0]
            Total += val[1]


    #print('Message ' + Message)
    if Message[0] != 'd': # safty net
        Message = 'Dicerolls: {} = {}'.format(Message[:-1], sum(Total)) # cleanup
    
    return((Message, sum(Total)))


def make_charicter(ctx, *args):
    skills = {'dexterity': 'DEX','wisdom':'WIS','intelligence':'INT','strength':'STR','constitution':'CON','charisma':'CHA',  'acrobatics': 'DEX','animalhandling':'WIS','arcana':'INT','athletics':'STR','deception':'CHA','history':'INT','insight':'WIS','intimidation':'CHA','investigation':'INT','medicine':'WIS','nature':'INT','perception':'WIS','performance':'CHA','persuasion':'CHA','religion':'INT','sleightofhand': 'DEX','stealth': 'DEX','survival':'WIS'}
    info = {'Current HP': 10,'Spell Save': 10, 'Proficiency': 1,'Spell Attack': 1,'Name': 'NAMELESS', 'URL': 'https://www.dungeonmastersvault.com/pages/dnd/5e/character-builder', 'AC': 10, 'Alignment': 'Unaligned', 'CHA': 10, 'CON': 10, 'Challenge Rating': 0, 'DEX': 10, 'HP': 10, 'INT': 10, 'Passive Perception': 10, 'STR': 10, 'Total Level': '1 ', 'Speed': '30ft', 'Main Class': 'Fighter', 'WIS': 10, 'Skills Prof': 'survival','Skills':[]}
    #print('start')
    magic = {"monk":'wis',"rogue":'INT',"fighter":'INT',"warlock":'CHA','wizard': 'INT', 'druid': 'WIS', 'sorcerer': 'CHA', 'bard': 'CHA', 'paladin': 'CHA', 'ranger': 'WIS', 'artificer': 'INT', 'cleric': 'WIS'}
    
    msg = ' '.join(args).split('|')[1:]
    #print(msg)
    for a in msg:
        #print(a)
        splt = a.index(': ')
        #print(a[:splt], a[splt+2:])
        if (a[splt+2:] != '__') and (a[splt+2:] != '___'):
            info[a[:splt]] = a[splt+2:]

    info['Current HP'] = int(info['HP'])
    info['Skills Prof'] = info['Skills']
    print(info['Skills Prof'])

    info['Proficiency'] = math.floor(int(info['Total Level'][:-1])/5)+2
    
    #val = int(info[magic[info['Main Class'][:-1].lower()]][:-1])
    #val = math.floor((val-10)/2)
    #print(val)

    # spell stuff
    val = get_modifyer(info,magic[info['Main Class'][:-1].lower()]) # the casting mod type for the player
    info['Spell Save'] = 8 + info['Proficiency'] + val
    info['Spell Attack'] = info['Proficiency'] + val

    # init
    info['Initiative'] = get_modifyer(info,'DEX')

    # skills
    for a in skills:
        skills[a] = get_modifyer(info,skills[a])

    info['Skills Prof'] += ','
    for a in info['Skills Prof'].split(','):
        if a != '':
            skills[a.replace(' ','').lower()] += info['Proficiency']
    print(skills)      
    info['Skills'] = skills

    #save char
    Save(('Players\\'+str(ctx.author).replace('#','_').replace(' ','') + info['Name'].lower().replace(' ','')), info)
    return(info)
    

def get_modifyer(main, typ):
    # Gives the modifyer
    val = int(main[typ][:-1])
    val = math.floor((val-10)/2)
    return(val)


'''
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Cards Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def shuffleDeck(deck, times = 4, amount = -1):
    '''
    suffles a deck
    shuffle(deck, times = 4, amount = 20) : gives a deck randomly suffled
    shuffle(deck, 6) better shuffle
    shuffle(deck, 12, 40) insane shuffle
    '''
    if amount < 0:
        amount = int(len(deck)/2)
    cards = list(deck) # clone
    #print(cards)
    for _ in range(times):
        for _ in range(amount):
            point = randomnum(0,len(cards)-1) # card 1 location
            difpoint = randomnum(0,len(cards)-1) # card 2 location
            difcard = cards[point] # card holder
            cards[point] = cards[difpoint] # swap card 1
            cards[difpoint] = difcard # swap card 2
    
    #print(cards)
    return(cards)



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Monster Tools ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#
def findMonster(NAME = 'Dragon turtle'):
    '''
    Given a name it will give you basics on a monster and a url to its page
    findMonster(NAME = 'Dragon turtle'): gives basic stats and a url (dict)
    '''
    name = NAME.lower().replace(' ','%20') # no spaces only %20
    url = "https://roll20.net/compendium/dnd5e/"+name # url
    r  = requests.get(url) # get info
    data = r.text # get data
    soup = BeautifulSoup(data,features="lxml") # soup

    # this is if it is not appart of the normal stuff or non existant
    if ('You do not own' in str(soup)):
        print("Cant get creature: link given.")
        return(url)
    elif 'Page Not Found' in str(soup):
        print('Not found.')
        return(None)
    
    # proper looking name
    name = soup.find('h1',{'class':'page-title'}).get_text().replace('\n','').replace('\t','')

    # achual info lies
    top = soup.find('div',{"class":"col-md-12 attrList"})
    stuff = top.find_all('div')

    # basicly this does all the work it is in an unusual div structure but makes this work nicely
    Monster = {'Name': name,'url': url}
    for a in range(1,len(stuff)-1,4):
        Monster[stuff[a].get_text()] = stuff[a+1].get_text().replace('\n',' ').replace(' + ','+')

    
    return(Monster)


#
def cleanPrintM(Monster):
    '''
    Prints out basic monster stuff
    cleanPrint(Monster): gives true or error: prints data/url
    '''
    if type(Monster) == str:
        print('Not found. Go to: {}'.format(Monster['url']))
        return('Not found. Go to: {}'.format(Monster['url']))
    elif Monster == None:
        print('Not found. No page.')
        return('Not found. No page.')
    print('For more go to: {}'.format(Monster['url']))
    
    
    print(Monster['Name'])
    print(Monster['Size']+Monster['Type']+':'+Monster['Alignment'])
    print()

    print('AC:'+Monster['AC'])
    print('HP:'+Monster['HP'])
    print('Speed:'+Monster['Speed'])
    print()

    print('STR','DEX','CON','INT','WIS','CHA')
    print(Monster['STR']+Monster['DEX']+Monster['CON']+Monster['INT']+Monster['WIS']+Monster['CHA'])
    print()

    # some have this some dont
    #print('Saving Throws:'+Monster['Saving Throws'])
    #print('Resistances:'+Monster['Resistances'])
    #print('Senses:'+Monster['Senses'])
    #print('Languages:'+Monster['Languages'])
    
    print('Challenge Rating:'+Monster['Challenge Rating'])
    print()
    print('For more go to: {}'.format(Monster['url']))
    return(True) # worked

    

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Spell Tools ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# damage damage damage
def offenceSpell(spell):
    '''
    Given a spell (dict) it will try to give you its damage and other helpfull bits relting to casting a damage spell
    '''
    offencive = {'damage':[], 'type':'area', 'save':None, 'higherLvl':None}

    try:
        # get the damages and there types cold lightning pearcing ect
        places = find_all(spell['does'],'take')
        for a in places:
            p1 = spell['does'][a:].index(' ') # could be takes witch would leave an s
            p2 = spell['does'][a:].index(' damage')
            if len(spell['does'][a+p1+1:p2+a].split(' ')[0]) <= 5:
                offencive['damage'] += [spell['does'][a+p1+1:p2+a].split(' ')]
    except ValueError:
        #print('area?')
        pass
    except Exception as e:
        print('Spell attack error: {}'.format(e))



    try:
        # get the type of spell ie ranged melee something else
        place = spell['does'].index('spell attack') # not achualy needed
        offencive['type'] = 'ranged' if 'ranged' in spell['does'][:place] else 'melee' if 'melee' in spell['does'][:place] else 'NO IDEA'
        #print(tpe)
    except ValueError:
        #print('area?')
        pass
    except Exception as e:
        print('Spell attack error: {}'.format(e))


    try:
        # if it has a saving through
        place = spell['does'].index(' saving throw')
        offencive['save'] = spell['does'][find_all(spell['does'][:place],' ')[-1]+1:place]
    except ValueError:
        #print('no save')
        pass
    except Exception as e:
        print('Save throw error: {}'.format(e))

    try:
        # upgrades
        place = spell['does'].index("damage increases by ")
        #print(place+13,spell['does'][place+13:].index(' ')+place+13)
        offencive['higherLvl'] = spell['does'][place+20:spell['does'][place+20:].index(' ')+place+20].replace(',','') # +13 is from "increases by "
    except ValueError:
        #print('no save')
        pass
    except Exception as e:
        print('Save throw error: {}'.format(e))


    print(offencive)
    return(offencive)


# bread and butter of file. Gets spells 
def findSpell(spellname):
    '''
    Finds a spell from https://www.dnd-spells.com/spell and makes it into a dict
    findSpell(spellname): gives a dict or None if no spell is found
    findSpell("mage hand"): gives dict on magehand
    '''

    spellname = spellname.lower().replace(' ','-') # spells get put into the website as first-last (No spaces no caps)
    print("Spell Name {}".format(spellname))
    url = "https://www.dnd-spells.com/spell/"+spellname # get url
    r  = requests.get(url) # get data from url
    print(f"Has request: {r != None}")

    data = r.text # makes a nice text stuff
    soup = BeautifulSoup(data,features="lxml") # maks a soup
    if "No such spell, try again" in str(soup): # wasent a spell
        if 'ritual' in spellname: # rituals have this tag included
            return(None) # not spelled correctly or doesent exist
        return(findSpell(spellname+' ritual')) # try again as a ritual


    div = soup.find_all("div") # gives all the divs
    print(f"Div Amount: {len(div)}")

    Spell = {} # spell base

    home = div[20].find_all("div")[0] # get the spells sorce from website
    print(f"Home {home}")

    #spells name
    name = str(home.find('h1')) # gets name of spell in nice format
    name = name[name.find('span>')+5:name.find('</span')] # cleanup
    Spell['name'] = name # save
    print(f"Name: {name}")

    # this is all the achual info that we want
    stuff = home.find_all('p')

    school = str(stuff[0])[3:-4] # gives the school its apart of
    Spell['school'] = school
    print(f"School: {school}")

    # information for the casting
    casting_stuff = str(stuff[1])[5:-5].replace('        ','') # cleanup
    casting_stuff = casting_stuff.replace('<strong>','').replace('</strong>','').replace('<br/>','') # remove bold and other fluff
    casting_stuff = casting_stuff.split('\r\n') # get each as own thing
    cast = {} 
    for a in casting_stuff:
        loc = a.index(':') # gives the tipical info
        cast[a[:loc].lower()] = a[loc+2:-1] 

    Spell['cast'] = cast
    print(f"CASTSTUFF {cast}")


    # gets wonky from here because sometimes there is a higher lvl spell stuff
    clean = str(stuff[2]).replace('\n','|n') # SAVE THE NEWLINES!
    clean = ' '.join(clean.split()) # weird spaces exist so this just removes them 
    what_do = str(clean)[4:-5].replace('<br/>','').replace('        ','')# what the spell do # cleanup
    
    # this is if there is a hihger lvl section
    segment = 0 # we need to shunt down the next stuff to move correct for this section
    if ('At higher level' in str(home)):
        segment = 1
        what_do += str(stuff[3])[5:-5].replace('<br/>','').replace('        ','')# what the spell do continued
    
    what_do = what_do.replace('’',"'").replace('•','*').replace('–','-')#.replace('|n','\n') # cleanup is insane on this
    Spell['does'] = what_do
    print(f"What DO: {what_do}")
    

    page = str(stuff[3+segment])[5:-4].replace('        ','') # where it is from
    Spell['page'] = page
    print(f"Page: {page}")

    # gives what classes it is naturaly apart of as a list
    classes = stuff[4+segment].find_all('a') # cleanup
    for a in range(len(classes)):
        classes[a] = classes[a].get_text()
    Spell['classes'] = list(classes)
    print(f"Classes: {classes}")

    # need url
    Spell['url'] = url
    print(f"URL: {url}")

    return(Spell) # fini



# gives a spell from a spellbook or adds a spell to a spellbook if not there
def SpellBook(spellname = 'ALL', BOOKNAME = "Spells", ADD = True):
    '''
    Gives a spell from a spell book if posable otherwise from page
    SpellBook(spellname = 'ALL', BOOKNAME = "Spells", ADD = True): gives a dict of spell data : saves a spellbook
    SpellBook("Mage Hand"): gives dict data on mage hand : saves a spellbook named Spells and adds mage hand to book if not already there
    SpellBook(): gives a dict containing every spell in the book
    SpellBook("Find familiar", "Bertle"): gives dict data on find familiar : saves/loads a spellbook named Bertle and adds mage hand to book if not already there
    SpellBook("Find familiar", "Bertle", False): gives dict data on find familiar : loads a spellbook named Bertle
    SpellBook(["Find familiar", "Mage Hand"]): gives dict data on find familiar and Mage hand in a list : loads a spellbook named Spells
    '''
    try:
        SpellList = Load(BOOKNAME) # load a spellbook
    except:
        print("Couldent load: {}. Making new file.".format(BOOKNAME)) # Error on spellbook
        SpellList = {} # empty spell list

    if spellname == 'ALL': # gives entire spellList
        return(SpellList)

    spells = [] # the return for the spells
    if type(spellname) != list: # if you give it just a name
        spellname = [spellname] # make into list

    for sp in spellname: # go though every spell in list
        sp = sp.lower().replace(' ','-') # NO SPACES! NO CAPS!

        try:
            spells.append(SpellList[sp]) # if spell in list add it to spells
        except:
            SpellList[sp] = findSpell(sp) # spell not in list look it up online
            Save(BOOKNAME,SpellList) # Save book
            spells.append(SpellList[sp]) # Add to return spells
    
    return(spells[0] if len(spells) == 1 else spells) # return all spells asked for in a list or as a dict if you ask for one


# just a nice way to print out the spell
def cleanPrintS(spells):
    '''
    Prints a dict spell nicly
    cleanPrint(spell) : gives True/False (if printed correctly): prints a spell or error
    cleanPrint([spell]) : gives True/False (if printed correctly): prints all spells
    '''

    if type(spells) != list:
        spells = [spells]

    for spell in spells:
        if type(spell) == dict:
            print(spell['name'])
            print('school:', spell['school'])
            print('level:', spell['cast']['level'])
            print('casting time:', spell['cast']['casting time'])
            print('range:', spell['cast']['range'])
            print('components:', spell['cast']['components'])
            print('duration:', spell['cast']['duration'])
            print(spell['does'].replace('|n','\n'))
            print(spell['page'])
            print(spell['classes'])
            print()
        else:
            # wasent a usable spell
            print("Not spelled correctly!")
            return(False)
    return(True)


# reloads the spell list from the source
def reloadSpellList(NAME = 'Spells'):
    '''
    Reload the spell List 
    reloadSpellList(NAME): gives the spell list "Should be the same or similar"
    '''
    print("Begin Reload")
    spellList = [a for a in Load(NAME)] # get the spell names
    Save("Spells",{}) # basicly refreshes the Spell list
    print("New save made.")
    print("Grabbing spells.")
    lst = SpellBook(spellList) # recollect all spells
    print("Finished")
    return(lst)



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Custom Admin Tools ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



def rename_file(old_filepath, new_filepath):
    """ Rename a file """
    os.rename(old_filepath, new_filepath)


def printFile(file):
    """ Read a file and return the contense """
    with open(file, "r") as f:
        lines = f.read()
        return lines.strip()

def SaveFile(NAME, data):
    """ saves a file with the path/name NAME """
    f = open(NAME,'w+')
    f.writelines(data)
    f.close()
    return(True)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Basic Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#this is to send complex messages and its from old turtle
async def sendmsg(ctx, msg = 'embd', embed = None):
    if embed:
        await ctx.send(embed=embed)
    else:
        await ctx.send(msg)
    

#this is for old commands that dont work without it from message event yeah
async def sendmsgorig(message,msg):
    await message.channel.send(msg)

async def sendmsgdirect(ctx, msg = 'embd', embed = None):
    if embed:
        await ctx.author.send(embed=embed)
    else:
        await ctx.author.send(msg)

#random number
def randomnum(low,high):
    return random.randrange(low,high+1)







"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Basic Sound Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

async def connect_to_user(ctx):
    try:
        vc = ctx.voice_client
        user_channel = ctx.author.voice.channel
        return await connect_to_channel(user_channel, vc)
    except Exception as e:
        print(e)
        raise TurtleException('User was not in a voice channel.',
                             msg='Get in a voice channel!')



async def connect_to_channel(channel, vc=None):
    if not channel:
        raise AttributeError('channel cannot be None.')

    if not vc:
        vc = await channel.connect(reconnect=False)

    if vc.channel is not channel:
        await vc.move_to(channel)

    return vc


def get_existing_voice_client(guild):
    for vc in bot.voice_clients:
        if vc.guild is guild:
            return vc
            
'''

async def connect_to_channel(channel, vc=None):
    if not channel:
        raise AttributeError('channel cannot be None.')

    if not vc:
        vc = await channel.connect(reconnect=False)

    if vc.channel is not channel:
        await vc.move_to(channel)

    return vc


def get_existing_voice_client(guild):
    for vc in bot.voice_clients:
        if vc.guild is guild:
            return vc
'''