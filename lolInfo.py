import json
import urllib.request
import urllib.parse


import asyncio
import discord

from discord.ext import commands


class Info:
	#bot=commands.Bot()
	#dataByld=True /// champ, spell
	api_key = "api_key=my_key"
	summoner_url = u"https://kr.api.riotgames.com/lol/summoner/v3/summoners/by-name/"
	league_url=u"https://kr.api.riotgames.com/lol/league/v3/positions/by-summoner/"
	version_url=u"https://kr.api.riotgames.com/lol/static-data/v3/versions"
	mastery_url=u"https://kr.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/"
	total_mastery_url=u"https://kr.api.riotgames.com/lol/champion-mastery/v3/scores/by-summoner/"
	match_list_url=u"https://kr.api.riotgames.com/lol/match/v3/matchlists/by-account/"
	match_url=u"https://kr.api.riotgames.com/lol/match/v3/matches/"
	spector_url=u"https://kr.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/"
	#rune_url=u"https://kr.api.riotgames.com/lol/static-data/v3/reforged-runes"
	#item_url=u"https://kr.api.riotgames.com/lol/static-data/v3/items"
	#spell_url=u"https://kr.api.riotgames.com/lol/static-data/v3/summoner-spells"
	#champ_url + "/" = 개별 챔피언 찾기
	#champ_url=u"https://kr.api.riotgames.com/lol/static-data/v3/champions"

	locale_url="locale=ko_KR"#item champ
	version_url="version="
	solo=[]
	team=[]
	last_match={}
	version = "8.15.1"

	def __init__(self):
		self.msg=discord.Embed()


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
		name_url=name
		print("setInfo")
		print(name)
		print(name_url)
		url=self.summoner_url+name_url+"?"+self.api_key
		print(url)
		response = urllib.request.urlopen(url)
		self.info = json.load(response)
		print("==============info==============")
		print(self.info)
		print("==============info==============")
		self.msg.set_author(name=self.info['name'],icon_url=self.icon_url+str(self.info['profileIconId'])+".png")
		self.msg.add_field(name="Level",value=str(self.info['summonerLevel']),inline=True)


	def setSoloRank(self):
		url = self.league_url+str(self.info['id'])+"?"+self.api_key
		response = urllib.request.urlopen(url)
		tier_info = json.load(response)

		solo=[]
		team=[]

		for i in tier_info:
			if i["queueType"]=="RANKED_SOLO_5x5":
				solo=i#솔랭
				print("==============solo==============")
				print(solo)
				print("==============solo==============")
			elif i["queueType"]=="RANKED_FLEX_SR":
				team=i#자유랭
				print("==============team==============")
				print(team)
				print("==============team==============")

		if solo != []:
			solo_msg=\
			solo['tier']+" "+solo['rank']+" %dLP"%solo['leaguePoints']+\
			"\n%d승 %d패"%(solo['wins'],solo['losses'])+\
			"\n승률: %.2lf%%\n "%(solo['wins']/(solo['wins']+solo['losses'])*100)
			if solo['tier']=="BRONZE":
				self.msg.colour=0x9C5221
			elif solo['tier']=="SILVER":
				self.msg.colour=0xC2BDB0
			elif solo['tier']=="GOLD":
				self.msg.colour=0xE7BD42
			elif solo['tier']=="PLATINUM":
				self.msg.colour=0xB9B8B3
			elif solo['tier']=="DIAMOND":
				self.msg.colour=0xFAF7E2
			elif solo['tier']=="MASTER":
				self.msg.colour=0xC0D5C2
			elif solo['tier']=="CHALLENGER":
				self.msg.colour=0xCEE4EE
		else:
			solo_msg ="UNRANKED\n "
		if team != []:
			team_msg=\
			team['tier']+" "+team['rank']+" %dLP"%team['leaguePoints']+\
			"\n%d승 %d패"%(team['wins'],team['losses'])+\
			"\n승률: %.2lf%%\n "%(team['wins']/(team['wins']+team['losses'])*100)
		else:
			team_msg="UNRANKED\n "



		self.msg.add_field(name="솔로 랭크",value=solo_msg,inline=True)
		self.msg.add_field(name="자유 랭크",value=team_msg,inline=True)
		self.msg.add_field(name=".",value='.',inline=True)

	def setChampInfo(self,name):
		f=open("./info/json/champion.json")
		a_champ=json.load(f)

		for i in a_champ["data"]:
			if a_champ["data"][i]["name"]==name:
				key=i
				print(name)
				break
		close(f)

		f=open("./info/json/champion/"+key+".json")
		champ=json.load(f)
		close(f)


	#	self.champ_msg=\





	def setDataSet(self):
		pass

	def setTopChamp(self):
		url=self.mastery_url+str(self.info['id'])+"?"+self.api_key
		total_url=self.total_mastery_url+str(self.info['id'])+"?"+self.api_key
		response = urllib.request.urlopen(url)
		total_response = urllib.request.urlopen(total_url)
		master = json.load(response)
		total_master = json.load(total_response)

		master_msg="전체 숙련도: [%d]\n"%total_master

		#f2=open("./info/json/queueid.json")

		#queue=json.load(f2)
		try:
			for i in range(0,3):
				for j in self.champ['data']:
					if int(self.champ['data'][j]['key'])==master[i]['championId']:
						master_msg+="%d. "%(i+1)+self.champ['data'][j]['name']+"["+"%d"%master[i]['championLevel']+"]: "+" %d\n "%master[i]['championPoints']
						break
		except IndexError:
			pass
		finally:
			self.msg.add_field(name="숙련도",value=master_msg,inline=True)



	def setMatchList(self,num):
		url=self.match_list_url+str(self.info['accountId'])+"?"+self.api_key
		response = urllib.request.urlopen(url)
		match_list=json.load(response)
		win = 0
		lose = 0
		try:
			for i in range(0,num):
				print(match_list['matches'][i]['gameId'])
				url=self.match_url+str(match_list['matches'][i]['gameId'])+"?"+self.api_key
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
					win+=1
				else:
					lose+=1


				if i == 0:
					self.last_match=match
					self.id =j
		except IndexError:
			pass
		finally:
				#self.last_result = match['teams'][team]['win']
				print("win:%d lose:%d"%(win, lose))
				if win+lose !=0:
					win_rate=win/(win+lose)*100
				else:
					win_rate=0
				win_rate_msg = "%d승 %d패\n승률: %d%%\n "%(win,lose,win_rate)

				self.msg.add_field(name="최근 %d게임"%(win+lose),value=win_rate_msg,inline=True)
				self.msg.add_field(name=".",value='.',inline=True)


	def setMyMatch(self,match,id):

		if match=={}:
			self.msg.add_field(name="마지막 게임",value="플레이 기록이 없습니다.",inline=True)
			self.msg.add_field(name=".",value='.',inline=True)

		min = int(match["gameDuration"]/60)
		sec = match["gameDuration"]%60

		last_match_msg=self.queue[str(match["queueId"])]+" "
		if match["participants"][id]["stats"]["win"] == True:
			last_match_msg+="<승> "
		else:
			last_match_msg+="<패> "
		last_match_msg+="(%d분 %d초)\n"%(min,sec)
		for i in self.champ['data']:
			if int(self.champ['data'][i]['key'])==match["participants"][id]["championId"]:
				last_match_msg+=self.champ['data'][i]['name']+" "+str(match["participants"][id]["stats"]["champLevel"])+"\n"
				break
		last_match_msg+="KDA:%d/%d/%d "%(match["participants"][id]["stats"]["kills"],match["participants"][id]["stats"]["deaths"],match["participants"][id]["stats"]["assists"])+\
		"[CS %d]\n"%(match["participants"][id]["stats"]["totalMinionsKilled"]+match["participants"][id]["stats"]["neutralMinionsKilled"])
		#"연속킬 : %d\n"%match["participants"][id]["stats"]["killingSprees"]


		if match["participants"][id]["stats"]["firstBloodKill"]!=0:
			last_match_msg+="퍼블 "

		if match["participants"][id]["stats"]["quadraKills"]!=0:
			last_match_msg+="쿼드라킬 "

		if match["participants"][id]["stats"]["pentaKills"]!=0:
			last_match_msg+="펜타킬 "
		last_match_msg+="\n "

		self.msg.add_field(name="마지막 게임",value=last_match_msg,inline=True)
		self.msg.add_field(name=".",value='.',inline=True)

	def setSpector(self):
		url = self.spector_url+str(self.info['id'])+"?"+self.api_key
		try:
			response = urllib.request.urlopen(url)
			spector=json.load(response)

			spector_msg=self.queue[str(spector["gameQueueConfigId"])]+" "

			for i in range(0,10):
				if spector["participants"][i]["summonerName"]==self.info["name"]:
					for j in self.champ['data']:
						if int(self.champ['data'][j]['key'])==spector["participants"][i]["championId"]:
							spector_msg+=self.champ['data'][j]['name']+" 플레이 중\n"
							break
					break

		except:
			print("spector except")
			spector_msg="현재 게임 중이 아닙니다\n"
		finally:
			self.msg.add_field(name="진행 중인 게임",value=spector_msg,inline=False)

	def ID(self,name=""):
		f=open("./info/json/champion.json")
		f2=open("./info/json/queueid.json")
		self.champ=json.load(f)
		self.queue=json.load(f2)
		f.close()
		f2.close()
		self.setVersion()
		self.setInfo(name)
		self.setMatchList(20)
		self.setSoloRank()
		self.setTopChamp()
		self.setMyMatch(self.last_match,self.id)
		self.setSpector()

		return self.msg
