import logging
from typing import List, Dict, Any

from BaseClasses import Region, Entrance, Location, Item, Tutorial, ItemClassification, RegionType
from worlds.AutoWorld import World, WebWorld


logger = logging.getLogger("DSP")


class DSPWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up DSP randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["lordlou"]
    )]

class DSPWorld(World):
    """
    Build the most efficient intergalactic factory in space simulation strategy 
    game Dyson Sphere Program! Harness the power of stars, collect resources, 
    plan and design production lines and develop your interstellar factory from 
    a small space workshop to a galaxy-wide industrial empire.
    """
    game: str = "Dyson Sphere Program"
    web = DSPWeb()

    data_version = 0
    required_client_version = (0, 3, 4)

    topology_present: bool = False
    remote_items: bool = False  # True if all items come from the server
    remote_start_inventory: bool = False  # True if start inventory comes from the server

    item_name_to_id = {"Electromagnetism": 86000}
    location_name_to_id = {"Electromagnetism": 87000}


    def generate_early(self) -> None:
        pass

    def create_regions(self):
        self.world.regions += [
            self.create_region("Menu", None, ["Start"]),
            self.create_region("Star Cluster", ["Electromagnetism"])
        ]

    def generate_basic(self):
        # Link regions
        self.world.get_entrance("Start", self.player).connect(self.world.get_region("Star Cluster", self.player))

        # Generate item pool
        pool = []
        pool.append(self.create_item("Electromagnetism"))

        self.world.itempool += pool

        self.world.completion_condition[self.player] = lambda state: True #state.has('Victory', self.player)

    def fill_slot_data(self):
        slot_data = {}
        return slot_data

    def create_item(self, name: str) -> Item:
        #item_id: int = self.item_name_to_id[name]

        return DSPItem(name, ItemClassification.progression, 85000, self.player)

    def create_region(self, name: str, locations=None, exits=None):
        ret = Region(name, RegionType.Generic, name, self.player)
        ret.world = self.world
        if locations:
            for location in locations:
                loc_id = self.location_name_to_id.get(location, None)
                location = DSPLocation(self.player, location, loc_id, ret)
                ret.locations.append(location)
        if exits:
            for region_exit in exits:
                ret.exits.append(Entrance(self.player, region_exit, ret))
        return ret

class DSPLocation(Location):
    game: str = "Dyson Sphere Program"


class DSPItem(Item):
    game: str = "Dyson Sphere Program"
