import itertools
import json
import pkgutil
from worlds.sm_map_rando import GetAPWorldPath, SMMapRandoWorld
from pysmmaprando import build_app_data

# Run like this:
# Archipelago>python -m worlds.sm_map_rando.tools.generateLocsAndItemsDicts

location_address_to_id = json.loads(pkgutil.get_data(__name__, "/".join(("..", "data", "loc_address_to_id.json"))).decode("utf-8"))

map_rando_app_data = build_app_data(GetAPWorldPath())

location_names = map_rando_app_data.game_data.get_location_names()

item_name_to_id = {
    item_name: SMMapRandoWorld.items_start_id + idx for idx, item_name in 
        enumerate(itertools.chain(
            map_rando_app_data.game_data.item_isv.keys,
            [
                "ArchipelagoItem",
                "ArchipelagoProgItem",
                "ArchipelagoUsefulItem",
                "ArchipelagoUsefulProgItem",
                "ProgMissile", 
                "ProgSuper", 
                "ProgPowerBomb"
            ]
        ))
    }

location_name_to_id = {
    loc_name: SMMapRandoWorld.locations_start_id + location_address_to_id[str(addr)] for idx, (loc_name, addr) in 
        enumerate(itertools.chain(zip(location_names, map_rando_app_data.game_data.get_location_addresses())))
    }

def DumpToJSONFile(obj, filename):
    with open("/".join(("worlds", "sm_map_rando", "data", filename + ".json")), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=4)

DumpToJSONFile(item_name_to_id, "item_name_to_id")
DumpToJSONFile(location_name_to_id, "location_name_to_id")
