import logging
import os
import Utils
import json
import Patch
import zipfile
import shutil
from typing import List, Dict, Any

from BaseClasses import Region, Entrance, Location, Item, Tutorial, ItemClassification, RegionType
from worlds.AutoWorld import World, WebWorld
from .Technologies import tech_table, recipe_sources, technology_table, advancement_technologies, required_technologies, ap_to_dsp_tech
from .Shapes import get_shapes
from .Options import dsp_options

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

class DSPLocation(Location):
    game: str = "Dyson Sphere Program"

class DSPItem(Item):
    game: str = "Dyson Sphere Program"

class DSPModFile(Patch.APContainer):
    game = "Dyson Sphere Program"
    compression_method = zipfile.ZIP_DEFLATED  # Factorio can't load LZMA archives

    def write_contents(self, opened_zipfile: zipfile.ZipFile):
        # directory containing Factorio mod has to come first, or Factorio won't recognize this file as a mod.
        mod_dir = self.path[:-4]  # cut off .zip
        for root, dirs, files in os.walk(mod_dir):
            for file in files:
                opened_zipfile.write(os.path.join(root, file),
                                     os.path.relpath(os.path.join(root, file),
                                                     os.path.join(mod_dir, '..')))
        # now we can add extras.
        super(DSPModFile, self).write_contents(opened_zipfile)

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

    item_name_to_id = tech_table.copy()
    location_name_to_id = tech_table.copy()

    static_nodes = {"Mission completed!"}

    option_definitions = dsp_options

    def generate_early(self) -> None:
        self.custom_technologies = self.set_custom_technologies()

    def create_regions(self):
        menu = Region("Menu", None, "Menu", self.player)
        start = Entrance(self.player, "Start", menu)
        menu.exits.append(start)
        milkyWay = Region("MilkyWay", None, "MilkyWay", self.player)
        milkyWay.world = menu.world = self.world

        for tech_name, tech_id in tech_table.items():
            tech = DSPLocation(self.player, tech_name, tech_id, milkyWay)
            milkyWay.locations.append(tech)
            tech.game = self.game

        start.connect(milkyWay)
        self.world.regions += [menu, milkyWay]

    def generate_basic(self):
        for tech_name, tech_id in tech_table.items():
            tech_item = DSPItem(tech_name, ItemClassification.progression if tech_name in advancement_technologies else ItemClassification.filler, tech_id, self.player)
            if tech_name in DSPWorld.static_nodes:
                 loc = self.world.get_location(tech_name, self.player)
                 loc.item = tech_item
                 loc.locked = True
                 loc.event = tech_item.advancement
            else:
                self.world.itempool.append(tech_item)

    def set_custom_technologies(self):
        custom_dsp_technologies = {}
        world_dsp_custom = getattr(self.world, "_custom_dsp_technologies", {})
        world_dsp_custom[self.player] = custom_dsp_technologies
        allowed_packs = self.world.max_science_pack[self.player].get_allowed_packs()
        for technology_name, technology in technology_table.items():
            custom_dsp_technologies[technology_name] = technology.get_custom(self.world, allowed_packs, self.player)
        return custom_dsp_technologies

    def fill_slot_data(self):
        slot_data = {}
        return slot_data

    def create_item(self, name: str) -> Item:
        #item_id: int = self.item_name_to_id[name]

        return DSPItem(name, ItemClassification.progression, tech_table[name], self.player)

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

    def set_rules(self):
        shapes = get_shapes(self)
        if self.world.logic[self.player] != 'nologic':
            from worlds.generic import Rules

            for tech_name, technology in self.custom_technologies.items():
                location = self.world.get_location(tech_name, self.player)
                Rules.set_rule(location, technology.build_rule(self.player))
                prequisites = shapes.get(tech_name)
                if prequisites:
                    locations = {self.world.get_location(requisite, self.player) for requisite in prequisites}
                    Rules.add_rule(location, lambda state,
                                                    locations=locations: all(state.can_reach(loc) for loc in locations))

            # get all science pack technologies (but not the ability to craft them)
            self.world.completion_condition[self.player] = lambda state: all(state.has(technology, self.player)
                                                               for technology in advancement_technologies)
            #self.world.completion_condition[self.player] = lambda state: state.has('Mission completed!', self.player)

    def generate_output(self, output_directory: str):
        base_info = {
            "version": Utils.__version__,
            "title": "Archipelago",
            "author": "Lordlou",
            "homepage": "https://archipelago.gg",
            "description": "Integration client for the Archipelago Randomizer",
            "dsp_version": "0.9.26.13026"
        }
        player_names = {x: self.world.get_player_name(x) for x in self.world.player_ids}
        locations = []
        for location in self.world.get_filled_locations(self.player):
            locations.append({"location": location.name, "locationID": technology_table[location.name].dsp_id, "locationDSPTech": ap_to_dsp_tech(technology_table[location.name].ap_id), "item": location.item.name, "playerId": location.item.player})
        mod_name = f"AP-{self.world.seed_name}-P{self.player}-{self.world.get_player_name(self.player)}"

        data = {"locations": locations, 
                "player_names" : player_names, 
                "tech_table": tech_table,
                "mod_name": mod_name, "allowed_science_packs": list(self.world.max_science_pack[self.player].get_allowed_packs()),
                #"tech_cost_scale": tech_cost, "custom_data": world.custom_data[player],
                "tech_tree_layout_prerequisites": {ap_to_dsp_tech(technology_table[key].ap_id): [ap_to_dsp_tech(technology_table[v].ap_id) for v in value] for key, value in self.world.tech_tree_layout_prerequisites[self.player].items()},
                #"rocket_recipe" : rocket_recipes[world.max_science_pack[player].value],
                "slot_name": self.world.get_player_name(self.player),
                #"starting_items": self.world.starting_items[self.player]
                }
        for dsp_option in Options.dsp_options:
            data[dsp_option] = getattr(self.world, dsp_option)[self.player].value

        mod_dir = os.path.join(output_directory, mod_name+"_"+Utils.__version__)
        os.makedirs(mod_dir, exist_ok=True)
        with open(os.path.join(mod_dir, "data.json"), "wt") as f:
            json.dump(data, f, indent=4)
        
        info = base_info.copy()
        info["name"] = mod_name
        with open(os.path.join(mod_dir, "info.json"), "wt") as f:
            json.dump(info, f, indent=4)

        zf_path = os.path.join(mod_dir + ".zip")
        mod = DSPModFile(zf_path, player=self.player, player_name=self.world.get_player_name(self.player))
        mod.write()

        shutil.rmtree(mod_dir)
