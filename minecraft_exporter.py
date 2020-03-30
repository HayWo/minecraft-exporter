from prometheus_client import start_http_server, REGISTRY, Metric
import time
import requests
import json
import nbt
import re
import os
from mcrcon import MCRcon
from os import listdir
from os.path import isfile, join

class MinecraftCollector(object):
    def __init__(self):
        self.statsdirectory = "/world/stats"
        self.playerdirectory = "/world/playerdata"
        self.advancementsdirectory = "/world/advancements"
        self.betterquesting = "/world/betterquesting"
        self.map = dict()
        self.questsEnabled = False
        if os.path.isdir(self.betterquesting):
            self.questsEnabled = True

    def get_players(self):
        return [f[:-5] for f in listdir(self.statsdirectory) if isfile(join(self.statsdirectory, f))]

    def uuid_to_player(self,uuid):
        uuid = uuid.replace('-','')
        if uuid in self.map:
            return self.map[uuid]
        else:
            result = requests.get('https://api.mojang.com/user/profiles/'+uuid+'/names')
            self.map[uuid] = result.json()[0]['name']
            return(result.json()[0]['name'])

    def get_player_stats(self,uuid):
        with open(self.statsdirectory+"/"+uuid+".json") as json_file:
            data = json.load(json_file)
            json_file.close()
        nbtfile = nbt.nbt.NBTFile(self.playerdirectory+"/"+uuid+".dat",'rb')
        data["stat.XpTotal"]  = nbtfile.get("XpTotal").value
        data["stat.XpLevel"]  = nbtfile.get("XpLevel").value
        data["stat.Score"]    = nbtfile.get("Score").value
        data["stat.Health"]   = nbtfile.get("Health").value
        data["stat.foodLevel"]= nbtfile.get("foodLevel").value
        with open(self.advancementsdirectory+"/"+uuid+".json") as json_file:
            count = 0
            advancements = json.load(json_file)
            for key, value in advancements.items():
                if key in ("DataVersion"):
                  continue
                if value["done"] == True:
                    count += 1
        data["stat.advancements"] = count
        if self.questsEnabled:
            data["stat.questsFinished"] = self.get_player_quests_finished(uuid)
        return data

    def update_metrics_for_player(self,uuid):
        data = self.get_player_stats(uuid)
        name = self.uuid_to_player(uuid)

        mc_items_crafted = Metric('mc_items_crafted','Blocks a Player mined',"counter")
        mc_items_broken = Metric('mc_items_broken','Blocks a Player mined',"counter")
        mc_items_mined = Metric('mc_items_mined','Blocks a Player mined',"counter")
        mc_chests_opened = Metric('mc_chests_opened','Blocks a Player mined',"counter")
        mc_damage_dealt = Metric('mc_damage_dealt','Blocks a Player mined',"counter")
        mc_damage_taken = Metric('mc_damage_taken','Blocks a Player mined',"counter")
        mc_time_since_rest = Metric('mc_time_since_rest','Blocks a Player mined',"counter")
        mc_sleeped_bed = Metric('mc_sleeped_bed','Blocks a Player mined',"counter")
        mc_minutes_played = Metric('mc_minutes_played','Blocks a Player mined',"counter")
        mc_interaction_with_furnace = Metric('mc_interaction_with_furnace','Blocks a Player mined',"counter")
        mc_jumps = Metric('mc_jumps','Blocks a Player mined',"counter")
        mc_time_sneaked = Metric('mc_time_sneaked','Blocks a Player mined',"counter")
        mc_deaths = Metric('mc_deaths','Blocks a Player mined',"counter")
        mc_drops = Metric('mc_drops','Blocks a Player mined',"counter")
        mc_time_since_death = Metric('mc_time_since_death','Blocks a Player mined',"counter")
        mc_left_game = Metric('mc_left_game','Blocks a Player mined',"counter")
        mc_craftingtable_used = Metric('mc_craftingtable_used','Blocks a Player mined',"counter")
        mc_animals_bred = Metric('mc_animals_bred','Blocks a Player mined',"counter")
        mc_kills_total = Metric('mc_kills_total','Blocks a Player mined',"counter")
        mc_killed_by = Metric('mc_killed_by','Blocks a Player mined',"counter")
        mc_items_used = Metric('mc_items_used','Blocks a Player mined',"counter")
        mc_pickedup_items_total = Metric('mc_pickedup_items_total','Blocks a Player mined',"counter")
        mc_kills = Metric('mc_kills','Blocks a Player mined',"counter")
        mc_dropped_items_total = Metric('mc_dropped_items_total','Blocks a Player mined',"counter")
        mc_cm_traveled = Metric('mc_cm_travelled','Blocks a Player mined',"counter")
        mc_xp_total = Metric('mc_xp_total','Blocks a Player mined',"counter")
        mc_current_level = Metric('mc_current_level','Blocks a Player mined',"counter")
        mc_food_level = Metric('mc_food_level','Blocks a Player mined',"counter")
        mc_health = Metric('mc_health','Blocks a Player mined',"counter")
        mc_score = Metric('mc_score','Blocks a Player mined',"counter")
        mc_advancements = Metric('mc_advancements','Blocks a Player mined',"counter")

        for key, value in data.items():
            if key in ("DataVersion"):
                continue
            elif key in ("stats"):
                stats = value
                for skey, sval in stats.items():
                    if skey == "minecraft:dropped":
                        for nkey, nval in sval.items():
                            mc_dropped_items_total.add_sample('mc_dropped_items_total',value=nval,labels={'player':name})
                    elif skey == "minecraft:killed":
                        for nkey, nval in sval.items():
                            if nkey == "minecraft:spider":
                                mc_kills.add_sample('mc_kills',value=nval,labels={'player':name, 'type':"spider"})
                            elif nkey == "minecraft:skeleton":
                                mc_kills.add_sample('mc_kills',value=nval,labels={'player':name, 'type':"skeleton"})
                            elif nkey == "minecraft:chicken":
                                mc_kills.add_sample('mc_kills',value=nval,labels={'player':name, 'type':"chicken"})
                            elif nkey == "minecraft:drowned":
                                mc_kills.add_sample('mc_kills.',value=nval,labels={'player':name, 'type':"drowned"})
                            elif nkey == "minecraft:zombie_villager":
                                mc_kills.add_sample('mc_kills',value=nval,labels={'player':name, 'type':"zombie_villager"})
                            elif nkey == "minecraft:squid":
                                mc_kills.add_sample('mc_kills',value=nval,labels={'player':name, 'type':"squid"})
                            elif nkey == "minecraft:sheep":
                                mc_kills.add_sample('mc_kills',value=nval,labels={'player':name, 'type':"sheep"})
                            elif nkey == "minecraft:zombie":
                                mc_kills.add_sample('mc_kills',value=nval,labels={'player':name, 'type':"zombie"})
                            else:
                                mc_kills.add_sample('mc_kills',value=nval,labels={'player':name, 'type':"other"})
                    elif skey == "minecraft:picked_up":
                        for nkey, nval in sval.items():
                            mc_pickedup_items_total.add_sample('mc_pickedup_items_total',value=nval,labels={'player':name})
                    elif skey == "minecraft:killed_by":
                        for nkey, nval in sval.items():
                            if nkey == "minecraft:spider":
                                mc_killed_by.add_sample('mc_killed_by',value=nval,labels={'player':name, 'type':"spider"})
                            elif nkey == "minecraft:skeleton":
                                mc_killed_by.add_sample('mc_killed_by',value=nval,labels={'player':name, 'type':"skeleton"})
                            elif nkey == "minecraft:chicken":
                                mc_killed_by.add_sample('mc_killed_by',value=nval,labels={'player':name, 'type':"chicken"})
                            elif nkey == "minecraft:drowned":
                                mc_killed_by.add_sample('mc_killed_by',value=nval,labels={'player':name, 'type':"drowned"})
                            elif nkey == "minecraft:zombie_villager":
                                mc_killed_by.add_sample('mc_killed_by',value=nval,labels={'player':name, 'type':"zombie_villager"})
                            elif nkey == "minecraft:squid":
                                mc_killed_by.add_sample('mc_killed_by',value=nval,labels={'player':name, 'type':"squid"})
                            elif nkey == "minecraft:sheep":
                                mc_killed_by.add_sample('mc_killed_by',value=nval,labels={'player':name, 'type':"sheep"})
                            elif nkey == "minecraft:zombie":
                                mc_killed_by.add_sample('mc_killed_by',value=nval,labels={'player':name, 'type':"zombie"})
                            else:
                                mc_killed_by.add_sample('mc_killed_by',value=nval,labels={'player':name, 'type':"other"})
                    elif skey == "minecraft:used":
                        for nkey, nval in sval.items():
                            mc_items_used.add_sample("mc_items_used",value=nval,labels={'player':name, 'type':"other"})
                    elif skey == "minecraft:custom":
                        for nkey, nval in sval.items():
                            if nkey == "minecraft:mob_kills":
                                mc_kills_total.add_sample('mc_kills_total',value=nval,labels={'player':name})
                            elif nkey == "minecraft:animals_bred":
                                mc_animals_bred.add_sample('mc_animals_bred',value=nval,labels={'player':name})
                            elif nkey == "minecraft:interact_with_crafting_table":
                                mc_craftingtable_used.add_sample('mc_craftingtable_used',value=nval,labels={'player':name})
                            elif nkey == "minecraft:leave_game":
                                mc_left_game.add_sample('mc_left_game',value=nval,labels={'player':name})
                            elif nkey == "minecraft:time_since_death":
                                mc_time_since_death.add_sample('mc_time_since_death',value=nval,labels={'player':name})
                            elif nkey == "minecraft:climb_one_cm":
                                mc_cm_traveled.add_sample("mc_cm_traveled",value=nval,labels={'player':name,'method':"climbing"})
                            elif nkey == "minecraft:sprint_one_cm":
                                mc_cm_traveled.add_sample("mc_cm_traveled",value=nval,labels={'player':name,'method':"sprinting"})
                            elif nkey == "minecraft:walk_one_cm":
                                mc_cm_traveled.add_sample("mc_cm_traveled",value=nval,labels={'player':name,'method':"walking"})
                            elif nkey == "minecraft:drop":
                                mc_drops.add_sample('mc_drops',value=nval,labels={'player':name})
                            elif nkey == "minecraft:deaths":
                                mc_deaths.add_sample('mc_deaths',value=nval,labels={'player':name})
                            elif nkey == "minecraft:sneak_time":
                                mc_time_sneaked.add_sample('mc_time_sneaked',value=nval,labels={'player':name})
                            elif nkey == "minecraft:walk_under_water_one_cm":
                                mc_cm_traveled.add_sample("mc_cm_traveled",value=nval,labels={'player':name,'method':"walking under water"})
                            elif nkey == "minecraft:boat_one_cm":
                                mc_cm_traveled.add_sample("mc_cm_traveled",value=nval,labels={'player':name,'method':"boating"})
                            elif nkey == "minecraft:jump":
                                mc_jumps.add_sample('mc_jumps',value=nval,labels={'player':name})
                            elif nkey == "minecraft:walk_on_water_one_cm":
                                mc_cm_traveled.add_sample("mc_cm_traveled",value=nval,labels={'player':name,'method':"walking on water"})
                            elif nkey == "minecraft:interact_with_furnace":
                                mc_interaction_with_furnace.add_sample('mc_interaction_with_furnace',value=nval,labels={'player':name})
                            elif nkey == "minecraft:play_one_minute":
                                mc_minutes_played.add_sample('mc_minutes_played',value=nval,labels={'player':name})
                            elif nkey == "minecraft:sleep_in_bed":
                                mc_sleeped_bed.add_sample('mc_sleeped_bed',value=nval,labels={'player':name})
                            elif nkey == "minecraft:time_since_rest":
                                mc_time_since_rest.add_sample('mc_time_since_rest',value=nval,labels={'player':name})
                            elif nkey == "minecraft:damage_taken":
                                mc_damage_taken.add_sample('mc_damage_taken',value=nval,labels={'player':name})
                            elif nkey == "minecraft:minecart_one_cm":
                                mc_cm_traveled.add_sample("mc_cm_traveled",value=nval,labels={'player':name,'method':"minecarting"})
                            elif nkey == "minecraft:damage_dealt":
                                mc_damage_dealt.add_sample('mc_damage_dealt',value=nval,labels={'player':name})
                            elif nkey == "minecraft:swim_one_cm":
                                mc_cm_traveled.add_sample("mc_cm_traveled",value=nval,labels={'player':name,'method':"swimming"})
                            elif nkey == "minecraft:fly_one_cm":
                                mc_cm_traveled.add_sample("mc_cm_traveled",value=nval,labels={'player':name,'method':"flying"})
                            elif nkey == "minecraft:open_chest":
                                mc_chests_opened.add_sample('mc_chests_opened',value=nval,labels={'player':name})
                            elif nkey == "minecraft:fall_one_cm":
                                mc_cm_traveled.add_sample("mc_cm_traveled",value=nval,labels={'player':name,'method':"falling"})
                            elif nkey == "minecraft:crouch_one_cm":
                                mc_cm_traveled.add_sample("mc_cm_traveled",value=nval,labels={'player':name,'method':"crouching"})
                    elif skey == "minecraft:mined":
                        for nkey, nval in sval.items():
                            if nkey == "minecraft:dirt":
                                mc_items_mined.add_sample('mc_items_mined',value=nval,labels={'player':name, 'type':"dirt"})
                            elif nkey == "minecraft:cobblestone":
                                mc_items_mined.add_sample('mc_items_mined',value=nval,labels={'player':name, 'type':"cobblestone"})
                            elif nkey == "minecraft:sand":
                                mc_items_mined.add_sample('mc_items_mined',value=nval,labels={'player':name, 'type':"sand"})
                            elif nkey == "minecraft:stone":
                                mc_items_mined.add_sample('mc_items_mined',value=nval,labels={'player':name, 'type':"stone"})
                            elif nkey == "minecraft:gravel":
                                mc_items_mined.add_sample('mc_items_mined',value=nval,labels={'player':name, 'type':"gravel"})
                            elif nkey == "minecraft:coal_ore":
                                mc_items_mined.add_sample("mc_items_mined",value=nval,labels={'player':name, 'type':"coal_ore"})
                            elif nkey == "minecraft:iron_ore":
                                mc_items_mined.add_sample("mc_items_mined",value=nval,labels={'player':name, 'type':"iron_ore"})
                            elif nkey == "minecraft:gold_ore":
                                mc_items_mined.add_sample("mc_items_mined",value=nval,labels={'player':name, 'type':"gold_ore")
                            elif nkey == "minecraft:crafting_table":
                                mc_items_mined.add_sample('mc_items_mined',value=nval,labels={'player':name, 'type':"crafting_table"})
                            elif nkey == "minecraft:sugar_cane":
                                mc_items_mined.add_sample('mc_items_mined',value=nval,labels={'player':name, 'type':"sugar_cane"})
                            elif nkey == "minecraft:torch":
                                mc_items_mined.add_sample('mc_items_mined',value=nval,labels={'player':name, 'type':"torch"})
                            elif nkey == "minecraft:chest":
                                mc_items_mined.add_sample("mc_items_mined",value=nval,labels={'player':name, 'type':"chest"})
                            else:
                                mc_items_mined.add_sample("mc_items_mined",value=nval,labels={'player':name, 'type':"other"})
                    elif skey == "minecraft:broken":
                        for nkey, nval in sval.items():
                            if nkey == "minecraft:stone_pickaxe":
                                mc_items_broken.add_sample('mc_items_broken',value=nval,labels={'player':name, 'type':"stone_pickaxe"})
                            elif nkey == "minecraft:stone_shovel":
                                mc_items_broken.add_sample("mc_items_broken",value=nval,labels={'player':name, 'type':"stone_shovel"})
                            elif nkey == "minecraft:stone_axe":
                                mc_items_broken.add_sample("mc_items_broken",value=nval,labels={'player':name, 'type':"stone_axe"})
                            elif nkey == "minecraft:stone_sword":
                                mc_items_broken.add_sample("mc_items_broken",value=nval,labels={'player':name, 'type':"stone_sword"})
                            elif nkey == "minecraft:stone_hoe":
                                mc_items_broken.add_sample("mc_items_broken",value=nval,labels={'player':name, 'type':"stone_hoe"})
                            else:
                                mc_items_broken.add_sample("mc_items_broken",value=nval,labels={'player':name, 'type':"other"})
                    elif skey == "minecraft:crafted":
                        for nkey, nval in sval.items():
                            mc_items_crafted.add_sample("mc_items_crafted",value=nval,labels={'player':name, 'type':"other"})
            else:
                stat = key.split(".")[1]
                if stat == "XpTotal":
                    mc_xp_total.add_sample('mc_xp_total',value=value,labels={'player':name})
                elif stat == "XpLevel":
                    mc_current_level.add_sample('mc_current_level',value=value,labels={'player':name})
                elif stat == "foodLevel":
                    mc_food_level.add_sample('mc_food_level',value=value,labels={'player':name})
                elif stat == "Health":
                    mc_health.add_sample('mc_health',value=value,labels={'player':name})
                elif stat == "Score":
                    mc_score.add_sample('mc_score',value=value,labels={'player':name})
                elif stat == "advancements":
                    mc_advancements.add_sample('mc_advancements',value=value,labels={'player':name})

        return [mc_items_crafted, mc_items_broken, mc_items_mined, mc_chests_opened, mc_damage_dealt, mc_damage_taken, mc_time_since_rest, mc_sleeped_bed, mc_minutes_played, mc_interaction_with_furnace, mc_jumps, mc_time_sneaked, mc_deaths, mc_drops, mc_time_since_death, mc_left_game, mc_craftingtable_used, mc_animals_bred, mc_kills_total, mc_killed_by, mc_items_used, mc_pickedup_items_total, mc_kills, mc_dropped_items_total, mc_cm_traveled, mc_xp_total, mc_current_level, mc_food_level, mc_health, mc_score, mc_advancements]

    def collect(self):
        for player in self.get_players():
            for metric in self.update_metrics_for_player(player):
                yield metric


if __name__ == '__main__':

    start_http_server(9055)
    REGISTRY.register(MinecraftCollector())
    print("Exporter started on Port 9055")
    while True:
        time.sleep(1)
