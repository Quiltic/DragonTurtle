#this is so that the IDE doesent yell at me for not having this in the file.
if __name__ == "__main__":  
    from bs4 import BeautifulSoup
    import requests
    import JTools as jt

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Spell Tools ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# bread and butter of file. Gets spells 
def findSpell(spellname):
    '''
    Finds a spell from https://www.dnd-spells.com/spell and makes it into a dict
    findSpell(spellname): gives a dict or None if no spell is found
    findSpell("mage hand"): gives dict on magehand
    '''

    spellname = spellname.lower().replace(' ','-') # spells get put into the website as first-last (No spaces no caps)
    url = "https://www.dnd-spells.com/spell/"+spellname # get url
    r  = requests.get(url) # get data from url

    data = r.text # makes a nice text stuff
    soup = BeautifulSoup(data,features="lxml") # maks a soup
    if "No such spell, try again" in str(soup): # wasent a spell
        if 'ritual' in spellname: # rituals have this tag included
            return(None) # not spelled correctly or doesent exist
        return(findSpell(spellname+' ritual')) # try again as a ritual


    div = soup.find_all("div") # gives all the divs
    
    Spell = {} # spell base

    home = div[20].find_all("div")[0] # get the spells sorce from website

    #spells name
    name = str(home.find('h1')) # gets name of spell in nice format
    name = name[name.find('span>')+5:name.find('</span')] # cleanup
    Spell['name'] = name # save
    

    # this is all the achual info that we want
    stuff = home.find_all('p')

    school = str(stuff[0])[3:-4] # gives the school its apart of
    Spell['school'] = school
    

    # information for the casting
    casting_stuff = str(stuff[1])[5:-5].replace('        ','') # cleanup
    casting_stuff = casting_stuff.replace('<strong>','').replace('</strong>','').replace('<br/>','') # remove bold and other fluff
    casting_stuff = casting_stuff.split('\r\n') # get each as own thing
    cast = {} 
    for a in casting_stuff:
        loc = a.index(':') # gives the tipical info
        cast[a[:loc].lower()] = a[loc+2:-1] 

    Spell['cast'] = cast
    

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

    
    page = str(stuff[3+segment])[5:-4].replace('        ','') # where it is from
    Spell['page'] = page
    
    # gives what classes it is naturaly apart of as a list
    classes = stuff[4+segment].find_all('a') # cleanup
    for a in range(len(classes)):
        classes[a] = classes[a].get_text()
    Spell['classes'] = list(classes)
    
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
        SpellList = jt.Load(BOOKNAME) # load a spellbook
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
            jt.Save(BOOKNAME,SpellList) # Save book
            spells.append(SpellList[sp]) # Add to return spells
    
    return(spells[0] if len(spells) == 1 else spells) # return all spells asked for in a list or as a dict if you ask for one


# just a nice way to print out the spell
def cleanPrint(spells):
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
    spellList = [a for a in jt.Load(NAME)] # get the spell names
    jt.Save("Spells",{}) # basicly refreshes the Spell list
    print("New save made.")
    print("Grabbing spells.")
    lst = SpellBook(spellList) # recollect all spells
    print("Finished")
    return(lst)



if __name__ == "__main__":
    #reloadSpellList()
    cleanPrint(SpellBook(["find familiar", 'Mage hand']))
    