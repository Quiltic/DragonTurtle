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
        inpt = ''.join(args).replace(' ','').lower() # achual input
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
            tps = ['+','-','*','/'] # types of things in the list that we want to look for
            loc = flattenList([find_all(inpt,a) for a in tps]) # all of the things get made into list (probably easer way fo finding this but eah)
            loc.sort() # sort doesent return anything for some reason so this needs its own line
            #print(loc)

            inpt = cutUp(inpt, loc) # we need all of the segments individualy
            if (len(inpt) == 1) and ('d' not in inpt[0]): # basicly if you have ('+3') as input
                inpt = ['1d20'] + inpt 
            #print(inpt)
            
            specialTypes = ['strength','dexterity','constitution','intelligence','wisdom','charisma','acrobatics','animalhandling','arcana','athletics','deception','history','insight','intimidation','investigation','medicine','nature','perception','performance','persuasion','religion','sleightofhand','stealth','survival'] # thease are all skills in D&D... 
            
            for a in inpt:
                if 'd' in a:
                    d = diceRoller(a) # temp variabel
                    data[d[0]] = d[1]
                    data['total'] += sum(d[1]) # yay totals

                elif a not in specialTypes: # for +, -, /, *
                    data[a] = [int(a)] 
                    data['total'] += int(a) # yay totals
                
                else:
                    pass # oh god not yet

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
    data = string.split('d')
    #print(data)
    mult = 1 # for negitives
    if '-' in data[0]:
        mult = -1

    data[0] = data[0].replace('-','').replace('+','').replace('*','').replace('/','') # cleanup

    vals = [mult*randomnum(1,int(data[1])) for _ in range(int(data[0]))]

    return((string,vals))



# for testing
if __name__ == "__main__":
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