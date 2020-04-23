if __name__ == "__main__":
    #import os, subprocess, random, asyncio
    import discord
    from discord.ext import commands
    bot = commands.Bot(";")
    bertle = 275002179763306517


import math

try:
    #import JTools as jt
    from JTools import Save
except:
    import os
    os.system("python3 -m pip install git+https://github.com/Quiltic/JTools.git")
    #import JTools as jt
    from JTools import Save



def make_charicter(ctx, *args):
    try:

        skills = {'dexterity': 'DEX','wisdom':'WIS','intelligence':'INT','strength':'STR','constitution':'CON','charisma':'CHA',  'acrobatics': 'DEX','animalhandling':'WIS','arcana':'INT','athletics':'STR','deception':'CHA','history':'INT','insight':'WIS','intimidation':'CHA','investigation':'INT','medicine':'WIS','nature':'INT','perception':'WIS','performance':'CHA','persuasion':'CHA','religion':'INT','sleightofhand': 'DEX','stealth': 'DEX','survival':'WIS'}
        info = {'Current HP': 10,'Spell Save': 10, 'Proficiency': 1,'Spell Attack': 1,'Name': 'NAMELESS', 'URL': 'https://www.dungeonmastersvault.com/pages/dnd/5e/character-builder', 'AC': 10, 'Alignment': 'Unaligned', 'CHA': 10, 'CON': 10, 'Challenge Rating': 0, 'DEX': 10, 'HP': 10, 'INT': 10, 'Passive Perception': 10, 'STR': 10, 'Total Level': '1 ', 'Speed': '30ft', 'Main Class': 'Fighter', 'WIS': 10, 'Skills Prof': 'survival','Skills':[]}
        #print('start')
        magic = {"monk":'wis',"rogue":'INT',"fighter":'INT',"warlock":'CHA','wizard': 'INT', 'druid': 'WIS', 'sorcerer': 'CHA', 'bard': 'CHA', 'paladin': 'CHA', 'ranger': 'WIS', 'artificer': 'INT', 'cleric': 'WIS'}
        
        msg = ' '.join(args).split('|')[1:]
        print(msg)
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

        return(info)

    except Exception as e:
        print(e)



def get_modifyer(main, typ):
    '''
    Gives the modifyer
    ie 20 (+5), 10 (+0), 1 (-5)
    '''
    val = int(main[typ][:-1])
    val = math.floor((val-10)/2)
    return(val)