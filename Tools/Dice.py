'''
Dice stuff
'''

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### imports Tools ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#this is so that the IDE doesent yell at me for not having this in the file. Yes its that annoying
if __name__ == "__main__":
    #import os, subprocess, random, asyncio
    import discord
    from discord.ext import commands
    bot = commands.Bot(";")
    bertle = 275002179763306517

    

from random import randrange

try:
    from JTools import find_all #, flattenList, cutUp
except:
    import os
    os.system("python3 -m pip install git+https://github.com/Quiltic/JTools.git")
    from JTools import find_all #, flattenList, cutUp


def flattenList(lst): # in newer version of Jtools but no yet implementinted into git 
    out = []
    for a in lst:
        if type(a) == list:
            out += flattenList(a)
            #for b in a:
            #    out.append(b)
        else:
            out.append(a)
    return(out)

def cutUp(string, lst): # in newer version of Jtools but no yet implementinted into git 
    '''
    Givin a string cut it up at locations in lst
    cutUp('hi',[1]) : gives ['h','i']
    '''
    lst = [0] + lst + [len(string)] # to get the begining and end
    new = [string[lst[a-1]:lst[a]] for a in range(1,len(lst))] # split it up

    if new[0] == '': # when the first val of lst was also a 0 (lst origin == [0,3] then it would be [0,0,...])
        new = new[1:] # remove '' made by this

    if new[-1] == '': # when the last val of lst was also a max len (lst origin == [0,3] then it would be [...,3,3])
        new = new[:-1] # remove '' made by this

    return(new)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Dice Tools ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


#random number
def randomnum(low,high):
    return randrange(low,high+1)


# dice dice baby
def diceBase(*args):
    '''
    This is used to split up all the segments in an input
    returns {'total': #, dicetyps: [vals], dicetyps: [vals], exct}
    '''
    data = {'total': 0}

    if len(args) != 0:
        inpt = ''.join(args).replace(' ','').lower().replace('--','-').replace('-+','-') # achual input
        #print(inpt)

        if 'adv' in inpt: # advantage
            inpt = inpt.replace('adv','')
            if inpt == '': # for []r adv
                data['try1'] = diceBase(*())
                data['try2'] = diceBase(*())
            else:
                data['try1'] = diceBase(inpt)
                data['try2'] = diceBase(inpt)
            data['total'] = max(data['try1']['total'],data['try2']['total'])

        elif 'dis' in inpt: # disadvantage
            inpt = inpt.replace('dis','')
            if inpt == '': # for []r dis
                data['try1'] = diceBase(*())
                data['try2'] = diceBase(*())
            else:
                data['try1'] = diceBase(inpt)
                data['try2'] = diceBase(inpt)

            data['total'] = min(data['try1']['total'],data['try2']['total'])
        
        
        else: # normal rolls

            if ('d' not in inpt): # basicly if you have ('+3') as input
                inpt = '1d20' + inpt 

            tps = ['+','-','*','/'] # types of things in the list that we want to look for
            loc = flattenList([find_all(inpt,a) for a in tps]) # all of the things get made into list (probably easer way fo finding this but eah)
            loc.sort() # sort doesent return anything for some reason so this needs its own line
            #print(loc)

            
            inpt = cutUp(inpt, loc) # we need all of the segments individualy
            
            #print(inpt)
            
            specialTypes = ['strength','dexterity','constitution','intelligence','wisdom','charisma','acrobatics','animalhandling','arcana','athletics','deception','history','insight','intimidation','investigation','medicine','nature','perception','performance','persuasion','religion','sleightofhand','stealth','survival'] # thease are all skills in D&D... 
            
            for a in inpt:
                if 'd' in a:
                    d = diceRoller(a) # temp variabel
                    data[d[0]] = d[1]
                    data['total'] += sum(d[1]) # yay totals
                
                elif a in tps:# fail safe
                    pass

                elif a not in specialTypes: # fail safe but mostly for +, -
                    data[a] = [int(a)] 
                    data['total'] += int(a) # yay totals
                
            #print(data)

    else: # flat d20
        data['1d20'] = [randomnum(1,20)]
        data['total'] += data['1d20'][0] # yay totals

    return(data)


#
def diceRoller(string):
    '''
    This is for dice rolling IE 1d6 4d12 exct
    '''
    data = string.split('d') # get a split of the dice
    #print(data)
    mult = 1 # for negitives
    if '-' in data[0]:
        mult = -1

    data[0] = data[0].replace('-','').replace('+','').replace('*','').replace('/','') # cleanup

    vals = [mult*randomnum(1,int(data[1])) for _ in range(int(data[0]))] # roll the dice alot

    return((string,vals))


def quick_combiner(roll):
    '''
    takes in a roll and gives what it should say
    '''
    say = '' # what say you
    for a in roll:
        if (a != 'total') and (a != 'speak'): # so we dont edit the wrong things
            say += ' ' + a # space
            if 'd' in a:
                val = a.index('d') # find val
                val = ['{}]'.format(a[val+1:]), '**{}**]'.format(a[val+1:]),'{}, '.format(a[val+1:]), '**{}**, '.format(a[val+1:])] # replace vals with bold
                say += ' ' + str(roll[a]).replace('1]','**1**]').replace(' 1,',' **1**,').replace(val[0],val[1]).replace(val[2],val[3]) # true replace
    return(say)


