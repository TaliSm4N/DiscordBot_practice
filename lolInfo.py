import json
import urllib.request
import urllib.parse


import asyncio
import discord

from discord.ext import commands


class Info:
	#bot=commands.Bot()
	#dataByld=True /// champ, spell
	api_key = "api_key=RGAPI-db7abb8d-362a-4adb-a1f3-dd91174738eb"
	summoner_url = u"https://kr.api.riotgames.com/lol/summoner/v3/summoners/by-name/"
	league_url=u"https://kr.api.riotgames.com/lol/league/v3/positions/by-summoner/"
	version_url=u"https://kr.api.riotgames.com/lol/static-data/v3/versions"
	mastery_url=u"https://kr.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/"
	total_mastery_url=u"https://kr.api.riotgames.com/lol/champion-mastery/v3/scores/by-summoner/"
	match_list_url=u"https://kr.api.riotgames.com/lol/match/v3/matchlists/by-account/"
	match_url=u"https://kr.api.riotgames.com/lol/match/v3/matches/"
	#rune_url=u"https://kr.api.riotgames.com/lol/static-data/v3/reforged-runes"
	#item_url=u"https://kr.api.riotgames.com/lol/static-data/v3/items"
	#spell_url=u"https://kr.api.riotgames.com/lol/static-data/v3/summoner-spells"
	#champ_url + "/" = 개별 챔피언 찾기
	#champ_url=u"https://kr.api.riotgames.com/lol/static-data/v3/champions"

	locale_url="locale=ko_KR"#item champ
	version_url="version="
	solo=[]
	team=[]
	version = "8.15.1"


	def setVersion(self):
		print("setVersion")
		url=self.version_url+"?"+self.api_key
		try:
			response = urllib.request.urlopen(url)
			v = json.load(response)
			self.version = v[0]

		except:
			print("version except")
		finally:
			self.version_url+=self.version
			self.icon_url=u"http://ddragon.leagueoflegends.com/cdn/{0}/img/profileicon/".format(self.version)
			print(self.icon_url)
			#self.champ_url=u"http://ddragon.leagueoflegends.com/cdn/{0}/data/ko_KR/champion.json".format(self.version[0])
			#self.indiv_champ_url=u"http://ddragon.leagueoflegends.com/cdn/{0}/data/ko_KR/champion/".format(self.version[0])

	def setInfo(self,name):
		self.name_url=name
		print("setInfo")
		print(name)
		print(self.name_url)
		url=self.summoner_url+self.name_url+"?"+self.api_key
		print(url)
		response = urllib.request.urlopen(url)
		self.info = json.load(response)
		print("==============info==============")
		print(self.info)
		print("==============info==============")

	def setSoloRank(self):
		url = self.league_url+str(self.info['id'])+"?"+self.api_key
		response = urllib.request.urlopen(url)
		tier_info = json.load(response)

		for i in tier_info:
			if i["queueType"]=="RANKED_SOLO_5x5":
				self.solo=i#솔랭
				print("==============solo==============")
				print(self.solo)
				print("==============solo==============")
			elif i["queueType"]=="RANKED_FLEX_SR":
				self.team=i#자유랭
				print("==============team==============")
				print(self.team)
				print("==============team==============")

	def setChampAllInfo(self):
		url=self.champ_url+"?"+self.locale_url+"&"+self.version_url+"&tags=all&dataByld=true"+"&"+self.api_key
		try:
			response = urllib.request.urlopen(url)
			data = json.load(response)
			self.champ_info = open("./champ_info.json","w")
			self.champ_info.write(data)
			self.champ_info.close()
		except:
			print("champInfo except")

#	def setDataSet(self):
#		self.setVersion()
		#self.setChampAllInfo()

	def setTopChamp(self):
		url=self.mastery_url+str(self.info['id'])+"?"+self.api_key
		total_url=self.total_mastery_url+str(self.info['id'])+"?"+self.api_key
		response = urllib.request.urlopen(url)
		total_response = urllib.request.urlopen(total_url)
		self.master = json.load(response)
		self.total_master = json.load(total_response)

	def setMatchList(self):
		url=self.match_list_url+str(self.info['accountId'])+"?"+self.api_key
		response = urllib.request.urlopen(url)
		self.match_list=json.load(response)

	def setMatch(self):
		self.win = 0
		self.lose = 0
		for i in range(0,20):
			print(self.match_list['matches'][i]['gameId'])
			url=self.match_url+str(self.match_list['matches'][i]['gameId'])+"?"+self.api_key
			response = urllib.request.urlopen(url)
			match=json.load(response)
			for j in range(0,10):
				if match["participantIdentities"][j]["player"]["summonerName"]==self.info['name']:
					if j<5:
						team=0
						break
					else:
						team=1
						break
			if match['teams'][team]['win']=="Win":
				self.win+=1
			else:
				self.lose+=1

			if i == 0:
				self.last_match=match
				#self.last_result = match['teams'][team]['win']
		print("win:%d lose:%d"%(self.win, self.lose))


	def message(self,mode):

		if mode == 0:#id모드
			msg=discord.Embed()
			print(self.icon_url+str(self.info['profileIconId'])+".png")
			msg.set_author(name=self.info['name'],icon_url=self.icon_url+str(self.info['profileIconId'])+".png")
			if self.solo != []:
				solo_msg=\
				self.solo['tier']+" "+self.solo['rank']+" %dLP"%self.solo['leaguePoints']+\
				"\n%d승 %d패"%(self.solo['wins'],self.solo['losses'])+\
				"\n승률: %.2lf%%"%(self.solo['wins']/(self.solo['wins']+self.solo['losses'])*100)
			else:
				solo_msg ="UNRANKED"
			if self.team != []:
				team_msg=\
				self.team['tier']+" "+self.team['rank']+" %dLP"%self.team['leaguePoints']+\
				"\n%d승 %d패"%(self.team['wins'],self.team['losses'])+\
				"\n승률: %.2lf%%"%(self.team['wins']/(self.team['wins']+self.team['losses'])*100)
			else:
				team_msg="UNRANKED"

			master_msg="전체 숙련도: [%d]\n"%self.total_master
			f=open("./info/json/champion.json")
			#f2=open("./info/json/queueid.json")
			champ=json.load(f)
			#queue=json.load(f2)
			for i in range(0,3):
				for j in champ['data']:
					if int(champ['data'][j]['key'])==self.master[i]['championId']:
						master_msg+="%d. "%(i+1)+champ['data'][j]['name']+"["+"%d"%self.master[i]['championLevel']+"]: "+" %d\n"%self.master[i]['championPoints']
						break
			#last_match_msg=\
			#queue[str(self.last_match["queueId"])]+"\n"+\
			#""

			#print("master_msg: "+master_msg)


			win_rate_msg = "%d승 %d패\n승률: %d%%"%(self.win,self.lose,self.win/20*100)


			msg.add_field(name="Level",value=str(self.info['summonerLevel']),inline=True)
			msg.add_field(name="최근 20게임",value=win_rate_msg,inline=False)
			#msg.add_field(name="　",value="　",inline=True)
			msg.add_field(name="솔로 랭크",value=solo_msg,inline=True)
			msg.add_field(name="자유 랭크",value=team_msg,inline=True)
			#msg.add_field(name="　",value="　",inline=True)
			msg.add_field(name="숙련도",value=master_msg,inline=False)


			#await self.bot.say(embed=msg)
			#await self.bot.say('test say')
			print("testmann==================")
			return msg
		#	msg= \
		#	"Level: %d"%self.info['summonerLevel']
