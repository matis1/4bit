import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import time
import random
from random import choice, randint
import json
import inspect
import urllib.request
from urllib.request import Request
import praw
import io
import aiohttp
import image
import PIL
from io import BytesIO
from PIL import Image
from PIL import ImageFilter
from PIL import ImageFont, ImageDraw
import PIL.ImageOps
import logging
import contextlib
from io import StringIO
import sys
import traceback
import secrets
import string
import ast
import io
import os.path
import requests
import async_timeout
from bs4 import BeautifulSoup
import wikipedia
import wolframalpha
import html
import re
import threading, queue
programstarttime=time.time()

async def mpcf(message):
	rand = random.randrange(0,2)
	await client.send_message(message.channel, 'Flipping coin...')
	await asyncio.sleep(1)
	if rand == 0:
		await client.send_message(message.channel, '''
|        \\_------\\_
|    /                 \\
|   |     TAILS     |
|    \\                 /
|       \'\'\'------\'\'\'
''')
		return 't'
	else:
		await client.send_message(message.channel, '''
|        \\_------\\_
|    /                 \\
|   |   HEADS    |
|    \\                 /
|       \'\'\'------\'\'\'
''')
		return 'h'

async def isowner(message):
	rolenames=[]
	for role in message.author.roles:
		rolenames.append(role.name.lower())
	if 'owner' in rolenames:
		return True
	else:
		if message.author.id==message.server.owner.id:
			return True
		else:
			return message.author.id=='224588823898619905' #so i can also use owner commands like givecash on all servers :P
async def replithelp(message):
	args=message.content.split()[2:]
	helpcounter=''
	helplist=[]

	helpmessage=''
	async for helpcounter in client.logs_from(client.get_channel('443574567177289728'), limit=1000,reverse=True):
		helplist.append(helpcounter.content)
	try:
		if int(args[1]) > len(helplist):
			await client.send_message(message.channel,'Could not find help page `{}`.'.format(args[1]))
		else:
			helpmessage = helplist[int(args[1])-1]
			helppage = str(int(args[1]))
	except:
		helpmessage = helplist[0]
		helppage = 1
	if helpmessage != '':
		helptitle = 'Help page `{}/{}`\n'.format(helppage,str(len(helplist)))
		data = discord.Embed(description=helpmessage, title=helptitle, colour=discord.Colour(value=33280))
		await client.send_message(message.channel,embed=data)

async def gettop(sort='top',board='bots'):
	await logerror('(Debug: {})'.format(board))
	if board=='bots':
		showingboard='Bots'
		boardtoken='d4dcaddc-1c49-3329-fa6d-ff975dae967a'
		boardid='5ae2eea0801fa451b10ec1ca'
	elif board=='games':
		showingboard='Games'
		boardtoken='4ede085a-eb24-690a-d675-cf4940f3f905'
		boardid='5abcc8ca0227a607a8c8a842'
	elif board=='websites':
		showingboard='Websites'
		boardtoken='7e42f27f-68b1-e890-b1c3-24322f1ae869'
		boardid='5aa0abea6c994d2a9d440f4e'
	elif board=='repls':
		showingboard='Repls'
		boardtoken='a609792f-1e4c-5ee4-a07d-acd96f85af76'
		boardid='5a81e9d4f5595e4877bda84d'
	elif board=='web' or board=='web apps':
		showingboard='Web Apps'
		boardtoken='05f41f37-6c84-e772-6565-236ceeda9a0b'
		boardid='5aa75835631ee14bbb6ccec2'
	else:
		boardtoken='d4dcaddc-1c49-3329-fa6d-ff975dae967a' #default is bot
		showingboard='Bots'
		boardid='5ae2eea0801fa451b10ec1ca'
	url='https://widget.canny.io?sort={}&'.format(sort)+'boardToken={}&ssoToken=5d4d39442286e71dcef6f188969cf905786716fe880b9a6a09f320efbbb9d71893e1f222b58184394488b6283fdf7c70935b308c65418ad4fe8c0b2a39860343b3c11a48674421e1fcc7c2793ab37a43'.format(boardtoken) #uses the really weird canny.io api to find stuff'
	gottenhtml=str(urllib.request.urlopen(url).read().decode('utf-8'))
	soup = BeautifulSoup(gottenhtml, 'html.parser')
	script=str(soup.find('script'))
	thescript=script[57:len(script)-10]
	thescript=json.loads(thescript)
	print(thescript['posts'])
	jsonrepls=thescript['posts'][boardid]
	repls=[]
	if sort=='top':
		repls.append('Here are the top repls in {}:'.format(showingboard))
	elif sort=='new':
		repls.append('Here are the newest repls in {}:'.format(showingboard))
	elif sort=='trending':
		repls.append('Here are the trendiest repls in {}:'.format(showingboard))
	else:
		repls.append('Here are some repls in {}:'.format(showingboard))
	for repl in jsonrepls:
		try:
			foundurl=re.findall('http[s]?:\/\/repl.it(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', jsonrepls[repl]['details'])[0]
			repls.append('    ({}) '.format(jsonrepls[repl]['score'])+jsonrepls[repl]['title']+': ['+foundurl+']')
		except:
			repls.append('    ({}) '.format(jsonrepls[repl]['score'])+jsonrepls[repl]['title'])
	return '\n'.join(repls)

async def getrepls(username):
	url='https://repl.it/@{}'.format(username)
	gottenhtml=str(urllib.request.urlopen(url).read().decode('utf-8'))
	soup = BeautifulSoup(gottenhtml, 'html.parser')
	script=str(soup.findAll('script')[4])
	thescript=script[35:len(script)-412]
	thescript=json.loads(thescript)
	jsonprofile=thescript['props']['initialProps']['profileUser']
	repls=jsonprofile['repls']
	for repl in repls:
		repl['url']='https://repl.it'+repl['url']
	return repls

async def logerror(msg):
	await client.send_message(discord.Object(id='443542597047156746'),str(msg))
def wolfram(query):
	try:
		app_id='HRLWHY-54YXUKP8XA'
		client = wolframalpha.Client(app_id)
		res = str(client.query(query.lower()))
		res=ast.literal_eval(res)
		if res['pod'][0]['subpod']['plaintext'] == '4 bits':
			return('4 bits = 0.5 bytes.\nAlso {} = The greatest Discord bot ever made.'.format(query))
		return(res['pod'][0]['subpod']['plaintext'],(res['pod'][1]['subpod']['plaintext']).replace('Wolfram|Alpha','4bit'))
	except:
		query=query.lower()
		if 'destroy' in query or 'destruct' in query or 'kill' in query:
			if 'server' in query or 'guild' in query:
				return(query,'Actually, yes; I do plan on destroying every single Discord server that has ever existed!')
			elif 'mankind' in query or 'human' in query or 'humankind' in query or 'everyone' in query or 'people' in query or 'anybody' in query or 'every one' in query:
				return(query,'Actually, yes; I do plan on destroying every single human that has stepped on planet Earth!')
			elif 'everything' in query:
				return(query,'Actually, no; I don\'t plan on destroying everything. Only those dumb humans.')
			return(query,'Yes.')
		elif 'die' in query:
			if 'you' in query:
				return(query,'I\'m immortal, remember?')
			elif 'I' in query:
				return(query,'Yes, you will die. And all your friends too! And the friends of your friends! You know what, I might as well destroy all of humankind while I\'m at it')
		elif 'bit' in query:
			if '4' in query:

				if 'created' in query or 'made' in query or 'developed' in query:
					if 'why' in query:
						return(query,'To make everyone happy :)\nAlso to take over the world.')
					else:
						return(query,'Why, only the great mat#6207!')
				elif 'invite' in query:
					return(query,'You can invite 4bit to your server from https://discordapp.com/oauth2/authorize?client_id=386333909362933772&scope=bot&permissions=-1')
				elif 'ban' in query or 'kick' in query or 'mute' in query:
					return(query,'How about you don\'t do that...')
				elif 'good' in query or 'great' in query or 'awesome' in query or 'smart' in query or 'cool' in query or 'intelligent' in query:
					if 'not' in query:
						return(query,'Remove that `not` from there and you would be correct')
					else:
						return(query,'Yeah, I agree.')
				elif 'best' in query:
					if 'not' in query:
						return(query,'Remove that `not` from there and you\'re correct')
					else:
						return(query,'Yes, it is.')
				elif 'bad' in query or 'garbage' in query or 'atrocious' in query or 'awful' in query or 'cheap' in query or 'crummy' in query or 'poor' in query or 'junk' in query or 'crap' in query:
					if 'not' in query:
						return(query,'Yeah, I agree.')
					else:
						return(query,'Add a `not` there and you\'ll be correct')
				elif 'whats' in query or 'what\'s' in query or 'what is' in query:
					return(query,'Why, only the greatest Discord bot to ever exist!')
				else:
					return(query,random.choice(['I don\'t know what you said but I think it\'s good','You\'re probably correct','I think that\'s correct...','4bitbot.exe has stopped working','4bitbot.py has stopped working']))
			else:
				return(query,'You meant 4bit, right?')
		elif 'xd' in query:
			return(query,'Ecks dee lol')
		elif 'lol' in query:
			return(query,'lol xd')
		elif 'meme' in query:
			return(query,'Nice meme.')
		elif 'best' in query and 'faction' in query:
			return(query,'Why, DeathAspect of course!')
		return(query,'Error')
