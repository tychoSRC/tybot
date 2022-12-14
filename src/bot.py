import discord
from discord.ext import commands
from discord import app_commands
import classdefs
import random
import json
from classdefs import tree
import os
from discord.utils import get
import logging
import funcs
import requests 

print (os.getcwd())

# try:
#     f = open('./src/botConfig.json')
# except FileNotFoundError:
#     print("There was an error opening the file. Please check path in bot.py")
# # f = open('..\\data\\credentials.json')
# config = json.load(f)

# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# logging.warning('This will get logged to a file')


# TOKEN = config["botMeta"]["TOKEN"]

def run_discord_bot(token):

    bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

    @tree.command(name="ping", description="Pings the user", guild=discord.Object(id=1044668454646587453))
    async def self(interation: discord.Interaction):
        await interation.response.send_message(f"Pong")

    @bot.event 
    async def on_ready():
        try:
            print("Bot is online")
            logging.info('Bot is online')
        except Exception as e:
            print(e)
            logging.error('%s', e)

    @bot.event
    async def on_member_join(member):
        try:
            channel = member.guild.system_channel
            await channel.send(f"{member.mention} Hello, I hope you have a good day ")
        except Exception as e:
            print(e)
            logging.error('%s', e)

    @bot.event 
    async def on_member_remove(member):
        try:
            channel = member.guild.system_channel
            await channel.send(f"Goodbye  {member.mention}")
        except Exception as e:
            print(e)
            logging.error('%s', e)

    @bot.command(aliases=['8ball', '8bal'])
    async def eightball(ctx, *, question):
        # responses = ['All signs point to yes...', 'Yes!', 'My sources say nope.', 'You may rely on it.', 'Concentrate and ask again...', 'Outlook not so good...', 'It is decidedly so!', 'Better not tell you.', 'Very doubtful.', 'Yes - Definitely!', 'It is certain!', 'Most likely.', 'Ask again later.', 'No!', 'Outlook good.', 'Don\'t count on it.']
        try:
            f = open('./data/botData.json')
        except FileNotFoundError:
            print("The response file was not found! Please check path or input the absolute path to botdata.json")
            logging.error('The response file was not found! Please check path or input the absolute path to botdata.json')
        data = json.load(f)
        responses = data["responses"]
        print(f"{ctx.author} used 8ball")
        try:
            await ctx.send(f"**Question: ** {question} \n**Answer: ** {random.choice(responses)}")
        except Exception as e:
            print(e)

    @bot.command()
    async def cute(ctx, member:discord.Member = None):
        try:
            if member == None:
                member = ctx.author
            name = member.display_name
            await ctx.send(f"Can we please talk about what a cutiepie {member.mention} is? Can yall believe how cute they are?")
            await ctx.message.delete()
            logging.info('%s used cute command and message was deleted', ctx.author)
        except Exception as e:
            print(e)
            logging.error('%s', e)

    @bot.command(aliases = ['luv', 'Love'])
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def love(ctx, member:discord.Member = None):
        try:
            if member == None:
                member = ctx.author
            name = member.display_name
            await ctx.send(f"There is a {random.randint(1, 100)} % chance of love between {ctx.author.mention} and {member.mention} <3")
            logging.info('%s used love command with target %s', ctx.author, name)
        except Exception as e:
            print(e)
            logging.error('%s', e)

    @bot.command()
    async def hug(ctx, member:discord.Member = None):
        try:
            if member == None:
                member = ctx.author
            currCount = funcs.incrementInJSON("./data/botData.json", str(ctx.message.guild.id), "hugCount")
            await ctx.send(f" {ctx.author} gives {member.mention.mention} a fat hug <3. {currCount} hugs were given out in this server")
            # print(ctx.message.guild.id)
            logging.info('%s used hug command', ctx.author)
        except Exception as e:
            print(e)
            logging.error('%s', e)

    @bot.command()
    async def hate(ctx):
        try:
            member = random.choice(ctx.guild.members)
            await ctx.send(f"Oh wow {member.mention} kinda sucks huh?")
            logging.info('Hate command was used successfully')
        except Exception as e:
            print(e)
            logging.error('%s', e)

    @bot.command()
    async def map(ctx):
        try:
            response = requests.get(f'https://api.mozambiquehe.re/maprotation?auth=b5aeb39166fc6db8a895bfd34942d6e3&version=1')
            data = response.json()
            await ctx.send(f'Current Map: {data["battle_royale"]["current"]["map"]} for {data["battle_royale"]["current"]["remainingTimer"]} \nNext map: {data["battle_royale"]["next"]["map"]} for {data["battle_royale"]["next"]["DurationInMinutes"]} minutes ')
        except Exception as e:
            print(e)

    # @bot.command()
    # async def embed(ctx, member:discord.Member = None):
    #     if member == None:
    #         member = ctx.author 

    #     name = member.display_name
    #     pfp = member.display_avatar

    #     embed = discord.Embed(title="This is my embed", description="Its a very cool embed", colour=discord.Colour.random())
    #     embed.set_author(name=f"{name}", url="http://twitch.tv/tychoFPS", icon_url="https://static-cdn.jtvnw.net/jtv_user_pictures/54c0ae70-1dd6-406a-9ce3-537948f316b2-profile_image-70x70.png")
    #     embed.set_thumbnail(url=f"{pfp}")
    #     embed.add_field(name="This is 1 field", value="This field is just a value")
    #     embed.add_field(name="This is 2 field", value="This field is just a value", inline=True)
    #     embed.add_field(name="This is 1 field", value="This field is just a value", inline=False)
    #     embed.set_footer(text=f"{name} Made this embed")

    #     print("It reached the await")

    #     await ctx.send(embed=embed)

    bot.run(token)