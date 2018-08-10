import json
import urllib.request
import urllib.parse


import asyncio
import discord

from discord.ext import commands


class Info:
	#bot=commands.Bot()
	api_key = "?api_key=RGAPI-66e6e8e6-cb0a-496f-92ff-bbe7dab825ab"
	summoner_url = u"https://kr.api.riotgames.com/lol/summoner/v3/summoners/by-name/"
	league_url=u"https://kr.api.riotgames.com/lol/league/v3/positions/by-summoner/"
	version_url=u"https://kr.api.riotgames.com/lol/static-data/v3/versions"


	def setVersion(self):
		print("setVersion")
		url=self.version_url+self.api_key
		print("%s"%url)
		try:
			response = urllib.request.urlopen(url)
			self.version = json.load(response)
			self.icon_url=u"http://ddragon.leagueoflegends.com/cdn/{0}/img/profileicon/".format(self.version[0])
		except:
			self.icon_url=u"http://ddragon.leagueoflegends.com/cdn/8.15.1/img/profileicon/"

	def setInfo(self,name):
		self.name_url=urllib.parse.quote_plus(name)
		#print(name)
		url=self.summoner_url+self.name_url+self.api_key
		response = urllib.request.urlopen(url)
		self.info = json.load(response)
		print("==============info==============")
		print(self.info)
		print("==============info==============")

	def setSoloRank(self):
		url = self.league_url+str(self.info['id'])+self.api_key
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


	def message(self,mode):

		if mode == 0:#id모드
			msg=discord.Embed()
			test=discord.Embed()
			msg.set_author(name=self.info['name'],icon_url=self.icon_url+str(self.info['profileIconId'])+".png")
			test.set_author(name=self.info['name'],icon_url=self.icon_url+str(self.info['profileIconId'])+".png")
			solo_msg=\
			self.solo['tier']+" "+self.solo['rank']+" %dLP"%self.solo['leaguePoints']+\
			"\n승: %d 패: %d"%(self.solo['wins'],self.solo['losses'])+\
			"\n승률: %.2lf%%"%(self.solo['wins']/(self.solo['wins']+self.solo['losses'])*100)
			team_msg=\
			self.team['tier']+" "+self.team['rank']+" %dLP"%self.team['leaguePoints']+\
			"\n승: %d 패: %d"%(self.team['wins'],self.team['losses'])+\
			"\n승률: %.2lf%%"%(self.team['wins']/(self.team['wins']+self.team['losses'])*100)

			msg.add_field(name="Level",value=str(self.info['summonerLevel']),inline=False)
			msg.add_field(name="솔로 랭크",value=solo_msg,inline=True)
			msg.add_field(name="자유 랭크",value=team_msg,inline=True)
			msg.add_field(name="test field",value=test,inline=True)
			#await self.bot.say(embed=msg)
			#await self.bot.say('test say')
			print("testmann==================")
			return msg
		#	msg= \
		#	"Level: %d"%self.info['summonerLevel']
