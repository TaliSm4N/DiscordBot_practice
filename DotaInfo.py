import dota2api

import json

class Info:
	api=dota2api.Initialise(api_key="my_key",language="ko_KR",raw_mode=False)

	def __init__(self):
		pass

	def setInfo(self,name):
		pass

	def setDataSet(self):
		with open("./dota_info/json/hero.json","w") as f:
			a_hero=self.api.get_heroes()
			f.write(json.dumps(a_hero, ensure_ascii=False, indent="\t"))
			print(json.dumps(a_hero, ensure_ascii=False, indent="\t"))
		with open("./dota_info/json/item.json","w") as f:
			a_item=self.api.get_game_items()
			f.write(json.dumps(a_item, ensure_ascii=False, indent="\t"))
			print(json.dumps(a_item, ensure_ascii=False, indent="\t"))
