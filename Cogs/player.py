'''
This is where all of the basic character and player code is placed
'''
    
import discord
from discord.ext import commands, tasks
import math
from Tools import sendmsg

from JTools import Save, Load




class Character():
    def __init__(self, data = None):
        
        # Load info that is needed
        if type(data) == dict: # From a save
            self.loadChar(data)
        elif type(data) == tuple: # from a command
            self.createChar(data)
        else:
            ''' INSANELY IMPORTANT '''
            self.name = 'First one!'
            self.url = 'https://www.dndbeyond.com/characters/builder#/'
            self.mainClass = 'wizard'
            self.level = 1
            self.stats = {'STR': 10, 'DEX' : 10, 'CON' : 10, 'INT' : 10, 'WIS' : 10, 'CHA' : 10}
            self.AC = 10


            ''' helpfull stuff'''
            self.curHP = 1
            self.maxHP = 1
            self.tempHP = 0
            self.speed = '30ft'
            
            
            ''' stuff stuff '''
            self.cash = 0 # 100.24 : 100 gold, 2 silver, 4 copper
            self.invintory = '' # stuff
            self.hand = [] # this is for playing cards

            ''' custom rolls stuff '''
            self.customRolls = {}

            self.skillsProf = ""
            self.expertise = ""

            ''' spells stuff '''
            self.spellList = [] # player adds te name of the spells to this
            # dont know how helpfull this wll be but its here now
            self.spellSlots = {'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0} # current number of spell slots left to be used 
            # this needs to be calculated in an interesting way that ill deal with later
            self.spellSlotsMax = {'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0} 


            


            ''' stuff that gets redone every time. for ease of loading'''
            self.proficiency = math.floor(int(self.level)/5)+2 # nice equation huh?


            magic = {"monk":'WIS',"rogue":'INT',"fighter":'INT',"warlock":'CHA','wizard': 'INT', 'druid': 'WIS', 'sorcerer': 'CHA', 'bard': 'CHA', 'paladin': 'CHA', 'ranger': 'WIS', 'artificer': 'INT', 'cleric': 'WIS'}
            self.spellMod = self.get_modifyer(self.stats[magic[self.mainClass]])
            self.spellAttack = self.proficiency + self.spellMod
            self.spellSave = 8 + self.spellAttack


            self.skills = {'dexterity': 'DEX','wisdom':'WIS','intelligence':'INT','strength':'STR','constitution':'CON','charisma':'CHA',  'acrobatics': 'DEX','animalhandling':'WIS','arcana':'INT','athletics':'STR','deception':'CHA','history':'INT','insight':'WIS','intimidation':'CHA','investigation':'INT','medicine':'WIS','nature':'INT','perception':'WIS','performance':'CHA','persuasion':'CHA','religion':'INT','sleightofhand': 'DEX','stealth': 'DEX','survival':'WIS', 'initiative':'DEX'}
            for skill in self.skills:
                self.skills[skill] = self.get_modifyer(self.stats[self.skills[skill]])
                
                if skill in self.expertise.lower(): # skills gain *2 prof
                    self.skills[skill] += self.proficiency * 2

                elif skill in self.skillsProf.lower(): # skills gain prof
                    self.skills[skill] += self.proficiency   


    def get_modifyer(self,val):
        '''
        Gives the modifyer
        ie 20 -> (+5), 10 -> (+0), 1 -> (-5)
        '''
        return(math.floor((val-10)/2))


    def getSaveable(self):
        """
        Gives the class as a dict
        """
        #dic = {"name":self.name, 'url':self.url, 'mainClass':self.mainClass, 'level':self.level, 'stats':self.stats, 'AC':self.AC, 'curHP':self.curHP, 'maxHP':self.maxHP, 'speed':self.speed, 'proficiency':self.proficiency,'cash':self.cash,'invintory':self.invintory,'spellList':self.spellList,'spellSlots':self.spellSlots,'spellSlotsMax':self.spellSlotsMax,'spellAttack':self.spellAttack,'spellSave':self.spellSave,'customRolls':self.customRolls,'skillsProf':self.skillsProf,'expertise':self.expertise,'skills':self.skills}
        dic = {"name":self.name, 
        'url':self.url, 
        'mainClass':self.mainClass, 
        'level':self.level, 
        'stats':self.stats, 
        'AC':self.AC, 
        'curHP':self.curHP, 
        'maxHP':self.maxHP, 
        'speed':self.speed, 
        'cash':self.cash,
        'invintory':self.invintory,
        'spellList':self.spellList,
        'spellSlots':self.spellSlots,
        'spellSlotsMax':self.spellSlotsMax,
        'customRolls':self.customRolls,
        'skillsProf':self.skillsProf,
        'expertise':self.expertise,
        }
        return(dic)


    def loadChar(self,data):
        """
        Data is made off of getSaveable or is made from cleanup
        """
        ''' INSANELY IMPORTANT '''
        self.name = data['name'].capitalize()
        self.url = data['url']
        self.mainClass = data['mainClass']
        self.level = data['level']
        try:
            self.stats = data['stats']
        except:
            self.stats = {'STR': data['STR'], 'DEX' : data['DEX'], 'CON' : data['CON'], 'INT' : data['INT'], 'WIS' : data['WIS'], 'CHA' : data['CHA']}
        self.AC = data['AC']


        ''' helpfull stuff'''
        self.curHP = data['curHP']
        self.maxHP = data['maxHP']
        self.tempHP = 0
        self.speed = data['speed']
        
        
        
        ''' prof stuff'''
        self.proficiency = math.floor(int(self.level+1)/5)+2 # nice equation huh?

        
        ''' stuff stuff '''
        self.cash = data['cash'] # 100.24 : 100 gold, 2 silver, 4 copper
        self.invintory = data['invintory'] # stuff
        self.hand = [] #data['hand'] # this is for playing cards
        

        ''' spells stuff '''
        self.spellList = data['spellList'] # player adds te name of the spells to this

        # dont know how helpfull this wll be but its here now
        self.spellSlots = data['spellSlots'] # current number of spell slots left to be used 
        # this needs to be calculated in an interesting way that ill deal with later
        self.spellSlotsMax = data['spellSlotsMax']

        ''' custom rolls stuff '''
        self.customRolls = data['customRolls']  
        
        magic = {"monk":'WIS',"rogue":'INT',"fighter":'INT',"warlock":'CHA','wizard': 'INT', 'druid': 'WIS', 'sorcerer': 'CHA', 'bard': 'CHA', 'paladin': 'CHA', 'ranger': 'WIS', 'artificer': 'INT', 'cleric': 'WIS'}
        self.spellMod = self.get_modifyer(self.stats[magic[self.mainClass]])
        self.spellAttack = self.proficiency + self.spellMod
        self.spellSave = 8 + self.spellAttack


        

        self.skillsProf = data['skillsProf']
        self.expertise = data['expertise']
        self.skills = {'dexterity': 'DEX','wisdom':'WIS','intelligence':'INT','strength':'STR','constitution':'CON','charisma':'CHA',  'acrobatics': 'DEX','animalhandling':'WIS','arcana':'INT','athletics':'STR','deception':'CHA','history':'INT','insight':'WIS','intimidation':'CHA','investigation':'INT','medicine':'WIS','nature':'INT','perception':'WIS','performance':'CHA','persuasion':'CHA','religion':'INT','sleightofhand': 'DEX','stealth': 'DEX','survival':'WIS'}
        for skill in self.skills:
            self.skills[skill] = self.get_modifyer(self.stats[self.skills[skill]])
            
            if skill in self.expertise.lower(): # skills gain *2 prof
                self.skills[skill] += self.proficiency * 2

            elif skill in self.skillsProf.lower(): # skills gain prof
                self.skills[skill] += self.proficiency


    def cleanup(self, *lines):
        '''
        Used to clean up inputs for data
        '''
        #print(lines[0][0])
        info = {
            'Name': self.name,
            'Main Class': self.mainClass,
            "Total Level": self.level,
            'AC': self.AC,
            'HP': self.maxHP,
            'Speed': self.speed,
            'STR': self.stats['STR'],
            'DEX': self.stats['DEX'],
            'CON': self.stats['CON'],
            'INT': self.stats['INT'],
            'WIS': self.stats['WIS'],
            'CHA': self.stats['CHA'],
            'Skills': self.skillsProf,
            'Expertise': self.expertise,
            'URL': self.url
            }


        msg = (' '.join(lines[0][0]) + ' ').split('|')[1:] # i dont fully know why it needs the [0][0] but from something it gains 2 lvls
        print(msg)
        for a in msg:
            #print(a)
            splt = a.index(': ')
            print(a[:splt], a[splt+2:])
            if (a[splt+2:splt+4] != '__') and (a[splt+2:] != ' ') and (a[splt+1:] != ' '):
                info[a[:splt]] = a[splt+2:-1]


        dic = {"name":info["Name"], 
        'url':info['URL'], 
        'mainClass':info['Main Class'].lower(), 
        'level':int(info["Total Level"]), 
        'stats':{'STR': int(info['STR']), 'DEX' : int(info['DEX']), 'CON' : int(info['CON']), 'INT' : int(info['INT']), 'WIS' : int(info['WIS']), 'CHA' : int(info['CHA'])}, 
        'AC':int(info['AC']), 
        'curHP':int(info['HP']), 
        'maxHP':int(info['HP']), 
        'speed':info['Speed'], 
        'proficiency':self.proficiency,
        'cash':self.cash,
        'invintory':self.invintory,
        'spellList':self.spellList,
        'spellSlots':self.spellSlots,
        'spellSlotsMax':self.spellSlotsMax,
        'spellAttack':self.spellAttack,
        'spellSave':self.spellSave,
        'customRolls':self.customRolls,
        'skillsProf':info["Skills"],
        'expertise':info['Expertise'],
        'skills':self.skills,
        }

        print(dic)
        return(dic)


    def createChar(self, *lines):
        data = self.cleanup(lines)
        self.loadChar(data)






class Player(commands.Cog):
    def __init__(self,bot, data = None):
        self.bot = bot
        
        self.users = {}
        self.allCharacters = {}
        try:
            self.users = Load('ActiveUsing')
            self.allCharacters = Load('Character')

            # get the achaul classes
            for name in self.allCharacters: # may be removed
                for char in self.allCharacters[name]:
                    self.allCharacters[name][char] = Character(self.allCharacters[name][char])
        
        except Exception as e:
            print(f"Flaw in loading: {e}")

        
        self.saveTimer.start()



    def cog_unload(self):
        self.saveTimer.cancel()

    @tasks.loop(minutes=10.0)
    async def saveTimer(self):
        if not self.bot.is_closed():
            print('Saved')

            if Load('ActiveUsing') != self.users:
                Save('ActiveUsing',self.users)
                await self.bot.get_user(275002179763306517).send("Saved Active using!")

            saveable = {}
            for name in self.allCharacters:
                for char in self.allCharacters[name]:
                    if "First one!" not in char:
                        try:
                            saveable[name][char] = self.allCharacters[name][char].getSaveable()
                        except:
                            saveable[name] = {char: self.allCharacters[name][char].getSaveable()}


            
            if Load('Character') != saveable:
                Save('Character',saveable)
                await self.bot.get_user(275002179763306517).send("Saved character lists!")


    @saveTimer.before_loop
    async def before_presence_task(self):
        await self.bot.wait_until_ready()

    '''
    # an example event
    @commands.Cog.listener()
    await def on_ready(self):
        print('IEEEEEEEEEEEEEEEE')
    #'''
    
    @commands.command()
    async def saveChar(self, ctx):
        '''
        Saves all characters to storage for reloading later
        []saveChar
        '''
        #using = {}
        #for char in self.users:
        #    using[char] = self.users[char]

        saveable = {}
        for name in self.allCharacters:
            for char in self.allCharacters[name]:
                if "First one!" not in char:
                    try:
                        saveable[name][char] = self.allCharacters[name][char].getSaveable()
                    except:
                        saveable[name] = {char: self.allCharacters[name][char].getSaveable()}
            

        Save('ActiveUsing',self.users)
        Save('Character',saveable)
        await sendmsg(ctx, "Characters saved!")


    # NOT DONE!
    @commands.command()
    async def kill(self,ctx, *name):
        '''
        Removes your character from the save list and unbines you to them
        NOTE YOU CANNOT GET THIS BACK!!
        []kill `name`
        '''
        name = ' '.join(name).capitalize()
        try:
            del self.allCharacters[str(ctx.author)][name]
            await sendmsg(ctx,f'Goodbye {name}. RIP.')
        except:
            await sendmsg(ctx, f'No character by name {name}!')


    async def getCurrent(self,ctx):
        '''
        Used to get something for other sections in turtle
        '''
        try:
            current = self.allCharacters[str(ctx.author)][self.users[str(ctx.author)]]
            '''
            if type(current) == dict: # faster load times on startup?
                self.allCharacters[str(ctx.author)+self.users[str(ctx.author)]] = Character(self.allCharacters[self.allCharacters[str(ctx.author)+self.users[str(ctx.author)]]])
                current = self.allCharacters[str(ctx.author)+self.users[str(ctx.author)]]
            '''
        except KeyError:
            await sendmsg(ctx,"You havent taken on a character yet!")
            await sendmsg(ctx,"Do []player __CHARACTER_NAME!__")
            await sendmsg(ctx,"**OR** if you havent made a character yet do []character!")

            tmp = Character()
            try:
                self.allCharacters[str(ctx.author)][tmp.name] = tmp
            except:
                self.allCharacters[str(ctx.author)] = {tmp.name: tmp}
            #self.allCharacters[str(ctx.author)] = self.allCharacters[str(ctx.author)].createChar(args)
            self.users[str(ctx.author)] = self.allCharacters[str(ctx.author)][tmp.name].name
            current = self.allCharacters[str(ctx.author)][self.users[str(ctx.author)]]

        except Exception as e:
            await sendmsg(ctx,"Op something went wrong.")
            print('Error: ', e)
            

        return(current)
        

    #makes a new character for someone or updates a current one
    @commands.command()
    async def character(self, ctx, *args):
        '''
        Makes/updates characters
        []character (gives basic steps for making a char)
        []character `Stuff` (makes a character, use []character to know more)
        []character update (gives you info on updating your char)
        []character list (gives you all the current characters you have made)
        '''
        if (len(args) == 1) and ('update' in args[0]):
            info = await self.getCurrent(ctx)
            stuff = f"""```\n[]character |Name: {info.name}\n|Main Class: {info.mainClass}\n|Total Level: {info.level}\n|AC: {info.AC}\n|HP: {info.maxHP}\n|Speed: {info.speed}\n|STR: {info.stats["STR"]}\n|DEX: {info.stats["DEX"]}\n|CON: {info.stats["CON"]}\n|INT: {info.stats["INT"]}\n|WIS: {info.stats["WIS"]}\n|CHA: {info.stats["CHA"]}\n|Skills: {info.skillsProf}\n|Expertise: {info.expertise}\n|URL: {info.url}```"""
            await sendmsg(ctx,stuff)
            await sendmsg(ctx,"Copy the above update it and send back") # with []player

        elif (len(args) == 1) and ('list' in args[0]):
            current = await self.getCurrent(ctx) # failsafe
            people=discord.Embed(title=f"{str(ctx.author)}'s Characters:", description=f"Currently using: {current.name}", color=0x25ae11)
            #embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
            for char in self.allCharacters[str(ctx.author)]:
                if char != "First one!":
                    char = self.allCharacters[str(ctx.author)][char]
                    people.add_field(name=char.name, value=f"{char.mainClass.capitalize()}: Level {char.level}", inline=True)
            
            await sendmsg(ctx,embed=people) # list

        elif len(args) != 0: # MAKING NEW OR UPDATEING CHARACTER
            
            current = await self.getCurrent(ctx) # For updating a character
            
            tmp = Character() # for making a new character
            tmp.createChar(args)

            if tmp.name == current.name: # determane weather this is an update or new char
                current.createChar(args) # update
            else:
                current = tmp # for new char

            #self.allCharacters[str(ctx.author)+tmp.name] = tmp 
            #self.allCharacters[str(ctx.author)] = self.allCharacters[str(ctx.author)].createChar(args)

            self.allCharacters[str(ctx.author)][current.name] = current # just update the data if needbe, mostly for new char
            self.users[str(ctx.author)] = self.allCharacters[str(ctx.author)][current.name].name # incase its a name change
            await self.player(ctx)

        else:
            stuff = """```\n[]character |Name: __\n|Main Class: __\n|Total Level: __\n|AC: __\n|HP: __\n|Speed: __ft\n|STR: __\n|DEX: __\n|CON: __\n|INT: __\n|WIS: __\n|CHA: __\n|Skills: __\n|Expertise: __\n|URL: __```"""
            await sendmsg(ctx,stuff)
            await sendmsg(ctx,"Copy the above then replace __ and send back") # with []player
            await sendmsg(ctx,"**If you dont have anything for that slot leave it blank __(EXCEPT NAME!!)__**")

        
    # this is to show the character
    @commands.command()
    async def player(self, ctx, *args):
        '''
        Shows your current player, updates player, or links character. Automaticly makes one if you dont have one
        []player (show)
        []player update (shows update info)
        []player `name` (links you to a character)
        '''
        #info = Load(('Players'+FilesType+str(ctx.author).replace('#','_').replace(' ','') + args[0].lower().replace(' ','')))
        if len(args) == 0:
            # for testing
            current = await self.getCurrent(ctx)
            '''
            try:
                current = self.allCharacters[str(ctx.author)+self.users[str(ctx.author)]]
            except:
                tmp = Character()
                self.allCharacters[str(ctx.author)+tmp.name] = tmp 
                self.users = self.allCharacters[str(ctx.author)].name
            '''   

            if current.curHP > current.maxHP: # for overheal
                overheal = f' + {current.curHP-current.maxHP} Temp'
            else:
                overheal = ''

            person=discord.Embed(title=current.name.capitalize(), url=current.url, description=f"{current.mainClass.capitalize()} : Level {current.level}", color=0x25ae11)
            #embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
            person.add_field(name="AC", value=current.AC, inline=True)
            person.add_field(name="HP", value=f'{current.curHP}/{current.maxHP}{overheal}', inline=True)
            person.add_field(name="Speed", value=current.speed, inline=True)
            person.add_field(name="Proficiency Bonus", value=current.proficiency, inline=False)
            person.add_field(name="STR", value=current.stats['STR'], inline=True)
            person.add_field(name="DEX", value=current.stats['DEX'], inline=True)
            person.add_field(name="CON", value=current.stats['CON'], inline=True)
            person.add_field(name="INT", value=current.stats['INT'], inline=True)
            person.add_field(name="WIS", value=current.stats['WIS'], inline=True)
            person.add_field(name="CHA", value=current.stats['CHA'], inline=True)

            #if self.Main Class'][:-1].lower() in magic:
            person.add_field(name="Spell Save", value=current.spellSave, inline=False)
            person.add_field(name="Spell Attack", value=current.spellAttack, inline=False)
            
            person.set_footer(text=f"Gold: {current.cash/100}")
            
            await ctx.send(embed = person)


        elif args[0] == 'update':
            info = await self.getCurrent(ctx)
            stuff = f"""```\n[]character |Name: {info.name}\n|Main Class: {info.mainClass}\n|Total Level: {info.level}\n|AC: {info.AC}\n|HP: {info.maxHP}\n|Speed: {info.speed}\n|STR: {info.stats["STR"]}\n|DEX: {info.stats["DEX"]}\n|CON: {info.stats["CON"]}\n|INT: {info.stats["INT"]}\n|WIS: {info.stats["WIS"]}\n|CHA: {info.stats["CHA"]}\n|Skills: {info.skillsProf}\n|Expertise: {info.expertise}\n|URL: {info.url}```"""
            await sendmsg(ctx,stuff)
            await sendmsg(ctx,"Copy the above update it and send back") # with []player
        else:

            name = ' '.join(args).capitalize()
            try:
                self.users[str(ctx.author)] = self.allCharacters[str(ctx.author)][name].name # link to a new char
                await sendmsg(ctx, f'Linked to {name}!') 
                await self.player(ctx)
            except KeyError:
                await sendmsg(ctx, f'Linkng failed! No Char named {name}!') 
            except Exception as e:
                await sendmsg(ctx,"Linking Error: {}".format(e))
                print(e)


    # HP BABY!
    @commands.command()
    async def hp(self, ctx, damage = 0, tipe = None):
        '''
        Heal or Hurt or just show current hp
        []hp (shows current hp)
        []hp `12` (heal 12)
        []hp `-12` (hurt -12)
        '''
        try:
            current = await self.getCurrent(ctx)

            print(str(damage).lower())

            if current.curHP < 0: # reset the heals
                current.curHP = 0

            if (str(damage).lower() == 'max') or (str(damage).lower() == 'rest') or (str(damage).lower() == 'long rest'): # Live
                damage = current.maxHP - current.curHP

            elif (str(damage).lower() == 'none') or (str(damage).lower() == 'dead') or (str(damage).lower() == 'down'): # kill
                damage = current.curHP

            else:
                damage = int(damage) # failsafe


                if tipe == None:
                    if (current.curHP + damage) > current.maxHP: # cant overheal
                        damage -= ((current.curHP + damage) - current.maxHP) # math


                    pain = current.tempHP + damage # a temp var used to deal with damage
                    if damage < 0:
                        current.tempHP += damage # MY SHIELD!
                    else:
                        current.curHP += damage # heal

                    if pain < 0:
                        current.curHP += pain # hurt
                else:
                    current.tempHP += damage
                


            if current.tempHP > 0: # for overheal
                overheal = f' + {current.tempHP} Temp'
            else:
                overheal = ''

            person=discord.Embed(title=current.name.capitalize(), url=current.url, color=0xf0fc03)
            person.add_field(name="HP", value=f"{current.curHP}/{current.maxHP}{overheal}", inline=True)

            if damage < 0:
                person.set_footer(text=f"Dammage taken: {damage}")
            elif damage > 0:
                person.set_footer(text=f"Dammage healed: {damage}")
            
            await ctx.send(embed = person)
            
        except KeyError:
            await sendmsg(ctx,"You havent taken on a character yet!")
            await sendmsg(ctx,"Do []player CHARACTER_NAME!")
            await sendmsg(ctx,"OR if you havent made a character yet do []character!")
        except Exception as e:
            await sendmsg(ctx,"Op something went wrong.")
            print('Error: ', e)


    # Holy sounds
    @commands.command()
    async def heal(self, ctx, damage = 0, tipe = None):
        '''
        Heal yaself
        []heal `12` (heald ya 12)
        '''
        self.hp(ctx, damage, tipe)


    # Demonic sounds
    @commands.command()
    async def hurt(self, ctx, damage = 0, tipe = None):
        '''
        Hurt yaself
        []hurt `12` (hurt ya 12)
        '''
        self.hp(ctx, -1 * damage, tipe)
        

    # GOOOOOLLLLDDDDD
    # CASH MONY BABY! 
    @commands.command()
    async def gold(self, ctx, val = 0):
        """
        Change/show your cash count!
        []gold (shows your cash amount)
        []gold `12` (gives you 12 gold) 
        []gold `-12` (takes away 12 gold)
        []gold `1.23` (gives you 1 gold, 2 silver, 3 copper)
        """
        try:
            current = await self.getCurrent(ctx)
            #amount = float(val)
            print(val)


            #gold = int(amount) # off the idea that gold = 1
            #print(round((amount-gold),2))
            #silver = int(round((amount-gold),2)*10) # off the idea that silver = .1
            #copper = int(round((amount-gold-(silver/10)),3)*100) # off the idea that copper = .01

            #print(gold,silver,copper)

            current.cash += val*100 # change values
            #'''

            cash = discord.Embed(title=f"{current.name}'s Cash Money", description=f"Gold: **{int(current.cash/100)}**", color=0xedd030)
                
            if int(str(current.cash)[-2]) > 0:
                cash.add_field(name=f"Silver: `{int(str(current.cash)[-2])}`", value="____", inline=True)
            if int(str(current.cash)[-1]) > 0:
                cash.add_field(name=f"Copper: `{int(str(current.cash)[-1])}`", value="____", inline=True)

            if val != 0:
                cash.set_footer(text=f"Cash Change: {val}")

            await sendmsg(ctx, embed=cash)

        except Exception as e:
            print(e)
            await sendmsg(ctx, "GOLD ERROR: {}".format(e))    


    # Less impressive cash
    @commands.command()
    async def silver(self, ctx, val = 0.0):
        """
        Change your silver count!
        []silver `amount` (change silver by amount) 
        """
        await self.gold(ctx,float(val/10))
    # even less impresive cash
    @commands.command()
    async def copper(self, ctx, val = 0.0):
        """
        Change your copper count!
        []copper `amount` (change copper by amount) 
        """
        await self.gold(ctx,float(val/100))



def setup(bot):
    bot.add_cog(Player(bot))