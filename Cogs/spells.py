'''
This is both an example cog and a helper cog for me.
'''
import discord, math
from discord.ext import commands
from Tools import sendmsg
from JTools import find_all, Load, Save, spellCheck


class Spells(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        #try:
        self.SpellList = Load('Spells') # load a spellbook
        #except:
        #    print("Couldent load: {}. Making new file.".format('Spells')) # Error on spellbook
        #    self.SpellList = {} # empty spell list

    # gives a spell from a spellbook or adds a spell to a spellbook if not there
    def SpellBook(self, spellname = 'ALL', BOOKNAME = "Spells", ADD = True):
        '''
        Gives a spell from a spell book if posable otherwise from page
        SpellBook(spellname = 'ALL', BOOKNAME = "Spells", ADD = True): gives a dict of spell data : saves a spellbook
        SpellBook("Mage Hand"): gives dict data on mage hand : saves a spellbook named Spells and adds mage hand to book if not already there
        SpellBook(): gives a dict containing every spell in the book
        SpellBook("Find familiar", "Bertle"): gives dict data on find familiar : saves/loads a spellbook named Bertle and adds mage hand to book if not already there
        SpellBook("Find familiar", "Bertle", False): gives dict data on find familiar : loads a spellbook named Bertle
        SpellBook(["Find familiar", "Mage Hand"]): gives dict data on find familiar and Mage hand in a list : loads a spellbook named Spells
        '''
        #print(self.SpellList)

        if spellname == 'ALL': # gives entire spellList
            return(self.SpellList)

        spells = [] # the return for the spells
        if type(spellname) != list: # if you give it just a name
            spellname = [spellname] # make into list

        for sp in spellname: # go though every spell in list
            sp = sp.lower().replace(' ','-') # NO SPACES! NO CAPS!
            sp = spellCheck(sp,self.SpellList)

            try:
                spells.append(self.SpellList[sp]) # if spell in list add it to spells
            except:
                try:
                    spells.append(self.SpellList[sp+'-ritual']) # try again as a ritual
                except:
                    spells.append(None) # could not find it

                # This is old code and doesent work on the pi. I will leave this however for when i want to fix this
                #SpellList[sp] = findSpell(sp) # spell not in list look it up online
                #Save(BOOKNAME,SpellList) # Save book
                #spells.append(SpellList[sp]) # Add to return spells
        
        return(spells[0] if len(spells) == 1 else spells) # return all spells asked for in a list or as a dict if you ask for one


    # just a nice way to print out the spell
    def cleanPrintS(self, spells):
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




    
    # cast a spell at some level
    @commands.command()
    async def cast(self, ctx, *spell):
        '''
        Cast a spell with all the pirks of casting.
        '''
        user = await self.bot.get_cog('Player').getCurrent(ctx) #data for use of stuff later on
        dice = self.bot.get_cog('Dice').OutsideRoll
        pritty = self.bot.get_cog('Dice').pritify_helper
        try:
            upcharge = int(spell[-1])
            spell = spell[:-1]
            print(upcharge)
        except:
            #print(e)
            upcharge = 0

        spell = ' '.join(spell).lower()

        async with ctx.channel.typing():
            await ctx.message.add_reaction("📖")
            #await sendmsg(ctx,"Refactoring spell list")

            #reloadSpellList()
            data = self.SpellBook(spell) # get spell
            
            if (data != None) and (data != 'None'):
                print("Found")

                try:
                    # if you need to roll to hit
                    if (data['fight']['type'] != 'area') and (not data['fight']['heal']):
                        print(*('+'+str(user.spellAttack)))
                        hitstuff = await dice(ctx,*(str(user.spellAttack))) # damage roll
                        print(f'hit {hitstuff}')
                        spl=discord.Embed(title=data['name'], url=data['url'], description=f"**Rolled To Hit**: {pritty(hitstuff['dice1'])[2:]} = `{hitstuff['dice1'][2]}`", color=0x07a7af)
                    else:
                        spl=discord.Embed(title=data['name'], url=data['url'], description=f"School: {data['school']}", color=0x07a7af)
                    
                    '''
                    UPCASTING!
                    ITS ACHUAL HELL!
                    DONT LOOK TO HARD
                    '''
                    try:
                        if len(data['fight']['damage']):
                            if data['cast']['level'] == 'Cantrip':
                                if data['fight']['damage'][-1][0][data['fight']['damage'][-1][0].index('d'):] == data['fight']['higherLvl'][data['fight']['higherLvl'].index('d'):]:
                                    increase = int(data['fight']['higherLvl'][:data['fight']['higherLvl'].index('d')]) * math.floor((int(user.level)+1)/6) # ups at lvl 5, 11, & 17 so this does the charm
                                    #print(int(data['fight']['damage'][-1][0][:data['fight']['damage'][-1][0].index('d')]),int(data['fight']['higherLvl'][:data['fight']['higherLvl'].index('d')])*(upcharge-int(data['cast']['level'])))
                                    data['fight']['damage'][-1][0] = str(int(data['fight']['damage'][-1][0][:data['fight']['damage'][-1][0].index('d')]) + increase) + data['fight']['damage'][-1][0][data['fight']['damage'][-1][0].index('d'):]

                            elif upcharge > int(data['cast']['level']):
                                
                                # So there is an annoying glitch that becasue of the line below being in healing spells it wont upcast
                                # .replace(" + spellcasting_ability_modifier",'')
                                
                                print(data['fight']['damage'][-1][0][data['fight']['damage'][-1][0].index('d'):],data['fight']['higherLvl'][data['fight']['higherLvl'].index('d'):])
                                if data['fight']['damage'][-1][0][data['fight']['damage'][-1][0].index('d'):].replace('O','0').replace(" + spellcasting_ability_modifier",'') == data['fight']['higherLvl'][data['fight']['higherLvl'].index('d'):].replace('O','0').replace(" + spellcasting_ability_modifier",''):
                                    #print(int(data['fight']['damage'][-1][0][:data['fight']['damage'][-1][0].index('d')]),int(data['fight']['higherLvl'][:data['fight']['higherLvl'].index('d')])*(upcharge-int(data['cast']['level'])))
                                    data['fight']['damage'][-1][0] = str(int(data['fight']['damage'][-1][0][:data['fight']['damage'][-1][0].index('d')].replace('O','0').replace(" + spellcasting_ability_modifier",'')) + int(data['fight']['higherLvl'][:data['fight']['higherLvl'].index('d')].replace('O','0').replace(" + spellcasting_ability_modifier",''))*(upcharge-int(data['cast']['level']))) + data['fight']['damage'][-1][0][data['fight']['damage'][-1][0].index('d'):]
                                #data['fight']['damage'][-1] will be increased?

                                
                                
                    except:
                        pass

                    print(data['fight']['damage'])
                    # damage
                    dmg = 0 # total damage
                    for damage in data['fight']['damage']: # for each type of damage
                        try:
                            stuff = await dice(ctx,damage[0]) # this is the raw data
                            dmg += stuff['dice1'][2]
                            
                            try:
                                say = pritty(stuff['dice1'])
                                spl.add_field(name='`' + str(stuff['dice1'][2])+ '` ' + damage[1] + ('' if data['fight']['heal'] else ' damage'), value=f"Rolled: {say[2:]}", inline=True)
                            except IndexError:
                                say = pritty(stuff['dice1'])
                                spl.add_field(name='`' + str(stuff['dice1'][2])+ '` ' + '___ damage', value=f"Rolled: {say[2:]}", inline=True)
                            except Exception as e:
                                await sendmsg(ctx,"Type Damage Error: {}".format(e))
                                
                        except Exception as e:
                            await sendmsg(ctx,"Damage Error: {}".format(e))
                        

                    if dmg > 0: # dont need this if no damage
                        spl.add_field(name=f"Total: `{dmg}` {'healing' if data['fight']['heal'] else 'damage'}.", value=('Nice.' if data['fight']['heal'] else 'Ouch.'), inline=False)
                        spl.description +='\nType: {}'.format(data['fight']['type'])

                    
                    # if there is a type of save
                    if data['fight']['save'] != 'None':
                        spl.description += f"\nType Save: {data['fight']['save']}\nSave: `{user.spellSave}`"
                    

                    # what do
                    if len(data['does']) < 1000:
                        spl.add_field(name="What Do", value=data['does'].replace('|n','\n'), inline=False)
                    else:
                        spl.add_field(name="What Do", value=(data['does'][:1000]).replace('|n','\n'), inline=False)
                
                    #"""

                    if data['cast']['level'] != 'Cantrip': # CANTRIPS
                        spl.set_footer(text=f"Cast at level {max(int(data['cast']['level']),upcharge)}")
                    else:
                        spl.set_footer(text="Cast a Cantrip")

                    await ctx.send(embed = spl)


                    # UNDO A UPCAST THIS IS BECAUSE MAGIC WITH THE SPELL DATA
                    try:
                        if len(data['fight']['damage']):
                            if data['cast']['level'] == 'Cantrip':
                                if data['fight']['damage'][-1][0][data['fight']['damage'][-1][0].index('d'):] == data['fight']['higherLvl'][data['fight']['higherLvl'].index('d'):]:
                                    increase = int(data['fight']['higherLvl'][:data['fight']['higherLvl'].index('d')]) * math.floor((int(user.level)+1)/6) # ups at lvl 5, 11, & 17 so this does the charm
                                    #print(int(data['fight']['damage'][-1][0][:data['fight']['damage'][-1][0].index('d')]),int(data['fight']['higherLvl'][:data['fight']['higherLvl'].index('d')])*(upcharge-int(data['cast']['level'])))
                                    data['fight']['damage'][-1][0] = str(int(data['fight']['damage'][-1][0][:data['fight']['damage'][-1][0].index('d')]) - increase) + data['fight']['damage'][-1][0][data['fight']['damage'][-1][0].index('d'):]

                            elif upcharge > int(data['cast']['level']):
                                
                                # So there is an annoying glitch that becasue of the line below being in healing spells it wont upcast
                                # .replace(" + spellcasting_ability_modifier",'')
                                
                                print(data['fight']['damage'][-1][0][data['fight']['damage'][-1][0].index('d'):],data['fight']['higherLvl'][data['fight']['higherLvl'].index('d'):])
                                if data['fight']['damage'][-1][0][data['fight']['damage'][-1][0].index('d'):].replace('O','0').replace(" + spellcasting_ability_modifier",'') == data['fight']['higherLvl'][data['fight']['higherLvl'].index('d'):].replace('O','0').replace(" + spellcasting_ability_modifier",''):
                                    #print(int(data['fight']['damage'][-1][0][:data['fight']['damage'][-1][0].index('d')]),int(data['fight']['higherLvl'][:data['fight']['higherLvl'].index('d')])*(upcharge-int(data['cast']['level'])))
                                    data['fight']['damage'][-1][0] = str(int(data['fight']['damage'][-1][0][:data['fight']['damage'][-1][0].index('d')].replace('O','0').replace(" + spellcasting_ability_modifier",'')) - int(data['fight']['higherLvl'][:data['fight']['higherLvl'].index('d')].replace('O','0').replace(" + spellcasting_ability_modifier",''))*(upcharge-int(data['cast']['level']))) + data['fight']['damage'][-1][0][data['fight']['damage'][-1][0].index('d'):]
                                #data['fight']['damage'][-1] will be increased?

                                
                                
                    except:
                        pass

                except Exception as e:
                    await sendmsg(ctx,'Cast Error: {}'.format(e))

            else:
                await sendmsg(ctx,"Cant get spell: {}".format(spell))
    

    # spells
    @commands.command()
    async def spell(self, ctx, *spell):
        """This finds and gives a spell. Usage: []spell fireball"""

        spell = ' '.join(spell).lower()

        if spell == '':
            await sendmsg(ctx, "Here is my Source Spellbook: https://www.dnd-spells.com/spell")
        try:
            async with ctx.channel.typing():
                await ctx.message.add_reaction("📖")
                #await sendmsg(ctx,"Refactoring spell list")

                #reloadSpellList()
                data = self.SpellBook(spell)
                
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
                        spl.add_field(name="What Do", value=str(data['does']).replace('|n','\n'), inline=False)
                    else:
                        spl.add_field(name="What Do", value=str(data['does'][:1000]).replace('|n','\n'), inline=False)

                    spl.set_footer(text="Page: {}    |:|    Classes: {}".format(data['page'],data['classes']))
                    await ctx.send(embed = spl)
                else:
                    await sendmsg(ctx,"Cant get spell: {}".format(spell))

        except Exception as e:
            await sendmsg(ctx, f"Spell Error: {e}")
            print(type(e), e)



def setup(bot):
    bot.add_cog(Spells(bot))