async def bitReplacer(ctx, using, *args):
    '''
    Corrects the values for special types when rolling
    '''
    specialTypes = ['strength','dexterity','constitution','intelligence','wisdom','charisma','acrobatics','animalhandling','arcana','athletics','deception','history','insight','intimidation','investigation','medicine','nature','perception','performance','persuasion','religion','sleightofhand','stealth','survival'] # thease are all skills in D&D... 
    try:
        things = list(args) # make it into a list for ease of acsess
        for a in range(len(args)): # iterate through the list
            for b in specialTypes: # if it is a special type
                
                temp = args[a].lower().replace('+','').replace('-','').replace('*','').replace('/','') # cleanup

                if temp == '': # empty val. strangely needed
                    pass
                elif temp in "proficiency": # if its the word proficiency
                    things[a] = str(using[str(ctx.author)]['Proficiency']) # replace

                    if '-' not in things[a]:
                        things[a] = '+'+things[a] # no + is there when origionaly dealing with thing
                    break # dont need to keep looking onwards

                elif temp in b: # in specialtypes 
                    #print(b)
                    things[a] = str(using[str(ctx.author)]['Skills'][b]) # replace
                    #print('hi')
                    if '-' not in things[a]:
                        things[a] = '+'+things[a] # no + is there when origionaly dealing with thing

                    await ctx.send("Rolling for {}! {}".format(b,things[a])) # eah might as well
                    break # dont need to keep looking onwards
                    #print('hi')
    except KeyError:
        return(None) # wrong skill names
        #await sendmsg(ctx,"Improper skill name! {}".format(args[a]))
    except Exception as e:
        print(type(e),e)
    
    return(things)



'''
def diceCleanup(stuff):
    print(stuff)
    stuff['speak'] = stuff['speak'].replace('1]','**1**]').replace('1,','**1**,')
    #print(stuff['speak'])
    iteration = 0
    for a in stuff:
        if (a != 'total') and (a != 'speak'):
            try:
                val = a.index('d')
                print(stuff['speak'][iteration+1:])
                if val:
                    #[]r 6d6 +4d4 +3
                    print('val',a[val+1:])
                    val = ['{}]'.format(a[val+1:]), '**{}**]'.format(a[val+1:]),'{},'.format(a[val+1:]), '**{}**,'.format(a[val+1:])]
                    print(stuff['speak'][iteration+1:stuff['speak'][iteration+1:].index(']')+2].replace(val[0],val[1]).replace(val[2],val[3]))
                    stuff['speak'] = stuff['speak'][:iteration+2] + stuff['speak'][iteration+1:stuff['speak'][iteration+1:].index(']')+2].replace(val[0],val[1]).replace(val[2],val[3]) + stuff['speak'][stuff['speak'][iteration+1:].index(']')+1:]

                    #print('iter',iteration)
                    iteration = str(stuff['speak'][iteration+1:]).index(']')+1
                    print('iter',iteration)
                    
                    
            except Exception as e:
                print(type(e),e)
    #print(stuff['speak'])
    return(stuff['speak'])

'''
'''
[]customroll |Name: random
|Main Roll: 1d4
|Second Roll: __
|Table info (do * # DOES):
* 1 dance
* 2 fly
* 3 jump
* 4 `1d4` cold damage
'''



'''
[]customroll |Name: spear
|Main Roll: 1d20 + str + prof
|Second Roll: 1d6 + str
|Table info (do * # DOES):
* __ __
'''
def CustomRollMaker(ctx,*args):
    '''
    make custom rolls
    returns: {'Name': '', 'Main Roll': '1d20', 'Second Roll': None, 'Table info (do * # DOES)':{}} # base
    '''
    custRoll = {'Name': '', 'Main Roll': '1d20', 'Second Roll': None, 'Table info (do * # DOES)':{}} # base
    msg = ' '.join(args).split('|')[1:] # splitter
    print(msg)

    for a in msg:
        #print(a)
        splt = a.index(': ') # get the split
        #print(a[:splt], a[splt+2:])
        if a[:splt] == 'Table info (do * # DOES)': # ignore this part of the table
            #print('hi)')
            tablestuff = a[splt+2:].split('* ') # get the part we want
            #print(tablestuff)
            for data in tablestuff: # for table stuff mostly cleanup
                if data != '':
                    splt = data.index(' ')
                    custRoll['Table info (do * # DOES)'][str(data[:splt])] = str(data[splt+1:])

        elif (a[splt+2:-1] != '__') and (a[splt+2:-1] != '___'): # more stuff related to cleanup for main/sub rolls
            custRoll[a[:splt]] = a[splt+2:-1].lower()
        
    print(custRoll)
    return(custRoll)


# for testing
if __name__ == "__main__":
    '''
    Tests
    '''
    print(diceBase(*()))
    print('\n'*2)
    print(diceBase(*('+1 ')))
    print('\n'*2)
    print(diceBase(*('4d6 ', '+1 ')))
    print('\n'*2)
    print(diceBase(*('4d6 ', '+1 ','-1d4')))
    print('\n'*2)
    print(diceBase(*('adv ')))
    print('\n'*2)
    print(diceBase(*('adv ','+1 ')))
    print('\n'*2)
    print(diceBase(*('adv ','4d6 ', '+1 ','-1d4')))


    roll = {'total': 31, '6d6': [6, 2, 1, 6, 3, 5], '+4d4': [2, 1, 1, 4], '+3': [3], 'speak': ' 6d6 [4, 6, 1, 6, 3, 5] +4d4 [4, 1, 1, 3] +3'}
    #diceCleanup(roll)


'''
# dice dice baby
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
'''