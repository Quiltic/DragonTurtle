'''
This is both an example cog and a helper cog for me.
'''
import discord
from discord.ext import commands
from Tools import sendmsgdirect, sendmsg, randomnum



class Cards(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.decks = {'playing': {'cards':['A♤', '2♤', '3♤', '4♤', '5♤', '6♤', '7♤', '8♤', '9♤', '10♤', 'J♤', 'Q♤', 'K♤', 'A♡', '2♡', '3♡', '4♡', '5♡', '6♡', '7♡', '8♡', '9♡', '10♡', 'J♡', 'Q♡', 'K♡', 'A♢', '2♢', '3♢', '4♢', '5♢', '6♢', '7♢', '8♢', '9♢', '10♢', 'J♢', 'Q♢', 'K♢', 'A♧', '2♧', '3♧', '4♧', '5♧', '6♧', '7♧', '8♧', '9♧', '10♧', 'J♧', 'Q♧', 'K♧'],'total': 52, 'left':52}}
        self.hands = {}
        #await self.shuffle(self,ctx, *name)



    @commands.command()
    async def discard(self,ctx,*cards):
        '''
        This is to be able to discard cards in your hand
        []discard `cards` (discards the cards specifyed)
        []discard `A`(discards all A's in your hand)
        []discard `A♤` (discards the A♤)
        []discard `card` open (says what cards you discarded in the chat you did this in)
        ''' 
        try: # failsafe
            if self.hands[ctx.author.name] == []:
                await sendmsg(ctx, "You have no hand to discard from! Use `[]draw`!")
                return
        except:
            await sendmsg(ctx, "You have no hand to discard from! Use `[]draw`!")
            return

        
        

         # ok so basicly ... yeah
        openn = False
        for cardsV in cards: # iterate though cards asked to remove
            done = False 
            while not done: # iterate if removed card
                done = True # no cards removed
                for card in self.hands[ctx.author.name]: # iterate though hand
                    if cardsV.upper() in card: # if the name is in the hand
                        self.hands[ctx.author.name].remove(card) # remove it
                        done = False # not done
                        break # faster iteration
                
        
        if 'open' in cards:
            print('open')
            await self.hand(ctx,'open')
        else:
            await self.hand(ctx)
        


        
    @commands.command()
    async def hand(self,ctx, openhand = ''):
        '''
        This shows your current hand
        []hand (sends it to you)
        []hand open (shows it in the current chat)
        '''
        try:
            words = ' ,'.join(self.hands[ctx.author.name])
        except:
            await sendmsg(ctx, "You have no hand! Use `[]draw`!")
            return

        if words == '':
            words = 'Empty Hand'
            
        hand=discord.Embed(title=f"{ctx.author.name}'s hand.", description=f"**{words}**")
        
        if 'open' in openhand.lower():
            await sendmsg(ctx,embed = hand)
        else:
            await sendmsgdirect(ctx, embed = hand)
        

    @commands.command()
    async def draw(self, ctx, *data):
        '''
        Draws a card.
        []draw open (throws out a card onto whatever chat the []draw command came from)
        []draw 6 (draws 6 cards)
        []draw 6 open (draws 6 cards openly)
        []draw terrot (draws from the terrot card deck)
        '''
        amount = 1
        openn = False # the cards are to be drawn to the user only
        deck = 'playing'
        for a in data:
            if 'open' in a:
                openn = True # place the cards on the "Table"

            try:
                amount = int(a)
            except:
                pass
        
        data = self.cards(amount,deck) # draw from a deck
        
        try: # give the user the drawn cards Needs to be cleaned up for multiple servers
            self.hands[ctx.author.name] += data['cards']
        except:
            self.hands[ctx.author.name] = data['cards']

        if data['words'] != '':
            hand=discord.Embed(title=f"Drew from {deck.capitalize()} deck.", description=f"Drew **{data['words']}**!")
            hand.set_footer(text=f"{self.decks[deck]['left']}/{self.decks[deck]['total']} cards left. {self.decks[deck]['total']-self.decks[deck]['left']} drawn from deck.")
        else:
            hand=discord.Embed(title=f"Drew from {deck.capitalize()} deck.", description=f"Cant draw no cards left, do []shuffle!")
        '''
        if len(data["cards"]) == 1:
            #hand.set_image(url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Playing_card_spade_2.svg/200px-Playing_card_spade_2.svg.png")
            hand.set_image(url=data['url'])
            print('hi')
        '''
        
        #await sendmsgdirect(ctx, data)
        if openn == True: # should be placed into the chat asked in
            await sendmsg(ctx,embed=hand)
        else:
            await sendmsgdirect(ctx, embed=hand) # sent directly to the user


    @commands.command()
    async def shuffle(self,ctx, *name):
        '''
        shuffles a deck of cards
        []shuffle  (shuffles the playing card deck)
        []shuffle ____ (shuffles the named deck)
        '''
        
        
        # this idea is temparary but the end goal is to remove it based on what server you are in
        for a in self.hands:
            try:
                self.hands[a] = []
            except:
                pass # no hand
        

        try:
            name = ''.join(name).lower()

            if name == '':
                name = 'playing'
            elif name not in self.decks:
                name = 'No' # No deck suffled
            
            self.decks[name]['cards'] = self.shuffleDeck(self.decks[name]['cards'])
            self.decks[name]['left'] = self.decks[name]['total']
            await sendmsg(ctx,f"{name.capitalize()} Deck Shuffled!")
        except Exception as e:
            await sendmsg(ctx,"SHUFFLE ERROR! {}".format(e))    


    def cards(self,amount = 1, deck = 'playing'):
        if amount < 0:
            amount = 1

        data = {'url': '', 'cards':[], 'words':''}

        mathsmagic = self.decks[deck]['total']-self.decks[deck]['left']

        if (mathsmagic + amount ) > self.decks[deck]['total']:
            amount = self.decks[deck]['left']

        data['cards'] = self.decks[deck]['cards'][mathsmagic:(mathsmagic + amount)]
        self.decks[deck]['left'] -= amount


        data['words'] = ' ,'.join(data['cards'])

        
        ''' # ill get back to this but for now its a dead hand
        if (deck == 'playing') and (len(data['cards']) == 1):
            tipes = {'♤':'Playing_card_spade', '♡':'Playing_card_heart', '♢': 'Playing_card_diamond', '♧': 'Playing_card_club'}
            if data['cards'][0][:-1] == 'A':
                tipes = {'A♤':'Aceofspades', 'A♡':'Aceofhearts', 'A♢': 'Aceofdiamonds', 'A♧': 'Aceofclubs'}
                data['url'] = f"https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/{tipes[data['cards'][0]]}.svg/200px-{tipes[data['cards'][0]]}.svg.png"
            else:
                data['url'] = f"https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/{tipes[data['cards'][0][-1]]}_{data['cards'][0][:-1]}.svg/200px-{tipes[data['cards'][0][-1]]}_{data['cards'][0][:-1]}.svg.png"
            #data['url'] = f"https://upload.wikimedia.org/wikipedia/commons/2/25/{tipes[data['cards'][0][-1]]}_{data['cards'][0][:-1]}.svg"
            #data['url'] = f"https://en.wikipedia.org/wiki/Standard_52-card_deck#/media/File:{tipes[data['cards'][0][-1]]}_{data['cards'][0][:-1]}"
        '''

        return data


    def shuffleDeck(self, deck, times = 4, amount = -1):
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



def setup(bot):
    bot.add_cog(Cards(bot))