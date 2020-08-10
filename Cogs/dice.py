'''
All dice info is based off of here
'''

import discord
from discord.ext import commands
import math
from Tools import sendmsg, randomnum

from JTools import spellCheck



class Dice(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.wepons = {
            "wild magic": {'~Effect': '1d50', 'Table': ['Roll on this table at the start of each of your turns for the next minute, ignoring this result on subsequent rolls.',
                'For the next minute, you can see any invisible creature if you have line of sight to it.',
                'A modron chosen and controlled by the DM appears in an unoccupied space within 5 feet of you, then disappears I minute later.',
                'You cast Fireball as a 3rd-level spell centered on yourself.',
                'You cast Magic Missile as a 5th-level spell.',
                'Roll a d10. Your height changes by a number of inches equal to the roll. If the roll is odd, you shrink. If the roll is even, you grow.',
                'You cast Confusion centered on yourself.',
                'For the next minute, you regain 5 hit points at the start of each of your turns.',
                'You grow a long beard made of feathers that remains until you sneeze, at which point the feathers explode out from your face.',
                'You cast Grease centered on yourself.',
                'Creatures have disadvantage on saving throws against the next spell you cast in the next minute that involves a saving throw.',
                'Your skin turns a vibrant shade of blue. A Remove Curse spell can end this effect.',
                'An eye appears on your forehead for the next minute. During that time, you have advantage on Wisdom (Perception) checks that rely on sight.',
                'For the next minute, all your spells with a casting time of 1 action have a casting time of 1 bonus action.',
                'You teleport up to 60 feet to an unoccupied space of your choice that you can see.',
                'You are transported to the Astral Plane until the end of your next turn, after which time you return to the space you previously occupied or the nearest unoccupied space if that space is occupied.',
                'Maximize the damage of the next damaging spell you cast within the next minute.',
                'Roll a d10. Your age changes by a number of years equal to the roll. If the roll is odd, you get younger (minimum 1 year old). If the roll is even, you get older.',
                '1d6 flumphs controlled by the DM appear in unoccupied spaces within 60 feet of you and are frightened of you. They vanish after 1 minute.',
                'You regain 2d10 hit points.',
                'You turn into a potted plant until the start of your next turn. While a plant, you are incapacitated and have vulnerability to all damage. If you drop to 0 hit points, your pot breaks, and your form reverts.',
                'For the next minute, you can teleport up to 20 feet as a bonus action on each of your turns.',
                'You cast Levitate on yourself.',
                'A unicorn controlled by the DM appears in a space within 5 feet of you, then disappears 1 minute later.',
                "You can't speak for the next minute. Whenever you try, pink bubbles float out of your mouth.",
                'A spectral shield hovers near you for the next minute, granting you a +2 bonus to AC and immunity to Magic Missile.',
                'You are immune to being intoxicated by alcohol for the next 5d6 days.',
                'Your hair falls out but grows back within 24 hours.',
                "For the next minute, any flammable object you touch that isn't being worn or carried by another creature bursts into flame.",
                'You regain your lowest-level expended spell slot.',
                'For the next minute, you must shout when you speak.',
                'You cast Fog Cloud centered on yourself.',
                'Up to three creatures you choose within 30 feet of you take 4d10 lightning damage.',
                'You are frightened by the nearest creature until the end of your next turn.',
                'Each creature within 30 feet of you becomes invisible for the next minute. The invisibility ends on a creature when it attacks or casts a spell.',
                'You gain resistance to all damage for the next minute.',
                'A random creature within 60 feet of you becomes poisoned for 1d4 hours.',
                'You glow with bright light in a 30-foot radius for the next minute. Any creature that ends its turn within 5 feet of you is blinded until the end of its next turn.',
                "You cast Polymorph on yourself. If you fail the saving throw, you turn into a sheep for the spell's duration.",
                'Illusory butterflies and flower petals flutter in the air within 10 feet of you for the next minute.',
                'You can take one additional action immediately.',
                'Each creature within 30 feet of you takes 1d10 necrotic damage. You regain hit points equal to the sum of the necrotic damage dealt.',
                'You cast Mirror Image.',
                'You cast Fly on a random creature within 60 feet of you.',
                "You become invisible for the next minute. During that time, other creatures can't hear you. The invisibility ends if you attack or cast a spell.",
                'If you die within the next minute, you immediately come back to life as if by the Reincarnate spell.',
                'Your size increases by one size category for the next minute.',
                'You and all creatures within 30 feet of you gain vulnerability to piercing damage for the next minute.',
                'You are surrounded by faint, ethereal music for the next minute.',
                'You regain all expended sorcery points.']},
            "coin": {'~Toss': "1d2", "Table": ['Heads','Tails']},
            "bear": {'~Type': "1d11", "Table": ['Brown Bear', 'Polar Bear', 'North American Black Bear', 'Asiatic Black Bear', 'Andean Bear', 'Panda Bear', 'Sloth bear', 'Sun Bear', 'Red Panda Bear', 'Owl Bear', 'Were Bear']},
            
            #Simple Melee Weapons
            "club": {'To Hit': '1d20 + prof + str','Damage': '1d4 + str'},
            "dagger": {'To Hit': '1d20 + prof + max(dex,str)','Damage': '1d4 + max(dex,str)'},
            "handaxe": {'To Hit': '1d20 + prof + str','Damage': '1d6 + str'},
            "javelin": {'To Hit': '1d20 + prof + str','Damage': '1d6 + str'},
            "light hammer": {'To Hit': '1d20 + prof + str','Damage': '1d4 + str'},
            "mace": {'To Hit': '1d20 + prof + str','Damage': '1d6 + str'},
            "quarterstaff": {'To Hit': '1d20 + prof + str','Damage': '1d8 + str'},
            "sickle": {'To Hit': '1d20 + prof + str','Damage': '1d4 + str'},
            "spear": {'To Hit': '1d20 + prof + str','Damage': '1d8 + str'},

            #Simple Ranged Weapons
            "light crossbow": {'To Hit': '1d20 + prof + dex','Damage': '1d8 + dex'},
            "dart": {'To Hit': '1d20 + prof + max(dex,str)','Damage': '1d4 + max(dex,str)'},
            "shortbow": {'To Hit': '1d20 + prof + dex','Damage': '1d6 + dex'},
            "sling": {'To Hit': '1d20 + prof + dex','Damage': '1d6 + dex'},


            #Martial Melee Weapons
            "battleaxe": {'To Hit': '1d20 + prof + str','Damage': '1d10 + str'},
            "flail": {'To Hit': '1d20 + prof + str','Damage': '1d8 + str'},
            "glaive": {'To Hit': '1d20 + prof + str','Damage': '1d10 + str'},
            "greataxe": {'To Hit': '1d20 + prof + str','Damage': '1d12 + str'},
            "greatsword": {'To Hit': '1d20 + prof + str','Damage': '2d6 + str'},
            "halberd": {'To Hit': '1d20 + prof + str','Damage': '1d10 + str'},
            "lance": {'To Hit': '1d20 + prof + str','Damage': '1d12 + str'},
            "longsword": {'To Hit': '1d20 + prof + str','Damage': '1d10 + str'},
            "maul": {'To Hit': '1d20 + prof + str','Damage': '2d6 + str'},
            "morningstar": {'To Hit': '1d20 + prof + str','Damage': '1d8 + str'},
            "pike": {'To Hit': '1d20 + prof + str','Damage': '1d10 + str'},

            "rapier": {'To Hit': '1d20 + prof + max(dex,str)','Damage': '1d8 + max(dex,str)'},
            "scimitar": {'To Hit': '1d20 + prof + max(dex,str)','Damage': '1d6 + max(dex,str)'},
            "shortsword": {'To Hit': '1d20 + prof + max(dex,str)','Damage': '1d6 + max(dex,str)'},

            "trident": {'To Hit': '1d20 + prof + str','Damage': '1d8 + str'},
            "war pick": {'To Hit': '1d20 + prof + str','Damage': '1d8 + str'},
            "warhammer": {'To Hit': '1d20 + prof + str','Damage': '1d10 + str'},

            "whip": {'To Hit': '1d20 + prof + max(dex,str)','Damage': '1d4 + max(dex,str)'},

            #Martial Ranged Weapons
            "blowgun": {'To Hit': '1d20 + prof + dex','Damage': '1d1 + dex'},
            "hand crossbow": {'To Hit': '1d20 + prof + dex','Damage': '1d6 + dex'},
            "heavy crossbow": {'To Hit': '1d20 + prof + dex','Damage': '1d10 + dex'},
            "longbow": {'To Hit': '1d20 + prof + dex','Damage': '1d8 + dex'},
            "net": {'To Hit': '1d20 + prof + dex'},

            }


    # so nice
    def replace(self, msg):
        '''
        given a msg return a replaced version 
        '''
        replaceables = {'+-':'-','++':'+','--':'+','-+':'-','*/':'/','/*':'*','+':' +','-':' -','*':' *','/':' /','+ ':'+','- ':'-','/ ':'/','* ':'*', '  ':' ',} # correct for weirdness
        for word in replaceables:
            msg = msg.replace(word,replaceables[word])
        return(msg)


    ''' This is for cleaning up inputs'''
    # this is for max and min
    async def cleanup_helper_minmax(self, ctx, msg, current):
        '''
        for max and min holy crap this was anoying
        '''

        print('msg: ', msg)
        tipe = 'max' if 'max' in msg else 'min' # so we know what type to use

        # failsafe
        replaceables = {'max': 'max(', 'min':'min(', '((':'('}
        for a in replaceables:
            msg = msg.replace(a,replaceables[a])

        msg = msg[:-1].split(',')
        msg[0] = msg[0][msg[0].index('(')+1:]
        #print(msg)

        msg = await self.cleanup_helper(ctx, msg, current)
        #print(f'{msg}')

        if tipe == 'max':
            return(max(msg))
        else:
            return(min(msg))

    # for str, stealth, perc ect
    async def cleanup_helper(self, ctx, msg, current):
        # spellcheck after all starting cleanup
        

        for a in range(len(msg)):
            #print('a: ',a)
            print('msg: ', msg)
            if msg[a] != '': # failsafe
                tip = msg[a][0] if (msg[a][0] == '+') or (msg[a][0] == '-') or (msg[a][0] == '/') or (msg[a][0] == '*') else '+' # for custom rolls
                
                tmp = spellCheck(msg[a].replace('+','').replace('-','').replace('*','').replace('/','').replace(' ',''), current.skills) # spell checking

                if tmp != None: # replace for later
                    msg[a] = tmp


                # for max and min
                if ('max' in msg[a]) or ('min' in msg[a]):
                    try:
                        msg[a].index(')') # tester only
                        b = a
                    except ValueError:
                        try:
                            loc = None
                            b = a + 1
                            while loc == None:
                                try:
                                    loc = msg[b].index(')')  # tester only
                                except ValueError:
                                    b += 1
                        except IndexError:
                            b -= 1

                    msg[a] = await self.cleanup_helper_minmax(ctx, ''.join(msg[a:b+1]), current) # the minmax stuff

                    # cleanup for max and min
                    for val in range(1,b-a+1):
                        msg[a+val] = ' '


                # get the skill stuff
                if (msg[a] != ' ') and (len(msg[a]) >= 3):
                    for name in current.skills:
                        if msg[a].replace('+','').replace('-','').replace('*','').replace('/','').replace(' ','') in name:
                            #await ctx.send(f"Rolling for {name}! `{current.skills[name]}`") # eah might as well
                            msg[a] = tip + str(current.skills[name]) # replace with value
                        
                        elif msg[a].replace('+','').replace('-','').replace('*','').replace('/','').replace(' ','') in 'initiative':
                            msg[a] = tip + str(current.skills['dexterity']) # replace with value

                        elif msg[a].replace('+','').replace('-','').replace('*','').replace('/','').replace(' ','') in 'proficiency':
                            msg[a] = tip + str(current.proficiency) # replace with value

                        elif msg[a].replace('+','').replace('-','').replace('*','').replace('/','').replace(' ','') in "spellcasting_ability_modifier":
                            msg[a] = tip + str(current.spellMod) # replace with value
                            

        return(msg)
        
    # cleanup core
    async def cleanup(self, ctx, *msg):
        out = {} # the end result is a dict with 'dice#' and if needed 'total', 'adv' or 'disadv'
        current = await self.bot.get_cog('Player').getCurrent(ctx) #data for use of stuff later on
        msg = ' '.join(msg[0]).lower() + ' ' # all together now
        print(f'msg in : {msg}')

        msg = msg.replace('`','')
        msg = msg.replace('**','')
        msg = msg.replace('--','')
        msg = msg.replace('__','')
        msg = msg.replace('~','')

        # for rolling a flat d20
        if msg == ' ':
            msg = '1d20 '
        
            


        ''' THIS DOESENT WORK YET!???? '''
        # for custom rolls
        if len(msg[:-1]) >= 3:
            for block in current.customRolls:
                if msg[:-1] in block:
                    for m in current.customRolls[block]:
                        if 'Table' != m:
                            out[m] = await self.cleanup(ctx,(current.customRolls[block][m], ''))
                        else:
                            out[m] = current.customRolls[block][m]
                        #print(out[m])
                    return(out)

            # for basic weapons
            for block in self.wepons:
                if msg[:-1] in block:
                    for m in self.wepons[block]:
                        if 'Table' != m:
                            out[m] = await self.cleanup(ctx,(self.wepons[block][m], ''))
                        else:
                            out[m] = self.wepons[block][m]
                        #print(out[m])
                    return(out)

            

        '''
        replaceables = {'+-':'-','++':'+','--':'+','-+':'-','*/':'/','/*':'*','+':' +','-':' -','*':' *','/':' /','+ ':'+','- ':'-','/ ':'/','* ':'*', '  ':' ',} # correct for weirdness
        for word in replaceables:
            msg = msg.replace(word,replaceables[word])
        '''
        msg = self.replace(msg)
        
        # This is for advantage
        msg = msg.replace('advantage','adv')
        msg = msg.replace('adv',' adv')
        msg = msg.replace('dis adv','dis')
        msg = msg.replace('dis',' dis')

        # resplit to be able to do less cleaning more transfering...
        msg = msg[:-1].split(' ')
        #print(msg)
        if msg[0] == '':
            if msg[1].startswith('+') or msg[1].startswith('-') or msg[1].startswith('*') or msg[1].startswith('/') or msg[1].startswith('adv') or msg[1].startswith('dis'): # missing a d20
                msg = ['1d20'] + msg[1:]
        elif (msg[0].startswith('d')):
            msg = ['1d20'] + msg
        elif ('d' not in msg[0]) and not (msg[0].startswith('max')) and not (msg[0].startswith('min')):
            msg = ['1d20'] + msg
        
        

        # do the main cleanup
        msg = await self.cleanup_helper(ctx, msg, current)
        #print(msg)

        # the final cleanup?
        msg = ' '.join(msg).lower()

        '''
        replaceables = {'+-':'-','++':'+','--':'+','-+':'-','*/':'/','/*':'*','+':' +','-':' -','*':' *','/':' /','  ':' ',} # correct for weirdness ... again
        for word in replaceables:
            msg = msg.replace(word,replaceables[word])
        '''

        msg = self.replace(msg)
        #print(spellCheck('aracna'))
        #await sendmsg(ctx, spellCheck('aracna'))
        #print(self.bot.get_cog('Player'))

        

        ''' NEEDS TO RETURN A DICT '''

        if out == {}:
            tipe = 'adv' if 'adv' in msg else 'dis' if 'dis' in msg else None
            out['dice1'] = msg
            
            if tipe != None:
                out['dice1'] = msg.replace(tipe,'')[:-1]
                out['dice2'] = msg.replace(tipe,'')[:-1]
                out[tipe.capitalize()] = ''
                
            #out['total'] = ['dice1']
        
            
        return(out)



    ''' This is for rolling the achual dice'''
    # SNAKE EYES!?
    def dice_roller_helper(self,string):
        '''
        This is for dice rolling IE 1d6 4d12 exct
        '''
        if string in 'disadvantage': # catches both adv and disadv
            return string

        data = string.split('d') # get a split of the dice
        print(f'rolling {data}')

        if len(data) == 1: # failsage for if you give it +1 or a word
            return(string)

    
        mult = -1 if '-' in data[0] else 1 # for negitives

        data[0] = data[0].replace('-','').replace('+','').replace('*','').replace('/','') # cleanup
        try:
            int(data[0])
            vals = [mult*randomnum(1,int(data[1])) for _ in range(int(data[0]))] # roll the dice alot
        except Exception as e:
            print(e)
            return(string)

        return(vals)
        #return((string,vals)) # may be helpfull later

    # roll cleanup 
    def diceRoller(self,data):
        '''
        Rolls dice and makes em prrty Also does math.
        Takes in data from cleanup function
        '''

        print(f'input : {data}') # show what im working with
        minmax = [20,0] # for the adv vs disadv min,max
        for dice in data: # iterate through it
            print(f'name : {dice}') # what peace we are on


            if (dice.lower() == "total") or (dice.lower() == "adv") or (dice.lower() == "dis") or (dice.lower() == "table"): # skip this its not supposed to be here
                pass
            else: 
                if type(data[dice]) == dict: # if we have recursion which tipicly happens from custom rolls
                    stuff = self.diceRoller(data[dice]) # call self
                else:
                    stuff = [self.dice_roller_helper(v) for v in data[dice].split(' ')] # get the data we want


                sudosum = 0 # end val we want
                for val in stuff: # iterate throuhg it because we have strings and lists...
                    if type(val) == list: # lists are from dice rolls making them much easer to handle
                        sudosum += sum(val) 
                    else:
                        try: # in case of unwanted string
                            sudosum += int(val)
                        except:
                            pass
                    
                
                #self.dice_roller_helper(data[dice])
                #print(stuff)

                data[dice] = [str(data[dice]), stuff, sudosum] # end data


                if type(data[dice][1]) == dict: # recursion is no good here
                    data[dice] = data[dice][1] # if not done this makes alot of clones of this data

                minmax[0] = min(minmax[0],sudosum)
                minmax[1] = max(minmax[1],sudosum)

            try:
                if (type(data[dice]) == dict) and (len(data[dice]) == 1): # remove the nonhelpfull dict
                        data[dice] = data[dice]['dice1'] # if not done this makes alot of clones of this data
            except:
                pass
        

        try:
            data['Dis'] # test
            data['Dis'] = [' ', ' ', minmax[0]]
        except KeyError:
            pass

        try:
            data['Adv'] # test
            data['Adv'] = [' ', ' ', minmax[1]]
        except KeyError:
            pass

        print(f'output : {data}') # out
        return(data)



    ''' This is for makin it look prdy on printout'''
    def pritify_helper(self, data):
        '''
        takes in a roll (list) and gives what it should say (string)
        data = ['1d20 +2 +1', [[14], '+2', '+1'], 17]
        returns
        
        '''
        say = '' # what say you
        if data[0] == ' ': # failsafe
            return(' ')


        stuff = data[0].split(' ')

        for a in range(len(stuff)):
            say += f' +{stuff[a]}'
            if stuff[a] != data[1][a]:
                words = f' {data[1][a]}'

                if 'd' in stuff[a]:
                    val = stuff[a].index('d') # find the maximum roll
                    try:
                        int(stuff[a][val+1:]) # test for a number
                        val = [f'{stuff[a][val+1:]}]', f'**{stuff[a][val+1:]}**]',f'{stuff[a][val+1:]}, ', f'**{stuff[a][val+1:]}**, '] # replace vals with bold
                        say += words.replace('[1]','[**1**]').replace(' 1,',' **1**,').replace(' 1]',' **1**]').replace(val[0],val[1]).replace(val[2],val[3]) # true replace
                    except:
                        say += words # failsafe
                else:
                    say += words # I dont know what this would be but i dont want to risk it

        print(say)

        say = self.replace(say)

        '''
        for a in data[1]: # the name 
            say += ' +' + a # space and +
            if 'd' in a:
                    val = a.index('d') # find val
                    val = ['{}]'.format(a[val+1:]), '**{}**]'.format(a[val+1:]),'{}, '.format(a[val+1:]), '**{}**, '.format(a[val+1:])] # replace vals with bold
                    say += ' ' + str(data[a]).replace('1]','**1**]').replace(' 1,',' **1**,').replace(val[0],val[1]).replace(val[2],val[3]) # true replace
        '''
        return(say)


    def pritify_recursion(self, data, embed):
        '''
        for use of embeded data
        '''
        print(data)

        for a in data:
            if a == 'Table':
                pass
            elif (type(data[a]) != dict):
                words = self.pritify_helper(data[a])
                print('words: ',words)

                if '~' == a[0]: # normal dice nothin fancy
                    embed.add_field(name=f"Out: `{data['Table'][int(data[a][2])-1]}`", value=f"{a[1:].capitalize()}: {words[2:]}", inline=False)
                elif 'dice' in a: # normal dice nothin fancy
                    embed.add_field(name=f'Total: `{data[a][2]}`', value=words[2:], inline=False)
                else: # cool dice
                    embed.add_field(name=f'{a.capitalize()} Total: `{data[a][2]}`', value=f"{a.capitalize()}: {words[2:]}", inline=False)
            else:
                embed = self.pritify_recursion(data[a], embed)
                
            print('embed: ',embed)
        return(embed)


    async def pritify(self,ctx, data):
        '''
        Gives the embed for use of pritty returning data
        '''
        current = await self.bot.get_cog('Player').getCurrent(ctx) #data for use of namein the active user

        if current.name != 'First one!':
            dice=discord.Embed(title=f"{current.name} Rolls", color=0xe33604)
        else:
            dice=discord.Embed(title=f"{ctx.author.name} Rolls", color=0xe33604)


        dice = self.pritify_recursion(data, dice)

        #embed.add_field(name=stuff['speak'].replace('[1]','[**1**]').replace('[20]','[**20**]'), value='**Total**: `'+ str(stuff['total']) + '`', inline=False)
        return(dice)






    async def OutsideRoll(self, ctx, *msg):
        '''
        same as other but is used for rolling in difrent cogs
        rolls a die or a bunch of dice
        NOTE 1d20 means 1, 20 sided die
        []r (rolls a 20 sided die)
        []r +1 (rolls 1d20 +1)
        []r 4d6 (rolls 4, 6 sided dice)
        []r adv (rolls 1d20 with advantage, maximum of the two)
        []r dis (rolls 1d20 with disadvantage, minimum of the two)

        Thease can be commbined in many ways to make alot of cool things
        
        []r `skill` (rolls for a skill, automatic charicter made if you dont have one)
        []r `CustomRollName` (rolls a custom roll made by player, do []cr or []customroll for more info)
        '''
        data = await self.cleanup(ctx,msg)
        return(self.diceRoller(data))


    @commands.command()
    async def r(self, ctx, *msg):
        '''
        rolls a die or a bunch of dice
        NOTE 1d20 means 1, 20 sided die
        []r (rolls a 20 sided die)
        []r +1 (rolls 1d20 +1)
        []r 4d6 (rolls 4, 6 sided dice)
        []r adv (rolls 1d20 with advantage, maximum of the two)
        []r dis (rolls 1d20 with disadvantage, minimum of the two)

        Thease can be commbined in many ways to make alot of cool things
        
        []r `skill` (rolls for a skill, automatic charicter made if you dont have one)
        []r `CustomRollName` (rolls a custom roll made by player, do []cr or []customroll for more info)
        '''
        data = await self.cleanup(ctx,msg)
        #await sendmsg(ctx, data)
        data = self.diceRoller(data)
        #await sendmsg(ctx, data)
        #data = self.pritify(data)
        await sendmsg(ctx,embed= await self.pritify(ctx, data))


    @commands.command()
    async def roll(self, ctx, *msg):
        '''
        rolls a die or a bunch of dice
        NOTE 1d20 means 1, 20 sided die
        []r (rolls a 20 sided die)
        []r +1 (rolls 1d20 +1)
        []r 4d6 (rolls 4, 6 sided dice)
        []r adv (rolls 1d20 with advantage, maximum of the two)
        []r dis (rolls 1d20 with disadvantage, minimum of the two)

        Thease can be commbined in many ways to make alot of cool things
        
        []r `skill` (rolls for a skill, automatic charicter made if you dont have one)
        []r `CustomRollName` (rolls a custom roll made by player, do []cr or []customroll for more info)
        '''
        await self.r(ctx,msg)


    @commands.command()
    async def init(self, ctx):
        '''
        Rolls Your initiative
        []init
        '''
        await self.r(ctx,('+dex'))


    @commands.command()
    async def save(self, ctx, *msg):
        '''
        Rolls for some save
        []save (str, dex, con, int, wiz, cha)
        '''
        lst = {'fighter':['STR','CON'], 'druid': ['WIS','INT'], 'artificer':['INT','CON'], 'barbarian':['STR','CON'], 'bard':['DEX','CHA'], 'cleric':['WIS','CHA'], 'monk':['STR','DEX'], 'paladin':['WIS','CHA'], 'ranger':['STR','DEX'], 'rouge':['DEX','INT'], 'sorcerer':['CON','CHA'], 'warlock':['WIS','CHA'], 'wizard':['INT','WIS']}
        
        current = await self.bot.get_cog('Player').getCurrent(ctx)
        lsta = {'dexterity': 'DEX','wisdom':'WIS','intelligence':'INT','strength':'STR','constitution':'CON','charisma':'CHA',  'acrobatics': 'DEX','animalhandling':'WIS','arcana':'INT','athletics':'STR','deception':'CHA','history':'INT','insight':'WIS','intimidation':'CHA','investigation':'INT','medicine':'WIS','nature':'INT','perception':'WIS','performance':'CHA','persuasion':'CHA','religion':'INT','sleightofhand': 'DEX','stealth': 'DEX','survival':'WIS'}
        
        for stuff in msg:
            stuff = spellCheck(stuff.replace('+','').replace('-','').replace('*','').replace('/','').replace(' ',''), current.skills) # spell checking
            for name in current.skills:
                if stuff.replace('+','').replace('-','').replace('*','').replace('/','').replace(' ','') in name:
                    print(lsta[name], lst[current.mainClass])
                    if lsta[name] in lst[current.mainClass]:
                        #print(((' '.join(msg) + ' prof')), type(((' '.join(msg) + ' prof'))))
                        await self.r(ctx,((' '.join(msg) + ' prof')))
                        return
        
        await self.r(ctx, *msg)
        

        #await self.r(ctx,(msg+'save'))

        #if tpe.upper() in lst[using[str(ctx.author)]['Main Class'].lower().replace(' ','')]:
        #    mod += int(using[str(ctx.author)]['Proficiency'])
        


    @commands.command()
    async def cr(self, ctx, *args):
        '''
        Lets you make custom rolls
        []cr (gives you info on how to start)
        '''

        if len(args) == 0:
            stuff = """```\n[]customroll |Name: __\n|Main: __\n|Second: __```"""
            
            await sendmsg(ctx,stuff)
            await sendmsg(ctx,"Copy the above then replace __ with whatever ~~(works with all []r commands)~~ and send back")
            await sendmsg(ctx,"You can replace the names of `Main` and `Second` with almost any word but **update** and **Name**.")
            await sendmsg(ctx,"If you dont have anything for that slot leave it blank (~~EXCEPT NAME!!~~)")
            #await sendmsg(ctx,"For the table put it inside a code block **```**.")
            #await sendmsg(ctx,"Table rolls are done off the Second Roll")
            #await sendmsg(ctx,"For rolls inside the table put it inside two **`**.")
        elif 'update' in args:
            pass
        else:
            current = await self.bot.get_cog('Player').getCurrent(ctx)

            #print(args)
            msg = (' '.join(args[0])+ ' ').split('|')[1:] # i dont fully know why it needs the [0][0] but from something it gains 2 lvls
            #print(msg) 

            info = {}
            
            for a in msg:
                #print(a)
                splt = a.index(': ')
                #print(a[:splt], a[splt+2:])
                if (a[splt+2:splt+4] != '__') and (a[splt+2:] != ' ') and (a[splt+1:] != ' '):
                    info[a[:splt]] = a[splt+2:-1]
            
            #print(info)
            
            name = info['Name']
            del info["Name"]
            current.customRolls[name] = info
            #print(current.customRolls[name])

            await sendmsg(ctx, f"Sucsessfully made {name} custom roll!")
            

    @commands.command()
    async def customroll(self,ctx,*args):
        '''
        Lets you make custom rolls
        []cr (gives you info on how to start)
        '''
        await self.cr(ctx, args)


    @commands.command()
    async def table(self,ctx,*args):
        '''
        Lets you make custom tables for rolls
        []table (gives you info on how to start)
        '''

        if len(args) == 0:
            stuff = """`[]table  ```\nName:___ \n___\n``` `"""
            
            await sendmsg(ctx,stuff)
            await sendmsg(ctx,"Copy the above then replace \_\_ with whatever __(works with all []r commands)__ and send back!")
            await sendmsg(ctx,"Add a new posibility inside of the \`\`\`, and hit enter outside to submit.")
        elif 'update' in args:
            pass
        else:
            #print(args[1:-1])
            #"coin": {'~Toss': "1d2", "Table": ['Heads','Tails']}
            #somethin[args[1]] = args[1:-1]
            print(args[1], list(args[2:-1]))
            current = await self.bot.get_cog('Player').getCurrent(ctx)
            current.customRolls[args[1].replace('Name:','')] = {'~Roll': f"1d{len(list(args[2:-1]))}", "Table":list(args[2:-1])}
            await sendmsg(ctx, f"Sucsessfully made {args[1].replace('Name:','')} custom Table!")



def setup(bot):
    bot.add_cog(Dice(bot))