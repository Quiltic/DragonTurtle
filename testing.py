from random import randrange

'''
This is a file to make test stuffs in.
'''

def randomnum(low,high):
    return randrange(low,high+1)

val = 123.4
gold = int(val)
silver = int((val-gold)*10)
copper = int((val-gold-(silver/10))*100)
print(gold,silver,copper)

"""
cards = ['A♠', '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♡', '2♡', '3♡', '4♡', '5♡', '6♡', '7♡', '8♡', '9♡', '10♡', 'J♡', 'Q♡', 'K♡', 'A♢', '2♢', '3♢', '4♢', '5♢', '6♢', '7♢', '8♢', '9♢', '10♢', 'J♢', 'Q♢', 'K♢', 'A♣', '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣']
cards = cards + cards + cards + cards
print(cards)
"""
"""

def shuffle(deck, times = 4, amount = 26):
    '''
    suffles a dec
    shuffle(deck, times = 4, amount = 20) : gives a deck randomly suffled
    shuffle(deck, 6) better shuffle
    shuffle(deck, 12, 40) insane shuffle
    '''
    cards = list(deck)
    #print(cards)
    for _ in range(times):
        for _ in range(amount):
            point = randomnum(0,len(cards)-1)
            difpoint = randomnum(0,len(cards)-1)
            difcard = cards[point]
            cards[point] = cards[difpoint]
            cards[difpoint] = difcard
    
    #print(cards)
    return(cards)

shuffle(cards)

'''
tpe = ['♠', '♡', '♢', '♣']
lst = ['A' ,'2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

newlst = []
for a in tpe:
    for b in lst:
        newlst.append(b+a)

print(newlst)
'''
"""