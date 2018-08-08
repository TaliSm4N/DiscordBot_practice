#-*-coding:utf-8-*-
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import asyncio
import discord
import random
import time
import pypubg

from discord.ext import commands

import json
import urllib.request
import urllib.parse


#client = discord.Client()

bot = commands.Bot(command_prefix='!')

# 1-6에서 생성된 토큰을 이곳에 입력해주세요.
token = "NDczNzE3OTYzODkyMDY0Mjg2.DkGAYw.Q2xSsrR_JzJNFTxJnpAnyr4D_dQ"


@bot.event
async def on_ready():
	print('login bot')
	print('username : {0}'.format(bot.user.name))
	print('ID : {0}'.format(bot.user.id))
	print('='*10)


@bot.command(pass_context=True)
async def test(ctx):
	print('hmm')
	await bot.say('test say {0}'.format(ctx.message.content))

@bot.command(pass_context=True)
async def dice(ctx,member: discord.Member = None):
	dice = random.randrange(1,7)
	if member is None:
		member = ctx.message.author
	chanel = ctx.message.channel
	id = member.id
#	id = id.split('#')[0]

	print('dice start {0}  dice %d'.format(member)%dice)
	await bot.say(id)

	await bot.say("<"+id+">님이 주사위를 굴렸습니다.")
	#awiat client.send_message(channel,"<@"+id+">님이 주사위를 굴렸습니다.")

	time.sleep(1)
	await bot.say('주사위의 결과는 %d입니다'%dice)

@bot.command(pass_context=True)
async def num(ctx,member: discord.Member = None):
	number = random.randrange(1,101)
	if member is None:
		member = ctx.message.author
	channel = ctx.message.channel
	id = member.id

	print('숫자 뽑기 시작 {0} 숫자는 %d'.format(member)%number)
	#await bot.say("<"+id+">님이 숫자를 뽑았습니다.")
	await bot.send_message(channel,"<@"+id+">님이 숫자를 뽑았습니다.")
	time.sleep(1)
	await bot.say('숫자의 결과는 %d입니다'%number)

@bot.command(pass_context=True)
async def vote(ctx,arg1):
	pass

@bot.command()
async def pubg(*args):
	if len(args)>0:
		profile=args[0]

@bot.command()
async def lol(*args):
	api_key="RGAPI-68f20a91-908e-4c30-94fa-b800e5555e5f"
	if len(args)>0:
		mode = args[0]
	name=""
	check = 0
	if mode=="id":
		for i in args[1:]:
			name += i
			if check != 0:
				name += "%20"


		name_url=urllib.parse.quote_plus(name)
		print(name)
		print(name_url)

		url=u"https://kr.api.riotgames.com/lol/summoner/v3/summoners/by-name/"+name_url+'?api_key='+api_key
		response = urllib.request.urlopen(url)

		info = json.load(response)
		id = info['id']
		url=u"https://kr.api.riotgames.com/lol/league/v3/positions/by-summoner/"+str(id)+'?api_key='+api_key
		response = urllib.request.urlopen(url)
		tier_info = json.load(response)

		print(info)
		print(tier_info)
		msg = \
		"ID: "+info['name']+\
		"\nLevel: %d"%info['summonerLevel']

		cnt = len(tier_info)

		for i in tier_info:
			if i["queueType"]=="RANKED_SOLO_5x5":
				msg+="\n------솔랭------"
			elif i["queueType"]=="RANKED_FLEX_TT":
				continue
			elif i["queueType"]=="RANKED_FLEX_SR":
				msg+="\n-----자유랭-----"
			msg+="\n랭크: "+i['tier']+" "+i['rank']+" %dLP"%i['leaguePoints']+\
			"\n승: %d 패: %d"%(i['wins'],i['losses'])+\
			"\n승률: %.2lf%%"%(i['wins']/(i['wins']+i['losses'])*100)+\
			"\n----------------\n"


		await bot.say(msg)





#client.run(token)
bot.run(token)

#####
###### 봇이 구동되었을 때 동작되는 코드입니다.
#####@client.event
#####async def on_ready():
#####	print("Logged in as ") #화면에 봇의 아이디, 닉네임이 출력됩니다.
#####	print(client.user.name)
#####	print(client.user.id)
#####	print("===========")
#####    # 디스코드에는 현재 본인이 어떤 게임을 플레이하는지 보여주는 기능이 있습니다.
#####    # 이 기능을 사용하여 봇의 상태를 간단하게 출력해줄 수 있습니다.
#####	await client.change_presence(game=discord.Game(name="반갑습니다 :D", type=1))
#####
###### 봇이 새로운 메시지를 수신했을때 동작되는 코드입니다.
#####@client.event
#####async def on_message(message):
#####	if message.author.bot: #만약 메시지를 보낸사람이 봇일 경우에는
#####		return None #동작하지 않고 무시합니다.
#####
#####	id = message.author.id #id라는 변수에는 메시지를 보낸사람의 ID를 담습니다.
#####	channel = message.channel #channel이라는 변수에는 메시지를 받은 채널의 ID를 담습니다.
#####
#####	if message.content.startswith('!커맨드'): #만약 해당 메시지가 '!커맨드' 로 시작하는 경우에는
#####		await client.send_message(channel, '커맨드') #봇은 해당 채널에 '커맨드' 라고 말합니다.
#####	elif message.content.startswith('_'):
#####			await client.send_message(channel,message.content)
#####			if()
#####	else: #위의 if에 해당되지 않는 경우
#####        #메시지를 보낸사람을 호출하며 말한 메시지 내용을 그대로 출력해줍니다.
#####		await client.send_message(channel, "<@"+id+">님이 \""+message.content+"\"라고 말하였습니다.")
#####
#####client.run(token)
#####
