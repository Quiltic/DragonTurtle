from JTools import Save, Load, find_all, spellCheck, spell_check_helper
import requests
from bs4 import BeautifulSoup


# damage damage damage
def offenceSpell(spell):
    '''
    Given a spell (dict) it will try to give you its damage and other helpfull bits relting to casting a damage spell
    '''
    offencive = {'damage':[], 'type':'area', 'save':None, 'higherLvl':None, 'multishot':False, 'heal': False}

    try:
        # get the damages and there types cold lightning pearcing ect
        places = find_all(spell['does'],'take')
        for a in places:
            p1 = spell['does'][a:].index(' ') # could be takes witch would leave an s
            p2 = spell['does'][a:].index(' damage')
            tmp = spell['does'][a+p1+1:p2+a].split(' ') # the stuff of the spell
            if (len(tmp[0]) <= 5) or (tmp[0] != "half"): # Make sure that the spell doesent contain what i think it does
                offencive['damage'] += [tmp] #spell['does'][a+p1+1:p2+a].split(' ')
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


# SPELLLLSSSSSS
def getAllSpells():
    """
    This gives every spell from every major ofital D&D book. May be behind.
    Only here to be saved for later use if needed
    """
    url = 'https://www.dnd-spells.com/spells'

    r  = requests.get(url) # get data from url
    print(f"Has request: {r != None}")

    data = r.text # makes a nice text stuff
    soup = BeautifulSoup(data,features="lxml") # maks a soup

    tr = soup.find_all("tr") # gives all the divs
    print(f"Div Amount: {len(tr)}")
    spells = []
    for a in tr:
        try: # There are 2 empty holders. Probably just templates for new spells
            a = a.find_all('a')[0].get('href') # url
            #print(a[33:].replace('-',' ')) 
            spells.append(a[33:].replace('-',' ')) # True name
        except:
            pass
    print(f"Amount of spells total {len(spells)}")
    return(spells)


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
    print(f"Found Home: {home != None}")

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
    
    what_do = what_do.replace('’',"'").replace('•','*').replace('–','-').replace("",' ').replace("",' ').replace("",'-') #.replace('|n','\n') # cleanup is insane on this... Also every box is a difrent chariter, somehow
    Spell['does'] = str(what_do) #.encode('utf-8').decode() # So basicly. UNICODE IN A BYTE LIST IS A BBBBBBBBBBBBBBBBBBBBBBBBBB
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
        sp = spellCheck(sp,SpellList)

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





"""
def cast(*spell):
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
                if '#' in e:
                    await sendmsg(ctx,'Sorry but you need to make a Charicter to use []cast. Do `[]charicter` for instructions.')
                else:
                    await sendmsg(ctx,'Cast Error: {}'.format(e))

        else:
            await sendmsg(ctx,"Cant get spell: {}".format(spell))


"""

data = SpellBook() # get spell

#print(spellCheck("sanctuary",))
#print(SpellBook("visious mocury"))

'''
for spel in data:
    data[spel]['fight'] = offenceSpell(data[spel])

Save('test',data)
'''