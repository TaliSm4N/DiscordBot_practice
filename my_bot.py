#-*-coding:utf-8-*-
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import asyncio
import discord
import random
import time
#import pypubg
import lolInfo
import dota2api

from discord.ext import commands

import json
import urllib.request
import urllib.parse


#client = discord.Client()

bot = commands.Bot(command_prefix='!')
#image=open("./tier-icons/Provisional.png", "rb")
#ima=image.read()
#tester=bot.create_custom_emoji(discord.server,name="name",image=ima)


# 1-6에서 생성된 토큰을 이곳에 입력해주세요.
token = "my_key"

#lol_info.setDataSet()


@bot.event
async def on_ready():
	print('login bot')
	print('username : {0}'.format(bot.user.name))
	print('ID : {0}'.format(bot.user.id))
	print('='*10)



@bot.command(pass_context=True)
async def test(ctx):
	print('hmm')

@bot.command(pass_context=True)
async def dice(ctx,member: discord.Member = None):
	dice = random.randrange(1,7)
	if member is None:
		member = ctx.message.author

		msg=discord.Embed(title='주사위 결과',description='%d'%dice,colour=0xDEADBF)

		if member.avatar_url=="":
			icon=member.default_avatar_url
		else:
			icon=member.avatar_url

		msg.set_author(name=member.display_name,icon_url=icon)
		msg.add_field(name="test field",value="test value",inline=True)

		await bot.say(embed=msg)


@bot.command(pass_context=True)
async def num(ctx,member: discord.Member = None):
	number = random.randrange(1,101)
	if member is None:
		member = ctx.message.author

	print('숫자 뽑기 시작 {0} 숫자는 %d'.format(member)%number)
	#await bot.say("<"+id+">님이 숫자를 뽑았습니다.")
	#await bot.send_message(channel,"<@"+id+">님이 숫자를 뽑았습니다.")

	#time.sleep(1)
	#await bot.say('숫자의 결과는 %d입니다'%number)
	#await bot.say(embed=msg)
	msg=discord.Embed(title='숫자 뽑기 결과',description='%d'%number,colour=0xDEADBF)

	if member.avatar_url=="":
		icon=member.default_avatar_url
	else:
		icon=member.avatar_url

	msg.set_author(name=member.display_name,icon_url=icon)
	await bot.say(embed=msg)

	#test=discord.Embed(title='My Embed Title', description='My Embed Content.', colour=0xDEADBF)
	#test.set_author(name='Someone', icon_url=bot.user.default_avatar_url)
	#await bot.say(msg)
	#await bot.say(embed=test)

@bot.command(pass_context=True)
async def vote(ctx,arg1):
	pass

@bot.command()
async def pubg(*args):
	if len(args)>0:
		profile=args[0]

@bot.command()
async def 롤(*args):
	await lol(args)

@bot.command()
async def lol(*args):

	token_msg=\
	"(msg) -> msg를 필수적으로 입력하지 않아도 됩니다.\n"+\
	"A/B/C.. -> A,B,C,... 중 하나만 입력해야합니다.\n"+\
	"[msg] -> 명령어에 맞게 msg를 반드시 입력해야합니다.\n"
	command_msg=\
	"!lol (?/help/도움) : !lol명령어의 도움말을 출력합니다.\n"+\
	"!lol id/계정 [소환사명] : 해당 소환사의 정보를 가져옵니다.\n"+\
	"!lol champ/챔프/챔 [챔피언이름] : 해당 챔피언의 정보를 가져옵니다.\n"

	lol_info=lolInfo.Info()
	if len(args)>0:
		mode = args[0]
	else:
		e=discord.Embed(title="!lol 도움말",description=command_msg)
		e.add_field(name="기호 안내",value=token_msg)

		await bot.say(embed=e)
		return
	name=""
	#lol_info=lolInfo.Info()


	if mode=="id" or mode=="계정":
		for i in args[1:]:
			name += i
			name += " "
		print("first:"+name)
		name=name[0:-1]
		print("second:"+name)
		msg=lol_info.ID(name)
		await bot.say(embed=msg)
	elif mode == "champ" or mode=="챔프" or mode=="챔":
		for i in args[1:]:
			name += i
			name +=" "

		name = name[0:-1]
		print(name)
		msg=lol_info.setChampInfo(name)
		await bot.say(embed=msg)
	elif mode=="업뎃" or mode=="update":
		lol_info.setDataSet()
		await bot.say("완료")
	elif mode=="help" or mode=="?" or mode=="도움":
		e=discord.Embed(title="!lol 도움말",description=command_msg)
		e.add_field(name="기호 안내",value=token_msg)
		await bot.say(embed=e)
	else:
		error_msg="!lol %s"%mode
		for i in args[1:]:
			error_msg += i
			error_msg +=" "
		e=discord.Embed(title="없는 명령",description=error_msg)
		e.add_field(name="!lol 도움말",value=command_msg)
		e.add_field(name="기호 안내",value=token_msg)
		await bot.say(embed=e)

@bot.command()
async def dota(*args):
	pass





	#api_key="RGAPI-66e6e8e6-cb0a-496f-92ff-bbe7dab825ab"
	#name_url=urllib.parse.quote_plus(name)
	#print(name)
	#print(name_url)

	#url=u"https://kr.api.riotgames.com/lol/summoner/v3/summoners/by-name/"+name_url+'?api_key='+api_key
	#response = urllib.request.urlopen(url)

	#info = json.load(response)
	#id = info['id']
	#url=u"https://kr.api.riotgames.com/lol/league/v3/positions/by-summoner/"+str(id)+'?api_key='+api_key
	#response = urllib.request.urlopen(url)
	#tier_info = json.load(response)

	##print(info)
	##print(tier_info)
	#msg = \
	#"ID: "+info['name']+\
	#"\nLevel: %d"%info['summonerLevel']

	#cnt = len(tier_info)

	#for i in tier_info:
	#	if i["queueType"]=="RANKED_SOLO_5x5":
	#		msg+="\n------솔랭------"
	#	elif i["queueType"]=="RANKED_FLEX_TT":
	#		continue
	#	elif i["queueType"]=="RANKED_FLEX_SR":
	#		msg+="\n-----자유랭-----"
	#	msg+="\n랭크: "+i['tier']+" "+i['rank']+" %dLP"%i['leaguePoints']+\
	#	"\n승: %d 패: %d"%(i['wins'],i['losses'])+\
	#	"\n승률: %.2lf%%"%(i['wins']/(i['wins']+i['losses'])*100)+\
	#	"\n----------------\n"

	#test=discord.Embed(title='My Embed Title', description='My Embed Content.', colour=0xDEADBF)
	#test.set_author(name='Someone', icon_url=bot.user.default_avatar_url)
	#await bot.say(msg)
	#await bot.say(embed=test)






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
