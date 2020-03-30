# minecraft-exporter

this is a prometheus exporter for the vanilla minecraft server
This exporter reads minecrafts nbt files, the advancements files.

## setup

- clone this repo
- `cd minecraft-exporter`
- create virtualenv `virtualenv -p /usr/bin/python3 .`
- activate virtualenv `source bin/activate`
- install requirements `pip install -r requirements.txt`
- make startscript executable `chmod +x startscript.sh`
- ad link to the world folder `ln -s /path/to/world world`

## Usage

- activate virtualenv `source bin/activate`
- run startscript `./startscript.sh`

## Metrics

```
mc_items_crafted
mc_items_broken
mc_items_mined
mc_chests_opened
mc_damage_dealt
mc_damage_taken
mc_time_since_rest
mc_sleeped_bed
mc_minutes_played
mc_interaction_with_furnace
mc_jumps
mc_time_sneaked
mc_deaths
mc_drops
mc_time_since_death
mc_left_game
mc_craftingtable_used
mc_animals_bred
mc_kills_total
mc_killed_by
mc_items_used
mc_pickedup_items_total
mc_kills
mc_dropped_items_total
mc_cm_traveled
mc_xp_total
mc_current_level
mc_food_level
mc_health
mc_score
mc_advancements
```


## Dashboards
### Not yet working in this fork

In the folder dashboards you'll find grafana dashboards for these metrics, they are however incomplete and can be expanded
