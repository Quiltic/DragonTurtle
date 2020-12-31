'''
This is both an example cog and a helper cog for me.
'''
import discord
from discord.ext import commands
from Tools import sendmsgdirect, sendmsg



class Helper(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        # current = await self.bot.get_cog('NAME') # for geting functions
    
    # an example event
    @commands.Cog.listener()
    async def on_ready(self):
        curr_status = discord.Activity(name="dragon sounds. | []help", type=discord.ActivityType.listening) # for style points
        await self.bot.change_presence(activity=curr_status)
        print("Let's Do This!")
        #await self.bot.get_user(275002179763306517).send("STARTED BABY!")
    

    # example command
    @commands.command()
    async def ping(self, ctx):
        '''
        PONG!
        This is a test command it literaly just gives you pong back.
        PONG!
        '''
        await sendmsgdirect(ctx,"PONG!")




    @commands.command()
    async def dragon(self,ctx):
        """Makes me react with 🐉🐢"""
        await ctx.message.add_reaction("🐉")
        await ctx.message.add_reaction("🐢")

    @commands.command()
    async def yell(self,ctx):
        """Turtle just Yells at you"""
        await sendmsg(ctx,"AGGGG")

    @commands.command()
    async def gitURL(self,ctx):
        """This gives the git repository on github."""
        await sendmsgdirect(ctx,"My repository is: https://github.com/Quiltic/DragonTurtle")

    


def setup(bot):
    bot.add_cog(Helper(bot))