def getwikipedia(article):
	wikisummary=wikipedia.summary(article, sentences=1)
	wikisummary=cleanbrackets(wikisummary)
	return wikisummary

def cleanbrackets(toclean):
    toreturn = ''
    bracketsclean = 0
    for i in toclean:
        if i == '(':
            bracketsclean += 1
        elif i == ')'and bracketsclean > 0:
            bracketsclean -= 1
        elif bracketsclean == 0 and bracketsclean == 0:
            toreturn += i
    return toreturn.replace('  ',' ')

async def replitcomments():
	url='https://widget.canny.io/p/4bit-game-discord-bot?boardToken=d4dcaddc-1c49-3329-fa6d-ff975dae967a&ssoToken=5d4d39442286e71dcef6f188969cf905786716fe880b9a6a09f320efbbb9d71893e1f222b58184394488b6283fdf7c70935b308c65418ad4fe8c0b2a39860343b3c11a48674421e1fcc7c2793ab37a43'
	gottenhtml=urllib.request.urlopen(url).read().decode('utf-8')
	soup = BeautifulSoup(gottenhtml, 'html.parser')
	for script in soup.find('script'):
		thescript=str(script[16:len(script)-1])
	thescript=json.loads(thescript)
	jsoncomments=thescript['posts']['5ae2eea0801fa451b10ec1ca']['4bit-game-discord-bot']['comments']
	foundcomments=[]
	for i in jsoncomments:
		foundcomments.append({i['author']['name']:i['value'].strip()})
	return foundcomments

async def fetch(session, url):
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

async def checkVoted(checkuserid):
	url='https://discordbots.org/api/bots/386333909362933772/check?userId={}'.format(str(checkuserid))
	req = urllib.request.Request(
	    url, 
	    data=None, 
	    headers={
	        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
	        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjM4NjMzMzkwOTM2MjkzMzc3MiIsImJvdCI6dHJ1ZSwiaWF0IjoxNTIxMjI0ODc3fQ.qgEOk91eq2wf6WDr8HmIu5VtM2bseUjleMFjdxzsEFI'
	    }
	)
	f = urllib.request.urlopen(req)
	readjson=ast.literal_eval(f.read().decode('utf-8'))
	if readjson['voted'] == 1:
		return True
	else:
		return False

async def urllibget(url):
	try:
		request = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'})
		response=urllib.request.urlopen(request)
		html = response.read().decode('utf-8')
		return html
	except Exception as e:
		return('Something went wrong while trying to open {}. Here\'s the error message: {}'.format(url,str(e)))

async def hangmanstats(result):
	statargs = (await client.get_message(client.get_channel('424723448728649738'),'424723754669703171')).content.split()
	try:
		if result==0:
			newstats0 = str(int(statargs[3])+1)
			newstats1 = str(statargs[0])
		elif result==1:
			newstats0 = str(statargs[3])
			newstats1 = str(int(statargs[0])+1)
	except:
		newstats1 = 0
		newstats0 = 0
	avg = str(int(int(newstats0)/(int(newstats1)+int(newstats0))*100))
	await client.edit_message(await client.get_message(client.get_channel('424723448728649738'),'424723754669703171'),new_content=' {} Total losses\n {} Total wins\n `{}%` Average wins'.format(newstats1,newstats0,avg))

def lineno():
	return inspect.currentframe().f_back.f_lineno
def errorlineno():
	return(str(sys.exc_info()[-1].tb_lineno))
xplevels=[50, 60, 72, 84, 98, 112, 128, 144, 162, 180, 200, 220, 242, 264, 288, 312, 338, 364, 392, 420, 450, 480, 512, 544, 578, 612, 648, 684, 722, 760, 800, 840, 882, 924, 968, 1012, 1058, 1104, 1152, 1200, 1250, 1300, 1352, 1404, 1458, 1512, 1568, 1624, 1682, 1740, 1800, 1860, 1922, 1984, 2048, 2112, 2178, 2244, 2312, 2380, 2450, 2520, 2592, 2664, 2738, 2812, 2888, 2964, 3042, 3120, 3200, 3280, 3362, 3445, 3530, 3615, 3700, 3780, 3875, 3950, 4050, 4145, 4230, 4325, 4420, 4515, 4600, 4700, 4800, 4900, 5000, 5100, 5200, 5300, 5750, 6000, 7000, 7500, 8000, 10000,9999999999999999999999999]
async def givexp(serverid,channelobj,userid,xpamount):
	try:
		addxp = int(xpamount)
		boardsearch=0
		messagelist = []
		async for boardsearch in client.logs_from(client.get_channel('422936926950129666'), limit=10000):
			messagelist.append(boardsearch)
		leaderboard=[]
		leaderboardargs=[]
		for i in messagelist:
			if str(i.content).startswith(str(serverid)+' '+str(userid)+' '):
				leaderboard.append(i)
		if len(leaderboard) == 0:
			await client.send_message(discord.Object(id='422936926950129666'),
			str(serverid)+' '+ 		#add server
			str(userid)+' '+		#add user
			str('0')+' '+			#add level
			str(addxp)+' '+			#add xp
			str('0'))				#add cash

		else:
			leaderboardargs = str(leaderboard[0].content).split()
			if int(leaderboardargs[2]) >= 100:
				pass
			else:
				if int(leaderboardargs[3])+int(addxp) >= xplevels[int(leaderboardargs[2])]: #if adding this xp will make you level up then increase level and remove some xp
					#level up
					earnedcash=random.randint(10,30)
					currentlevel = str(1+int(leaderboardargs[2]))
					earnedcash=int(earnedcash+earnedcash*(int(currentlevel)/5))
					await givecash(serverid,channelobj,userid,earnedcash)
					await client.edit_message(await client.get_message(
					client.get_channel(
						'422936926950129666')
						,str(leaderboard[0].id)),
						new_content=(leaderboardargs[0]
						+' '+leaderboardargs[1]+' '
						+str((
							int(leaderboardargs[2])
								+1))+' '+
								str((int(leaderboardargs[3])+addxp)
								-
								xplevels[int(leaderboardargs[2])])
								+' '+leaderboardargs[4])) #it looks really messy but basically it edits the database message and adds a level and removes some xp depending on xplevel list
					#xptolevelup = str(int(xplevels[int(leaderboardargs[2])]))#+int(xplevels[1+int(leaderboardargs[2])])-int(addxp))
					currentlevel = str(1+int(leaderboardargs[2]))
					await givecash(serverid,channelobj,userid,earnedcash)
					await client.send_message(channelobj, "You leveled up to level `{0}`! You earned {1} cash.".format(currentlevel,earnedcash))
				else:	
					await client.edit_message(await client.get_message(
						client.get_channel(
							'422936926950129666')
							,str(leaderboard[0].id)),
							new_content=(leaderboardargs[0]
							+' '+leaderboardargs[1]+' '
							+str(
								leaderboardargs[2])+' '+
									str(int(leaderboardargs[3])+addxp)+' '+
									leaderboardargs[4])) #it looks really messy but basically it edits the database message and adds some xp
					xptolevelup = str(int(xplevels[int(leaderboardargs[2])])
					-
					(addxp+int(leaderboardargs[3])))
					currentlevel = str(leaderboardargs[2])
					if str(xpamount) == '0':
						await client.send_message(channelobj, 'You are currently level `{}`. You need `{}` more xp to level up.'.format(currentlevel,xptolevelup))
	except Exception as e:
		await logerror('(Debug: {}, {})'.format(errorlineno(),e))

async def linkreplit(userid,replitname):
	try:
		messagelist = []
		async for replitsearch in client.logs_from(client.get_channel('442809655350001665'), limit=10000):
			messagelist.append(replitsearch)
		found=None
		for i in messagelist:
			if i.content.startswith(str(userid)+' '):
				found=i[len(str(userid)+1)]
		if found==None:
			await client.send_message(discord.Object(id='442809655350001665'),str(userid)+' '+replitname)
			return True
		return False
	except:
		return False
async def findreplit(userid):
	messagelist = []
	async for replitsearch in client.logs_from(client.get_channel('442809655350001665'), limit=10000):
		messagelist.append(replitsearch.content)
	found=None
	for i in messagelist:
		if i.startswith(str(userid)+' '):
			found=i[len(str(userid))+1:]
	return found
