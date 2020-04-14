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

## TODO
Add more items that are exolicitly named.

## Metrics

```
mc_items_crafted_total
mc_items_broken_total
mc_items_mined_total
mc_chests_opened_total
mc_damage_dealt_total
mc_damage_taken_total
mc_time_since_rest_total
mc_sleeped_bed_total
mc_minutes_played_total
mc_interaction_with_furnace_total
mc_jumps_total
mc_time_sneaked_total
mc_deaths_total
mc_drops_total
mc_time_since_death_total
mc_left_game_total
mc_craftingtable_used_total
mc_animals_bred_total
mc_kills_total
mc_killed_by_total
mc_items_used
mc_pickedup_items_total
mc_kills_absolute_total
mc_dropped_items_total
mc_cm_traveled_total
mc_xp_total_total
mc_current_level
mc_food_level
mc_health_total
mc_score_total
mc_advancements_total
```


## Dashboards

In the folder dashboards you'll find grafana dashboards for these metrics, they are however incomplete and can be expanded