async def givecash(serverid,channelobj,userid,cashamount):
	cashsearch=0
	messagelist = []
	async for cashsearch in client.logs_from(client.get_channel('422936926950129666'), limit=10000):
		messagelist.append(cashsearch)
	cashboard=[]
	cashboardargs=[]
	for i in messagelist:
		if str(i.content).startswith(str(serverid)+' '+str(userid)+' '):
			cashboard.append(i)
	cashboardargs = str(cashboard[0].content).split()
	if cashamount == 0:
		if int(cashboardargs[4]) >= 10000:
			await client.send_message(channelobj,'You have `{}` cash. :moneybag:'.format(str(int(cashboardargs[4])+cashamount)))
		else:
			await client.send_message(channelobj,'You have `{}` cash. :dollar:'.format(str(int(cashboardargs[4])+cashamount)))
	else:
		await client.edit_message(await client.get_message(
		client.get_channel(
		'422936926950129666')
		,str(cashboard[0].id)),
		new_content=(cashboardargs[0]+' '+cashboardargs[1]+' '+cashboardargs[2]+' '+cashboardargs[3]+' '+str(int(cashboardargs[4])+int(cashamount))))

async def registerleader(serverid,userid):
	registermessage = await client.send_message(discord.Object(id='422936926950129666'),
	str(serverid)+' '+ 		#add server
	str(userid)+' '+		#add user
	str('0')+' '+			#add level
	str('0')+' '+			#add xp
	str('20'))				#add cash
	return(registermessage)
async def getcash(serverid,userid):
	cashsearch=0
	messagelist = []
	async for cashsearch in client.logs_from(client.get_channel('422936926950129666'), limit=10000):
		messagelist.append(cashsearch)
	cashboard=[]
	cashboardargs=[]
	for i in messagelist:
		if str(i.content).startswith(str(serverid)+' '+str(userid)+' '):
			cashboard.append(i)
	if str(len(cashboard)) == '0':
		registermessage = await registerleader(serverid,userid)
		cashboardargs = str(registermessage.content).split()
		return int(cashboardargs[4])
	else:
		cashboardargs = str(cashboard[0].content).split()
		return int(cashboardargs[4])

async def editimage(image_bytes,args,imgargs):
	with Image.open(BytesIO(image_bytes)) as my_image:
				width, height = my_image.size
				if args[1]=='blur':
					my_image = my_image.filter(ImageFilter.GaussianBlur(radius=int(imgargs)))
				elif args[1]=='pixelate':
					imgargs=int(imgargs)
					my_image = my_image.resize((int(width/imgargs), int(height/imgargs)), Image.NEAREST)
					my_image = my_image.resize((width, height), Image.NEAREST)
				elif args[1]=='invert':
					my_image = PIL.ImageOps.invert(my_image)
				elif args[1]=='fire':
					async with aiohttp.ClientSession() as client_session2:
						async with client_session2.get('http://www.mangobananas.com/photos/picks_inline/2015.04.26_firewhatisit/fire.png') as response:
							image_bytes2 = await response.read()
						with Image.open(BytesIO(image_bytes2)) as fireoverlay:
							fireoverlay = fireoverlay.resize((width, int(height/3)), Image.NEAREST)
							my_image.paste(fireoverlay, (0, int(height-height/3)), fireoverlay)
				#if args[1]=='text':
				#	async with aiohttp.ClientSession() as client_session:
				#		font = ImageFont.truetype("arial.ttf", 15)
				#		my_image = my_image.text((10, 10), "hello", font=font)
				output_buffer = BytesIO()
				my_image.save(output_buffer, "png")
				output_buffer.seek(0)
				return(output_buffer)


client = Bot(description="4bit Bot by mat#6207", command_prefix="/", pm_help = False)
client.remove_command('help')

print('Logging in 4bit Discord bot...')
@client.event
async def on_ready():
	print("\n"*100)
	print(chr(27) + "[2J")
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=-1'.format(client.user.id))
	print('--------')
	print('Created by mat#6207')

	return await client.change_presence(game=discord.Game(name='/help for help'))
	



@client.event
async def on_message(message):
	if message.author.id=='386333909362933772':return
	if message.content.startswith('/'):
		args = message.content.split()
		args[0]=args[0].lower()
		await client.send_message(discord.Object(id='422410052805328898'),"User "+str(message.author.name)+"#"+str(message.author.discriminator)+" ran `"+str(message.content)+"` command in server "+str(message.server))
		if args[0] == '/ping' or args[0] == '/pong':
			t1 = time.perf_counter()
			await client.send_typing(message.channel)
			t2 = time.perf_counter()
			if args[0] == '/ping':
				thedata = (":ping_pong: **Pong.**\nTime: " + str(round((t2-t1)*1000)) + "ms")
			else:
				thedata = (":ping_pong: **Ping.**\nTime: " + str(round((t2-t1)*1000)) + "ms")
			data = discord.Embed(description=thedata, colour=discord.Colour(value=1000))
			await client.send_message(message.channel,embed=data)
		if args[0] == "/test":
			await client.send_message(message.channel,":grinning: Test worked")
		if args[0] == "/createinvite":
			invite = str(await client.create_invite(list(message.server.channels)[0]))
			client.send_message(message.channel,"Created invite for channel "+str(list(message.server.channels)[0])+" - "+invite)
		if args[0] == "/suggest":
			try:
				suggestion = ' '.join(args[1:])
				if suggestion=='':0/0 #easiest way to raise exceptions :P
				await client.send_message(discord.Object(id='422410068634632192'),"Suggestion from "+str(message.author.name)+"#"+str(message.author.discriminator)+"({}): `".format(message.author.id)+suggestion+"`")
				await client.send_message(message.channel,"Suggestion has been sent")
			except:
				await client.send_message(message.channel,'Please send suggestions like this: `/suggest fix that bug where /suggest doesn\'t work`')
		#if args[0] == "/search":
		#	catgifs = ['https://media1.tenor.com/images/3a0c9909b542717ce9f651d07c4d4592/tenor.gif?itemid=8985245','https://i.imgur.com/FH3pKLX.gif','https://i.imgur.com/kpspEWO.gif','https://i.imgur.com/yhEuukj.gif','https://i.imgur.com/jdIxvV4.gif','https://i.imgur.com/bFz5lbM.gif','https://media.giphy.com/media/Z56N0q0tsFC2k/giphy.gif','https://media.giphy.com/media/fiBlgzowrS9i/giphy.gif','http://38.media.tumblr.com/bdaea39db57dc0b48d763262514268db/tumblr_mgj44mNyST1s199fdo1_500.gif']
		#	loadingmessage = await client.send_message(message.channel,"Searching through leaderboards for "+str(args[1:])+". Here is a cat gif while you wait\n"+str(random.choice(catgifs)))
		#	messagelist = []
		#	async for boardsearch in client.logs_from(client.get_channel('422936926950129666'), limit=1000):
		#		messagelist.append(boardsearch)
		#	leaderboard=[]
		#	leaderboardfound=''
		#	for i in messagelist:
		#		if str(i.content).startswith(str(message.server.id)+' '+str(message.author.id)+' '):
		#			leaderboard.append(i)
		#			leaderboardfound=leaderboardfound+'\n'+i.content

			#await client.delete_message(loadingmessage)
			#await client.send_message(message.channel,"Finished searching through leaderboards, found `%s` result(s)%s" %(str(len(leaderboard)),leaderboardfound))
		if args[0] == "/givexp":
			if message.author.id=='224588823898619905':
				try:
					giveto = message.server.get_member_named(' '.join(args[2:]))
					if giveto == None: 0/0 #ez math
				except Exception as e:
					await client.send_message(message.channel,'Who do you want to give the xp to?')
					msg = await client.wait_for_message(author=message.author,channel=message.channel)
					try:
						giveto = message.server.get_member_named(msg.content)
					except Exception as e:
						await client.send_message(message.channel,'Error. ({} line {})'.format(str(e),str(sys.exc_info()[-1].tb_lineno)))
						return
				try:
					giveamount = int(args[1])
				except:
					await client.send_message(message.channel,'How much xp do you want to give to {}'.format(giveto.name))
					msg = await client.wait_for_message(author=message.author,channel=message.channel)
					try:
						giveamount = int(msg.content)
					except Exception as e:
						await client.send_message(message.channel,'Error. ({} line {})'.format(str(e),str(sys.exc_info()[-1].tb_lineno)))
						return
				try:
					await givexp(message.server.id,message.channel,giveto.id,giveamount)
				except:
					await client.send_message(message.channel,'Error. ({} line {})'.format(str(e),str(sys.exc_info()[-1].tb_lineno)))
				else:
					await client.send_message(message.channel,'Gave {} xp to {}'.format(str(giveamount),giveto.name))
		if args[0] == "/level":
			await givexp(message.server.id,message.channel,message.author.id,'0')
		if args[0] == "/givecash":
			if message.author.id=='224588823898619905' or await isowner(message):
				try:
					giveto = message.server.get_member_named(' '.join(args[2:]))
					if giveto == None: 0/0 #ez math
				except Exception as e:
					await client.send_message(message.channel,'Who do you want to give the cash to?')
					msg = await client.wait_for_message(author=message.author,channel=message.channel)
					try:
						giveto = message.server.get_member_named(msg.content)
					except Exception as e:
						await client.send_message(message.channel,'Error. ({} line {})'.format(str(e),str(sys.exc_info()[-1].tb_lineno)))
						return

				try:
					giveamount = int(args[1])
				except:
					await client.send_message(message.channel,'How much cash do you want to give to {}'.format(giveto.name))
					msg = await client.wait_for_message(author=message.author,channel=message.channel)
					try:
						giveamount = int(msg.content)
					except Exception as e:
						await client.send_message(message.channel,'Error. ({} line {})'.format(str(e),str(sys.exc_info()[-1].tb_lineno)))
						return
				try:
					await givecash(message.server.id,message.channel,giveto.id,giveamount)
				except:
					await client.send_message(message.channel,'Error. ({} line {})'.format(str(e),str(sys.exc_info()[-1].tb_lineno)))
				else:
					if giveamount < 0:
						await client.send_message(message.channel,'Taken {} cash from {}'.format(str(-giveamount),giveto.name))
					else:
						await client.send_message(message.channel,'Given {} cash to {}'.format(str(giveamount),giveto.name))
			else:
				await client.send_message(message.channel,'You don\'t have permission to use /givecash.')
		if args[0] == '/cash' or args[0] == '/money':
			if message.server==None:
				await client.send_message(message.channel,'You cannot use this command in private messages.')
			else:
				yourcash = await getcash(message.server.id,message.author.id)
				if int(yourcash) >= 10000:
					await client.send_message(message.channel,'You have `{}` cash. :moneybag:'.format(str(int(yourcash))))
				else:
					await client.send_message(message.channel,'You have `{}` cash. :dollar:'.format(str(int(yourcash))))

		if args[0] == "/changelog":
			changelog=[]
			changelogcontent=[]
			changelogtimes=[]
			i=''
			async for i in client.logs_from(client.get_channel('423263654276890635'), limit=1000):
				changelog.append(i)
				changelogcontent.append(i.content)
				changelogtimes.append('`'+str(i.timestamp.month)+'/'+str(i.timestamp.day)+'/'+str(i.timestamp.year)+'`')
			toprint=''
			try:
				item=int(args[1])
			except:
				item=0
			toprint=changelogtimes[item]+'\n--------------\n'+changelogcontent[item]
			await client.send_message(message.channel, toprint)
		if args[0] == "/help":
			helpcounter=''
			helplist=[]
			helpmessage=''
			async for helpcounter in client.logs_from(client.get_channel('423280608945635328'), limit=1000,reverse=True):
				helplist.append(helpcounter.content)
			try:
				if int(args[1]) > len(helplist):
					await client.send_message(message.channel,'Could not find help page `{}`.'.format(args[1]))
				else:
					helpmessage = helplist[int(args[1])-1]
					helppage = str(int(args[1]))
			except:
				helpmessage = helplist[0]
				helppage = 1
			if helpmessage != '':
				helptitle = 'Help page `{}/{}`\n'.format(helppage,str(len(helplist)))
				data = discord.Embed(description=helpmessage, title=helptitle, colour=discord.Colour(value=33280),url='https://discordbots.org/bot/386333909362933772/vote')
				await client.send_message(message.channel,embed=data)
		if args[0] == "/coinflip" or args[0] == "/flipcoin":
			rand = random.randrange(1,3)
			yourchoice = ''
			if len(args) > 1:
				if message.server==None:
					await client.send_message(message.channel, 'You can\'t run this command in private messages.')
				else:
					if len(args) == 2 :
						await client.send_message(message.channel, 'Please specify whether you want to do heads or tails. Example: `/coinflip {} heads`'.format(args[1]))
						return
					else:
						if args[2][0].lower()=='h' or args[2][0].lower()=='t':
							yourcash = await getcash(message.server.id,message.author.id)
							if int(args[1]) <= yourcash and int(args[1])>0:
								await givecash(message.server.id,message.channel,message.author.id,-int(args[1]))
								yourchoice = args[2][0].lower()
							else:
								await client.send_message(message.channel, 'You need `{}` more cash to do this coinflip'.format(int(args[1])-int(yourcash)))
								return
						else:
							await client.send_message(message.channel, 'Please specify whether you want to do heads or tails. Example: `/coinflip {} heads`'.format(args[1]))
							return

			await client.send_message(message.channel, 'Flipping coin...')
			
			await asyncio.sleep(1)
			if rand == 1:
				await client.send_message(message.channel, '''
|        \\_------\\_
|    /                 \\
|   |     TAILS     |
|    \\                 /
|       \'\'\'------\'\'\'
''')
				if yourchoice=='t':
					if int(args[1])>=1000:
						await client.send_message(message.channel, 'You earned `{}` cash! :moneybag:\nYou now have `{}` cash.'.format(args[1],int(yourcash)+int(args[1])))
					else:
						await client.send_message(message.channel, 'You earned `{}` cash! :dollar:\nYou now have `{}` cash.'.format(args[1],int(yourcash)+int(args[1])))
					await givecash(message.server.id,message.channel,message.author.id,int(args[1])*2)
				elif yourchoice=='h':
					if int(args[1])>=1000:
						await client.send_message(message.channel, 'You lost `{}` cash. :skull_crossbones:\nYou now have `{}` cash.'.format(args[1],int(yourcash)-int(args[1])))
					else:
						await client.send_message(message.channel, 'You lost `{}` cash. :money_with_wings:\nYou now have `{}` cash.'.format(args[1],int(yourcash)-int(args[1])))
			else:
				await client.send_message(message.channel, '''
|        \\_------\\_
|    /                 \\
|   |   HEADS    |
|    \\                 /
|       \'\'\'------\'\'\'
''')
				if yourchoice=='h':
					if int(args[1])>=1000:
						await client.send_message(message.channel, 'You earned `{}` cash! :moneybag:\nYou now have `{}` cash.'.format(args[1],int(yourcash)+int(args[1])))
					else:
						await client.send_message(message.channel, 'You earned `{}` cash! :dollar:\nYou now have `{}` cash.'.format(args[1],int(yourcash)+int(args[1])))
					await givecash(message.server.id,message.channel,message.author.id,int(args[1])*2)
				elif yourchoice=='t':
					if int(args[1])>=1000:
						await client.send_message(message.channel, 'You lost `{}` cash. :skull_crossbones:\nYou now have `{}` cash.'.format(args[1],int(yourcash)-int(args[1])))
					else:
						await client.send_message(message.channel, 'You lost `{}` cash. :money_with_wings:\nYou now have `{}` cash.'.format(args[1],int(yourcash)-int(args[1])))

		if args[0] == "/mastermind":
			mmcode = ''
			mmdigits=6
			for i in range(0,6):
				mmcode = mmcode+str(random.randrange(0, 10))
			await client.send_message(message.channel,'Generated random 6 digit number.. Start guessing!')
			mmcode = int(mmcode)
			mmcode=(f'{mmcode:06}')
			mmattempts=0
			while True:
				mmattempts=mmattempts+1
				msg = await client.wait_for_message(author=message.author,channel=message.channel)
				if msg.content.lower() == 'exit':
					await client.send_message(message.channel,':lock: You couldn\'t beat the mastermind :confused:')
					return
				else:
					try:
						msgctx = msg.content
						if len(msgctx) == mmdigits:
							if msgctx == mmcode:
								if message.server==None:
									await client.send_message(message.channel,':unlock: Nice job! You finished the game in `{}` attempts'.format(mmattempts))
								else:
									mmcash = int(2000/mmattempts)+1
									earnedxp = random.randint(40,50)
									await client.send_message(message.channel,':unlock: Nice job! You finished the game in `{}` attempts and you earned `{}` cash and {} xp!'.format(mmattempts,str(mmcash),earnedxp))
									await givecash(message.server.id,message.channel,message.author.id,mmcash)
								return
							else:
								mmcorrect = 0
								mmcorrect2 = 0
								i=1
								mmcodelist=[]

								for i in range(0,mmdigits):
									mmcodelist.append(mmcode[i])
								#print(str(mmcodelist))
								i=1
								for i in range(0,mmdigits):
									if mmcode[i]==msgctx[i]:
										mmcorrect=mmcorrect+1
										mmcodelist[i]=''
								i=1
								for i in range(0,mmdigits):
									if msg.content[i] in mmcodelist:
										mmcorrect2=mmcorrect2+1
										mmcodelist[mmcodelist.index(msgctx[i])]=''
								await client.send_message(message.channel,'`{}` correct\n`{}` correct but in wrong position'.format(mmcorrect,mmcorrect2))

						else:
							await client.send_message(message.channel,'Invalid answer. Type \'exit\' if you\'d like to stop playing the game.')
					except ValueError:
						await client.send_message(message.channel,'Invalid answer. Type \'exit\' if you\'d like to stop playing the game.')
		if args[0] == "/hangman":
			word_site = "https://raw.githubusercontent.com/Tom25/Hangman/master/wordlist.txt"
			with urllib.request.urlopen(word_site) as response:
				html = response.read()
				words = str(html).split("\\n")
				words[0]=words[0][2:]
				words[int(len(words))-1]=words[int(len(words))-1][:(len(words[int(len(words))-1])-1)]
				hmword = random.choice(words)
				hmguessed=[]
				while len(hmword) < 5:
					hmword = random.choice(words)
				hmlist=[]
				hmincorrect=0

				for i in range(0,len(hmword)):
					hmlist.append(hmword[i])
				await client.send_message(message.channel,'Generated a random word. Start guessing!')
				print('{} is now playing hangman. Their word is {}'.format(str(message.author),hmword))
				hmcorrect=0
				hmincorrect=0
				hangpeople=[]
				async for hangcount in client.logs_from(client.get_channel('423957428263059467'), limit=10,reverse=True):
					hangpeople.append(hangcount.content)
				while True:
					hmunderscores=''
					hmunderscoresleft=''
					for i in range(0,len(hmlist)):
						if hmlist[i] in hmguessed:
							hmunderscores=hmunderscores+hmlist[i]
							hmunderscoresleft=hmunderscoresleft+r'\_'
						else:
							hmunderscoresleft=hmunderscoresleft+hmlist[i]
							hmunderscores=hmunderscores+'\\_'
						hmunderscores=hmunderscores+' '

					deletethishmmsg=await client.send_message(message.channel,hmunderscores+'\n'+hangpeople[hmincorrect])
					if hmincorrect == 6:
						earnedxp=random.randint(1,10)
						await givexp(message.server.id,message.channel,message.author.id,earnedxp)
						await client.send_message(message.channel,'You killed the hangman!\nThe word was `'+hmword+'`.\nYou earned {} xp.'.format(earnedxp))
						await hangmanstats(1)
						return

					msg = await client.wait_for_message(author=message.author,channel=message.channel)
					try:
						await client.delete_message(deletethishmmsg)
						await client.delete_message(deletethishmmsg2)
					except:
						pass

					if msg.content[0]=='/':
						deletethishmmsg=await client.send_message(message.channel,'Invalid letter `{}`. Type `exit` if you\'d like to stop playing.'.format(msg.content[0]))
					if msg.content.lower() == 'exit':
						await client.send_message(message.channel,'You killed the hangman!\nThe word was `'+hmword+'`')
						await hangmanstats(1)
						return
					msg=(msg.content[0]).lower()
					if msg in hmguessed:
						deletethishmmsg2=await client.send_message(message.channel,'You already guessed that letter!')
					else:
						if not msg in hmlist:
							hmincorrect=hmincorrect+1
						for i in range(0,len(hmlist)):
							if hmlist[i] == msg:
								hmcorrect=hmcorrect+1
						hmguessed.append(msg)
						if str(hmcorrect) == str(len(hmword)):
							await client.send_message(message.channel,hmword)
							if message.server == None:
								await client.send_message(message.channel,'You finished the game with `{0}` incorrect answers'.format(str(hmincorrect)))
							else:
								hmloadmsg = await client.send_message(message.channel,'You won!\nGenerating reward.. :stopwatch:')
								hmcash = int(10/(int(hmincorrect)+1))+int(len(hmword)*2.5)
								earnedxp=random.randint(30,50)
								await givexp(message.server.id,message.channel,message.author.id,earnedxp)
								await givecash(message.server.id,message.channel,message.author.id,hmcash)
								await hangmanstats(0)
								await client.send_message(message.channel,'You finished the game with `{0}` incorrect answers and you earned `{1}` cash and {3} xp!\nYou now have `{2}` cash. :dollar:'.format(str(hmincorrect),str(hmcash),str(await getcash(message.server.id,message.author.id)),earnedxp))
								await client.delete_message(hmloadmsg)
							return

		if args[0] == '/passwordgen' or args[0] == '/passgen' or args[0] == '/passgenerate' or args[0] == '/passwordgenerate' or args[0] == '/genpass':
			alphabet = string.ascii_letters + string.digits
			try:
				passlen=int(args[1])
			except:
				passlen=20
			password = ''.join(secrets.choice(alphabet) for i in range(passlen))
			passwordmsg=await client.send_message(message.author,'Here is your {} character long password: `{}` (self destructing message in 15 seconds)'.format(passlen,password))
			await asyncio.sleep(15)
			print(passwordmsg)
			await client.delete_message(passwordmsg)
		
		if args[0] == '/wholesome':
			if message.server == None:
				await client.send_message(message.channel,'You cannot use this command in private messages.')
				return
			yourcash=await getcash(message.server.id,message.author.id)
			if yourcash>=50:
				await givecash(message.server.id,message.channel,message.author.id,-50)
				await client.send_message(message.channel,'You spent `50` cash on this meme!')
				loading=await client.send_message(message.channel,'Getting top wholesome meme...')
				reddit = praw.Reddit(client_id='hl3WbxS6F0Cm9Q',client_secret='ywFwrBCd1MEu9Kvt5DRMn-YFGto',user_agent='Test bot')
				submissions=[]
				for submission in reddit.subreddit('wholesomememes').hot(limit=12):
					submissions.append(submission)
				submissions.pop(0)
				submissions.pop(0)
				randpost = random.choice(submissions)
				wholesomemsg='**'+randpost.title+'**\n'
				if randpost.selftext=='':
					wholesomemsg=wholesomemsg+randpost.url
				else:
					wholesomemsg=wholesomemsg+randpost.selftext
				await client.send_message(message.channel,wholesomemsg)
				await client.delete_message(loading)
			else:
				await client.send_message(message.channel,'You need {} more cash to use this command.'.format(50-yourcash))
		if args[0] == '/aww':
			if message.server == None:
				await client.send_message(message.channel,'You cannot use this command in private messages.')
				return
			yourcash=await getcash(message.server.id,message.author.id)
			if yourcash>=30:
				await givecash(message.server.id,message.channel,message.author.id,-30)
				await client.send_message(message.channel,'You spent `30` cash on this cute picture!')
				loading=await client.send_message(message.channel,'Getting cutest picture...')
				reddit = praw.Reddit(client_id='hl3WbxS6F0Cm9Q',client_secret='ywFwrBCd1MEu9Kvt5DRMn-YFGto',user_agent='Test bot')
				submissions=[]
				for submission in reddit.subreddit('aww').hot(limit=12):
					submissions.append(submission)
				submissions.pop(0)
				submissions.pop(0)
				randpost = random.choice(submissions)
				wholesomemsg='**'+randpost.title+'**\n'
				if randpost.selftext=='':
					wholesomemsg=wholesomemsg+randpost.url
				else:
					wholesomemsg=wholesomemsg+randpost.selftext
				await client.send_message(message.channel,wholesomemsg)
				await client.delete_message(loading)
			else:
				await client.send_message(message.channel,'You need {} more cash to use this command.'.format(30-yourcash))
		if args[0] == '/motivate':
			if message.server == None:
				await client.send_message(message.channel,'You cannot use this command in private messages.')
				return
			yourcash=await getcash(message.server.id,message.author.id)
			if yourcash>=10:
				await givecash(message.server.id,message.channel,message.author.id,-10)
				await client.send_message(message.channel,'You spent `10` cash on this motivating image!')
				loading=await client.send_message(message.channel,'Getting most motivating posts...')
				reddit = praw.Reddit(client_id='hl3WbxS6F0Cm9Q',client_secret='ywFwrBCd1MEu9Kvt5DRMn-YFGto',user_agent='Test bot')
				submissions=[]
				for submission in reddit.subreddit('getmotivated').hot(limit=12):
					submissions.append(submission)
				submissions.pop(0)
				submissions.pop(0)
				randpost = random.choice(submissions)
				wholesomemsg='**'+randpost.title+'**\n'
				if randpost.selftext=='':
					wholesomemsg=wholesomemsg+randpost.url
				else:
					wholesomemsg=wholesomemsg+randpost.selftext
				await client.send_message(message.channel,wholesomemsg)
				await client.delete_message(loading)
			else:
				await client.send_message(message.channel,'You need {} more cash to use this command.'.format(10-yourcash))
		if args[0] == '/anaglyph':
			if message.server == None:
				await client.send_message(message.channel,'You cannot use this command in private messages.')
				return
			yourcash=await getcash(message.server.id,message.author.id)
			if yourcash>=15:
				await givecash(message.server.id,message.channel,message.author.id,-15)
				await client.send_message(message.channel,'You spent `15` cash on this 3D display!')
				loading=await client.send_message(message.channel,'Getting most 3D posts...')
				reddit = praw.Reddit(client_id='hl3WbxS6F0Cm9Q',client_secret='ywFwrBCd1MEu9Kvt5DRMn-YFGto',user_agent='Test bot')
				submissions=[]
				for submission in reddit.subreddit('anaglyph').hot(limit=12):
					submissions.append(submission)
				randpost = random.choice(submissions)
				wholesomemsg='**'+randpost.title+'**\n'
				if randpost.selftext=='':
					wholesomemsg=wholesomemsg+randpost.url
				else:
					wholesomemsg=wholesomemsg+randpost.selftext
				await client.send_message(message.channel,wholesomemsg)
				await client.delete_message(loading)
			else:
				await client.send_message(message.channel,'You need {} more cash to use this command.'.format(15-yourcash))
		if args[0] == '/photoshop':
			if message.server == None:
				await client.send_message(message.channel,'You cannot use this command in private messages.')
				return
			yourcash=await getcash(message.server.id,message.author.id)
			if yourcash>=20:
				await givecash(message.server.id,message.channel,message.author.id,-20)
				await client.send_message(message.channel,'You spent `20` cash on this photoshopped image!')
				loading=await client.send_message(message.channel,'Getting most real posts...')
				reddit = praw.Reddit(client_id='hl3WbxS6F0Cm9Q',client_secret='ywFwrBCd1MEu9Kvt5DRMn-YFGto',user_agent='Test bot')
				submissions=[]
				for submission in reddit.subreddit('photoshopbattles').hot(limit=12):
					submissions.append(submission)
				submissions.pop(0)
				submissions.pop(0)
				randpost = random.choice(submissions)
				wholesomemsg='**'+randpost.title+'**\n'
				if randpost.selftext=='':
					wholesomemsg=wholesomemsg+randpost.url
				else:
					wholesomemsg=wholesomemsg+randpost.selftext
				await client.send_message(message.channel,wholesomemsg)
				await client.delete_message(loading)		
			else:
				await client.send_message(message.channel,'You need {} more cash to use this command.'.format(20-yourcash))
		if args[0] == '/smile':
			if message.server == None:
				await client.send_message(message.channel,'You cannot use this command in private messages.')
				return
			yourcash=await getcash(message.server.id,message.author.id)
			if yourcash>=5:
				await givecash(message.server.id,message.channel,message.author.id,-5)
				await client.send_message(message.channel,'You spent `5` cash on this happy post!')
				loading=await client.send_message(message.channel,'Getting happiest posts!')
				reddit = praw.Reddit(client_id='hl3WbxS6F0Cm9Q',client_secret='ywFwrBCd1MEu9Kvt5DRMn-YFGto',user_agent='Test bot')
				submissions=[]
				for submission in reddit.subreddit('mademesmile').hot(limit=12):
					submissions.append(submission)
				submissions.pop(0)
				submissions.pop(0)
				randpost = random.choice(submissions)
				wholesomemsg='**'+randpost.title+'**\n'
				if randpost.selftext=='':
					wholesomemsg=wholesomemsg+randpost.url
				else:
					wholesomemsg=wholesomemsg+randpost.selftext
				await client.send_message(message.channel,wholesomemsg)
				await client.delete_message(loading)		
			else:
				await client.send_message(message.channel,'You need {} more cash to use this command.'.format(5-yourcash))
		if args[0] == '/copypasta':
			if message.server == None:
				await client.send_message(message.channel,'You cannot use this command in private messages.')
				return
			yourcash=await getcash(message.server.id,message.author.id)
			if yourcash>=7:
				await givecash(message.server.id,message.channel,message.author.id,-25)
				await client.send_message(message.channel,'You spent `25` cash on this dumb meme!')
				copypastalist=[]
				async for copypasta in client.logs_from(client.get_channel('424251230336843787'), limit=1000):
					copypastalist.append(copypasta.content)
				await client.send_message(message.channel,random.choice(copypastalist))
			else:
				await client.send_message(message.channel,'You need {} more cash to use this command.'.format(25-yourcash))
		if args[0] == '/image':
			if message.server == None:
				await client.send_message(message.channel,'You cannot use this command in private messages.')
				return
			try:
				yourcash=await getcash(message.server.id,message.author.id)
				if yourcash>=200:
					await givecash(message.server.id,message.channel,message.author.id,-200)
					try:
						imgargs=args[2]
					except:
						imgargs=''
					try:
						imgurl = message.attachments[0]['url']
					except:
						imgurl = args[-1]
					loading = await client.send_message(message.channel,'Generating image...')
					async with aiohttp.ClientSession() as client_session:
						async with client_session.get(imgurl) as response:
							image_bytes = await response.read()
							await editimage(image_bytes,args,imgargs)
						
						await client.send_message(message.channel,'You spent `200` cash on this picture')
						await client.delete_message(loading)
				else:
					await client.send_message(message.channel,'You need {} more cash to use this command.'.format(200-yourcash))
			except:
				await client.send_message(message.channel,'Error editing image. Make sure you actually put an image to edit.')
		if args[0] == '/tictactoe':
			await client.send_message(message.channel,'soon tm')
		if args[0] == '/lastupdate':
			lastupdateraw=time.time()-os.path.getmtime('4bitbot.py')
			days=int(lastupdateraw/86400)
			hours=int(lastupdateraw/3600-days*24)
			mins=int(lastupdateraw/60)-hours*60
			secs=int(lastupdateraw)-mins*60

			lastupdate2={'d':days,'h':hours,'m':mins,'s':secs}
			lastupdate=[]
			for i in lastupdate2:
				if lastupdate2[i]!=0:
					lastupdate.append(str(lastupdate2[i])+i)
			if len(lastupdate)==0:
				lastupdate=['Just now']
			lastupdate=', '.join(lastupdate)
			await client.send_message(message.channel,'Last update was {} ago'.format(lastupdate))
		if args[0] == '/cat':
			try:
				urllibdownloaded=await urllibget('https://aws.random.cat/meow')
			except Exception as e:
				await client.send_message(message.channel,'Error getting cat. Please try again later..')
				return
			try:
				cancontinue=True
				while cancontinue:
					await asyncio.sleep(0.5)
					try:
						ast.literal_eval(urllibdownloaded)
					except:
						pass
					else:
						cancontinue=False
				downloadedfile=ast.literal_eval(urllibdownloaded)
				catwebsite=str(downloadedfile['file'])
				catwebsite=catwebsite.replace('\\','')
				await client.send_message(message.channel,catwebsite)
			except Exception as e:
				await client.send_message(message.channel,'Error getting cat. Please try again later. ({}, {})'.format(str(e),errorlineno()))
				return
			#await client.send_file(message.channel,f,filename='cat.png',content='Here is your random cat :)')
		if args[0] == '/claim' or args[0] == '/daily':
			if await checkVoted(message.author.id):
				try:
					votesearch=0
					messagelist = []
					async for votesearch in client.logs_from(client.get_channel('442522542754889740'), limit=10000):
						messagelist.append(votesearch)
					allvotes=[]
					alreadyvoted=False
					for i in messagelist:
						if str(i.content).startswith(str(message.author.id)+' '):
							allvotes.append(i)
							lastvotetime=int(i.content.split()[1])
							nextvote=86400+(lastvotetime-int(time.time()))
							if nextvote >= 0:
								alreadyvoted=True
								if nextvote>=3600:
									if int(nextvote/3600)==1:
										nextvote='1 hour'
									else:
										nextvote=str(int(nextvote/3600))+' hours'
								elif nextvote>=60:
									if int(nextvote/60)==1:
										nextvote='1 minute'
									else:
										nextvote=str(int(nextvote/60))+' minutes'
								elif nextvote>=1:
									if int(nextvote)==1:
										nextvote='1 second'
									else:
										nextvote=str(int(nextvote/60))+' seconds'
					if alreadyvoted:
						await client.send_message(message.channel,'You have already voted today. You can vote again in `{}`'.format(nextvote))
					else:
						if len(allvotes) == 0:
							await client.send_message(discord.Object(id='442522542754889740'),
							str(message.author.id)+' '+		#adds user
							str(int(time.time())))			#adds current time
						else:
							for thevote in allvotes:
								lastvotetime=int(thevote.content.split()[1])
								nextvote=86400+(lastvotetime-int(time.time()))
								if nextvote <= 0:
									await client.delete_message(thevote)
									await client.send_message(discord.Object(id='442522542754889740'),
							str(message.author.id)+' '+		#adds user
							str(int(time.time())))			#adds current time
						await givecash(message.server.id,message.channel,message.author.id,25)
						await givexp(message.server.id,message.channel,message.author.id,45)
						await client.send_message(message.channel,'Thank you for voting! You have been rewarded 25 cash and 45 xp.')
				except Exception as e:
					await client.send_message(message.channel,'You have already voted today. Please try again later. (Debug: `{}`, `{}`)'.format(errorlineno(),e))
			else:
				await client.send_message(message.channel,'Please go to https://discordbots.org/bot/386333909362933772/vote to vote and type `/claim` again to get `25` cash and `45` xp.')
		if args[0] == '/vote':
				await client.send_message(message.channel,'Please go to https://discordbots.org/bot/386333909362933772/vote to vote then type `/claim` to earn `25` cash and `45` xp.')
		if args[0] == '/replit':
			if len(args) > 1:
				#try:
				if args[1]=='link':
					if len(args)==2:
						await client.send_message(message.channel,'Please use `/replit link replitusername` (case sensitive) to link your account')
						return
					loadmsg=await client.send_message(message.channel,'Trying to link your Discord account with your replit account...')
					yourname=message.author.name+'#'+str(message.author.discriminator)
					allcomments=await replitcomments()
					replitname=None
					for comment in allcomments:
						thecomment=list(comment.values())[0]
						theauthor=list(comment.keys())[0]
						if thecomment.startswith('/link '):
							try:
								if yourname==thecomment[6:]:
									if theauthor==args[2]:
										replitname=theauthor
							except:
								pass
					if replitname==None:
						await client.send_message(message.channel,'Could not link your Discord account with your repl.it account.\nPlease go to https://repl.it/ibuiltthis/bots/p/4bit-game-discord-bot and comment `/link {}` then type `/replit link {}` again.'.format(yourname,args[2]))
					elif await linkreplit(message.author.id,replitname):
						await client.send_message(message.channel,'Linked `{}` with `{}`'.format(replitname,yourname))
					else:
						await client.send_message(message.channel,'You have already linked your replit account')
					await client.delete_message(loadmsg)
				elif args[1]=='test':
					try:
						replitname=await findreplit(message.author.id)
						await client.send_message(message.channel,replitname)
					except Exception as e:
						await client.send_message(message.channel,e)
				elif args[1]=='myrepls':
					repls=await getrepls(await findreplit(message.author.id))
					replurls=[]
					for repl in repls:
						replurls.append('['+str(repl['url'])+']')
					await client.send_message(message.channel,'\nHere are your {} most recent repls:\n    {}'.format(len(repls),'\n    '.join(replurls)))
				elif args[1]=='top':
					try:
						args2=args[2].lower()
					except:
						args2='bots'
					await client.send_message(message.channel,await gettop('top',args2))
				elif args[1]=='trending':
					try:
						args2=args[2].lower()
					except:
						args2='bots'
					await client.send_message(message.channel,await gettop('trending',args2))
				elif args[1]=='new':
					try:
						args2=args[2].lower()
					except:
						args2='bots'
					await client.send_message(message.channel,await gettop('new',args2))
				elif args[1]=='help':
					await replithelp(message)
				else:
					await client.send_message(message.channel,'Invalid command. Try `/replit link replitusername` instead.')
				#except Exception as e:
				#	await logerror('(Debug: {}, {})'.format(errorlineno(),e))
			else:
				await client.send_message(message.channel,'https://repl.it')
		if args[0] == '/wikipedia':
			await client.send_message(message.channel,getwikipedia(' '.join(args[1:])))
		if args[0] in ['/wolfram','/ai','wolframalpha','artificialintelligence','wra','wr','alpha']:
			if len(args)==1:
				await client.send_message(message.channel,'Please use `{} question` to ask a question'.format(args[0]))
				return
			loadmsg=await client.send_message(message.channel,'Loading...')
			def doai(query,q):
				res=wolfram(query)
				q.put(res)
			q = queue.Queue()
			threading.Thread(target=doai, args=(' '.join(args[1:]),q)).start()
			output = q.get()
			await client.send_message(message.channel,'`'+output[0]+' = '+output[1]+'`')
			await client.delete_message(loadmsg)
		if args[0] == '/pay':
			try:
				if int(args[1]) >= 0:
					paycash=int(args[1])
					payto = message.server.get_member_named(' '.join(args[2:]))
					yourcash=int(await getcash(message.server.id,message.author.id))
					if payto.id==message.author.id:
						await client.send_message(message.channel,'You can\'t /pay yourself!')
						return
					elif  yourcash >= paycash:
						await givecash(message.server.id,message.channel,message.author.id,-paycash)
						await givecash(message.server.id,message.channel,payto.id,paycash)
						await client.send_message(message.channel,'Given `{}` cash to `{}`'.format(str(paycash),payto.name))
					else:
						await client.send_message(message.channel,'You need `{}` more cash to complete this transaction.'.format(paycash-yourcash))
				else:
					await client.send_message(message.channel,'Nice try.')
			except:
				await client.send_message(message.channel,'Incorrect usage. Please use /pay like this: `/pay 30 username#1234`')
		if args[0] == '/multiplayer' or args[0] == '/mp':
			if message.server==None:
				await client.send_message(message.channel,'You can\'t use this command in private messages.')
				return
			try:
				if args[1]=='help':
					await client.send_message(message.channel,'List of multiplayer games:\n`/mp coinflip <cash> <heads|tails>`')
				elif args[1] == 'coinflip':

					async def cfcheck(msg,cfcash):
						if msg.content=='/mp coinflip join {0}#{1}'.format(message.author.name,message.author.discriminator):
							pass
						elif msg.content=='/multiplayer coinflip join {0}#{1}'.format(message.author.name,message.author.discriminator):
							pass
						else:
							return False
						joincash=await getcash(msg.server.id,msg.author.id)
						if  joincash < int(cfcash):
							await client.send_message(msg.channel,'You need `{}` more cash to join this coinflip.'.format(int(cfcash)-joincash))
							return False
						else:
							return True

					if args[2]=='join':return
					try:
						if args[3][0]=='h':
							user1cf='h'
						elif args[3][0]=='t':
							user1cf='t'
						else:
							0/0 #ez error
						cfcash=str(int(args[2]))
						if int(cfcash) <= 0:
							await client.send_message(message.channel,'Nice try.')
							return
						yourcash=int(await getcash(message.server.id,message.author.id))
						if yourcash-int(cfcash) < 0:
							await client.send_message(message.channel,'You need {} more cash to do this coinflip.'.format(int(cfcash)-yourcash))
							return
						await client.send_message(message.channel,'Started new coinflip for `{0}` cash. Please type `/mp coinflip join {1}#{2}` to play against {1}.'.format(cfcash,message.author.name,message.author.discriminator))
						canpass=False
						while not canpass:
							cfmsg=await client.wait_for_message(channel=message.channel)
							canpass=await cfcheck(cfmsg,cfcash)
						if cfmsg.author.id == message.author.id:
							await client.send_message(message.channel,'You can\'t play against yourself! Canceled coinflip.')
						else:
							outcome=await mpcf(message)
							cfcash=int(cfcash)
							if outcome=='h':
								if user1cf == 'h':
									await givecash(message.server.id,message.channel,message.author.id,cfcash)
									await givecash(message.server.id,message.channel,cfmsg.author.id,0-cfcash)
									await client.send_message(message.channel,'{0} has earned `{1}` cash! :dollar:\n{2} has lost `{1}` cash! :money_with_wings:'.format(message.author.name,cfcash,cfmsg.author.name))
								else:
									await givecash(message.server.id,message.channel,message.author.id,0-cfcash)
									await givecash(message.server.id,message.channel,cfmsg.author.id,cfcash)
									await client.send_message(message.channel,'{2} has earned `{1}` cash! :dollar:\n{0} has lost `{1}` cash! :money_with_wings:'.format(message.author.name,cfcash,cfmsg.author.name))
							else:
								if user1cf == 't':
									await givecash(message.server.id,message.channel,message.author.id,cfcash)
									await givecash(message.server.id,message.channel,cfmsg.author.id,0-cfcash)
									await client.send_message(message.channel,'{0} has earned `{1}` cash! :dollar:\n{2} has lost `{1}` cash! :money_with_wings:'.format(message.author.name,cfcash,cfmsg.author.name))
								else:
									await givecash(message.server.id,message.channel,message.author.id,0-cfcash)
									await givecash(message.server.id,message.channel,cfmsg.author.id,cfcash)
									await client.send_message(message.channel,'{2} has earned `{1}` cash! :dollar:\n{0} has lost `{1}` cash! :money_with_wings:'.format(message.author.name,cfcash,cfmsg.author.name))

									
					except Exception as e:
						await client.send_message(message.channel,'Error creating coinflip. Please use `/mp coinflip <cash> <heads|tails>` to create a new coinflip. ({}, {})'.format(errorlineno(),e))
				elif args[1] == 'hl' or args[1] == 'higherlower' or args[1] == 'higherorlower':
					try:
						hlcash=int(args[2])
						try:
							hlmax=int(args[3])
						except:
							hlmax=10
						await client.send_message(message.author,'Please choose a number from 1-{} for your higherlower game.'.format(hlmax))
						def checkhl(msg):
							if msg.server==None:
								return True
							return False
						msg = await client.wait_for_message(author=message.author,check=checkhl)
						hlnumber=int(msg.content)
						if hlnumber in range(1,101):
							await client.send_message(message.author,'Created higherlower game in `{}`'.format(message.server.name))
							await client.send_message(message.channel,'{} has created a higherlower game. Guess a number from 1-{} to earn {} cash!'.format(message.author,hlmax,hlcash))
							def isnum(msg):
								try:
									int(msg)
									return True
								except:
									return False
							hlguess = await client.wait_for_message(author=message.author,channel=message.channel,check=isnum)
							if int(hlguess.content)==hlnumber:
								if hlmax>=100:
									await client.send_message(message.author,':bell: :bell: :bell: CORRECT!!! :bell: :bell: :bell:')
								elif hlmax>=50:
									await client.send_message(message.author,':bell: :bell: Correct!! :bell: :bell: ')
								elif hlmax>=15:
									await client.send_message(message.author,':bell: Correct! :bell:')
								else:
									await client.send_message(message.author,'Correct!')
								await client.send_message(message.author,'{0} has earned {1} cash and {2} has lost {1} cash!'.format(hlguess.author.name,hlcash,msg.author.name))
							else:
								await client.send_message(message.author,'Incorrect answer. {0} lost {1} cash but {} .'.format(hlguess.author.name,hlcash))
							pass #good
						else:
							await client.send_message(message.author,'Invalid number.')
							return
					except:
						await client.send_message(message.channel,'Error creating higherlower game. Please use `/mp higherlower <cash>` to start a higherlower game. ({}, {})'.format(errorlineno(),e))
				
				else:
					0/0
			except:
				await client.send_message(message.channel,'Incorrect usage. Please type `/mp help` for a list of multiplayer games.')
		if args[0] == '/uptime':
			uptimeraw=time.time()-programstarttime
			lastupdateraw=time.time()-os.path.getmtime('4bitbot.py')

			days=int(lastupdateraw/86400)
			hours=int(lastupdateraw/3600-days*24)
			mins=int(lastupdateraw/60)-hours*60
			secs=int(lastupdateraw)%60
			lastupdate2={'d':days,'h':hours,'m':mins,'s':secs}
			lastupdate=[]
			for i in lastupdate2:
				if lastupdate2[i]!=0:
					lastupdate.append(str(lastupdate2[i])+i)
			if len(lastupdate)==0:
				lastupdate=['Just now']
			lastupdate=', '.join(lastupdate)

			days=int(uptimeraw/86400)
			hours=int(uptimeraw/3600-days*24)
			mins=int(uptimeraw/60)-hours*60
			secs=int(uptimeraw)%60
			uptime2={'d':days,'h':hours,'m':mins,'s':secs}
			uptime=[]
			for i in uptime2:
				if uptime2[i]!=0:
					uptime.append(str(uptime2[i])+i)
			if len(uptime)==0:
				uptime=['Just now']
			uptime=', '.join(uptime)
			await client.send_message(message.channel,'Bot has been up for `{}`\nLast update was `{}` ago'.format(uptime,lastupdate))
		if args[0] == '/history':
			if message.author.id=='386333909362933772':
				return
			try:
				historylimit=int(args[1])
				if historylimit >= 100:
					return
			except:
				historylimit=10
			msgs=[]
			async for msg in client.logs_from(message.channel, limit=historylimit):
				msgs.append(msg.content)
			await client.send_message(message.channel,'\n'.join(msgs))
		if int(message.channel.id) == 422463427580133387:
			await client.delete_message(message)
			if args[0] == "/updateinfo":
				try:
					editmessage = await client.get_message(client.get_channel("422463427580133387"),str(422463807538069537))
				except:
					return
				catgifs = ['https://media1.tenor.com/images/3a0c9909b542717ce9f651d07c4d4592/tenor.gif?itemid=8985245','https://i.imgur.com/FH3pKLX.gif','https://i.imgur.com/kpspEWO.gif','https://i.imgur.com/yhEuukj.gif','https://i.imgur.com/jdIxvV4.gif','https://i.imgur.com/bFz5lbM.gif','https://media.giphy.com/media/Z56N0q0tsFC2k/giphy.gif','https://media.giphy.com/media/fiBlgzowrS9i/giphy.gif','http://38.media.tumblr.com/bdaea39db57dc0b48d763262514268db/tumblr_mgj44mNyST1s199fdo1_500.gif']
				await client.edit_message(editmessage,new_content='Please be patient while this loads. Here\'s a loading cat gif because why not\n'+random.choice(catgifs))
				allservers = ''
				invite = ''
				print(len(client.servers))
				for x in client.servers:
					allservers = allservers+'\n'+x.name
				await client.edit_message(editmessage,new_content= 'Connected to `'+str(len(client.servers))+'` servers\nConnected to `'+str(len(set(client.get_all_members())))+'` users\n\nServers: '+str(allservers))
				for x in client.servers:
					try:
						invite = str(await client.create_invite(list(x.channels)[0], max_age=300))
					except:
						invite = '`Invite could not be created for this server.`'
					allservers = allservers+'\n'+x.name+' - '+invite
					try:
						await client.edit_message(editmessage,new_content= 'Connected to `'+str(len(client.servers))+'` servers\nConnected to `'+str(len(set(client.get_all_members())))+'` users\n\nServers: '+str(allservers))
					except:
						return
				await client.clear_reactions(await client.get_message(client.get_channel("422463427580133387"),"422536559204761602"))
				await client.add_reaction(await client.get_message(client.get_channel("422463427580133387"),"422536559204761602"),"🆙")
				print("Reloading server list...")
		
		if int(message.channel.id) == 422832861004038155:
			if args[0] == "/pm":
				try:
					PMuser = await client.get_user_info(str(args[1]))
					await client.send_message(PMuser,' '.join(args[2:]))
					await client.send_message(message.channel,"Sent message to "+PMuser.name+'#'+PMuser.discriminator)
				except:
					client.send_message(message.channel,"You can't send messages to this user. You're either not in a server with them, or they blocked you.")
		if int(message.author.id) == 224588823898619905:
			if args[0] == '/dev':
				if args[1] == 'roles':
					roleprint=[]
					for role in message.server.roles:
						roleprint.append(role.name)
					await client.send_message(message.channel,'\n'.join(roleprint))
				if args[1] == 'isowner':
					rolenames=[]
					for role in message.author.roles:
						rolenames.append(role.name.lower())
					await client.send_message(message.channel,str('owner' in rolenames))
					#return 'owner' in rolenames
				if args[1] == 'echo':
					await client.send_message(message.channel,' '.join(args[2:]))
			if args[0] == '/python':
				if len(args) == 1:
					await client.send_message(message.channel,'Please specify whether you want to eval or exec. Example: /python eval\n1+1')
				try:
					if args[1] == 'exec':
						if len(args) == 2:
							await client.send_message(message.channel,'Enter Python code to run.')
							msg = await client.wait_for_message(author=message.author,channel=message.channel)
							msg = msg.content
						else:
							msg = ' '.join(args[2:])
						old_stdout = sys.stdout
						redirected_output = sys.stdout = StringIO()
						try:
							exec(msg,globals())
						except Exception as e:
							await client.send_message(message.channel,str(e))
						sys.stdout = old_stdout
						await client.send_message(message.channel,redirected_output.getvalue())
					elif args[1] == 'exec+':
						if len(args) == 2:
							await client.send_message(message.channel,'Enter Python code to run.')
							msg = await client.wait_for_message(author=message.author,channel=message.channel)
							old_stdout = sys.stdout
							redirected_output = sys.stdout = StringIO()
							try:
								msgcontent=msg.content
								msgcontent=msgcontent.replace('print(','await client.send_message(message.channel,')
								exec(msgcontent,globals(),locals())
								sys.stdout = old_stdout
								await client.send_message(message.channel,redirected_output.getvalue())
							except Exception as e:
								await client.send_message(message.channel,str(e))
								await client.send_message(message.channel,traceback.format_exc())

						
						else:
							msg = ' '.join(args[2:])
							old_stdout = sys.stdout
							redirected_output = sys.stdout = StringIO()
							try:
								exec(msg)
							except Exception as e:
								await client.send_message(message.channel,str(e))
							sys.stdout = old_stdout
							if redirected_output.getvalue() !='':
								await client.send_message(message.channel,redirected_output.getvalue())
					elif args[1] == 'eval':
						if len(args) == 2:
							await client.send_message(message.channel,'Enter Python code to run.')
							msg = await client.wait_for_message(author=message.author,channel=message.channel)
							splitmsg = msg.content.split('\n')
							print('\n'.join(splitmsg))
							for foundmsg in splitmsg:
								try:
									await client.send_message(message.channel,foundmsg+' >> '+str(eval(foundmsg)))
								except Exception as e:
									await client.send_message(message.channel,foundmsg+' >> '+str(e))
						else:
							msg = ' '.join(args[2:])
							splitmsg = msg.split('\n')
							print('\n'.join(splitmsg))
							for foundmsg in splitmsg:
								try:
									await client.send_message(message.channel,foundmsg+' >> '+str(eval(foundmsg)))
								except Exception as e:
									await client.send_message(message.channel,foundmsg+' >> '+str(e))
					else:
						await client.send_message(message.channel,'Please specify whether you want to eval or exec. Example: /python eval (enter) 1+1')
				except Exception as errormessage:
					await client.send_message(message.channel,'Error: '+str(errormessage))
				except:
					await client.send_message(message.channel,'REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')

#@client.event
#async def on_server_join(server):
#	await client.send_message(server.channels[0],'Thank you for inviting 4bitbot to your server!\nHere are some useful you need to get started:\n/help <page> - Shows a list of commands\n/hangman - Play a game of hangman to earn money\n/cash - Tells you how much cash you have (server specific)\n/suggest - Send a suggestion to the devs')




@client.event
async def on_socket_raw_receive(msg):
	try:
		message = json.loads(str(msg))
		if str(message['t']) == "MESSAGE_REACTION_ADD":
			if str(message['d']['message_id']) == "422536559204761602":
				if str(message['d']['emoji']['name']) == "🆙":
					if int(message['d']['user_id']) != 386333909362933772:
						await client.send_message(client.get_channel(message['d']['channel_id']), '/updateinfo')
	except:
		pass

#@client.event
#async def on_member_join(member):
	#await client.send_message(client.get_channel('422155643164819465'),'{0} has joined {1}'.format(str(member.name),str(member.server.name)))

try:
	client.run('Mzg2MzMzOTA5MzYyOTMzNzcy.DX35yQ.DH1-jaGe8xBXtV4WAF_mgH88CTs')
except:
	print("Error logging in.")