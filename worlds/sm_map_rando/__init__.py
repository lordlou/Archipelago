from __future__ import annotations

import logging
import copy
import os
import shutil
import threading
import base64
from typing import Any, Dict, Iterable, List, Set, TextIO, TypedDict

from BaseClasses import Region, Entrance, Location, MultiWorld, Item, ItemClassification, CollectionState, Tutorial
from Fill import fill_restrictive
from worlds.AutoWorld import World, AutoLogicRegister, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule

logger = logging.getLogger("Super Metroid")

from .Options import smmr_options
from .Rom import get_base_rom_path, SM_ROM_MAX_PLAYERID, SM_ROM_PLAYERDATA_COUNT, SMMapRandoDeltaPatch

from map_randomizer import create_gamedata, APRandomizer, APCollectionState

class SMMRCollectionState(metaclass=AutoLogicRegister):
    def init_mixin(self, parent: MultiWorld):
        
        # for unit tests where MultiWorld is instantiated before worlds
        if hasattr(parent, "state"):
            self.smmrcs = {player: copy.deepcopy(parent.state.smmrcs[player]) for player in parent.get_game_players(SMMapRandoWorld.game)}
            for player, group in parent.groups.items():
                if (group["game"] == SMMapRandoWorld.game):
                    self.smmrcs[player] = APCollectionState(None)
                    if player not in parent.state.smmrcs:
                        parent.state.smmrcs[player] = APCollectionState(None)
        else:
            self.smmrcs = {}

    def copy_mixin(self, ret) -> CollectionState:
        ret.smmrcs = {player: copy.deepcopy(self.smmrcs[player]) for player in self.smmrcs}
        return ret

class SMMapRandoWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Super Metroid Map Rando Client on your computer. This guide covers single-player, multiworld, and related software.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Farrak Kilhn"]
    )]


locations_start_id = 86000
items_start_id = 87000

class SMMapRandoWorld(World):
    """

    """

    game: str = "Super Metroid Map Rando"
    topology_present = True
    data_version = 0
    option_definitions = smmr_options

    gamedata = create_gamedata()

    item_name_to_id = {item_name: items_start_id + idx for idx, item_name in enumerate(gamedata.item_isv)}
    location_name_to_id = {loc_name: locations_start_id + idx for idx, loc_name in enumerate(gamedata.get_location_names())}

    web = SMMapRandoWeb()

    required_client_version = (0, 2, 6)

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.rom_name_available_event = threading.Event()
        self.locations = {}
        self.map_rando = APRandomizer(12345)
        

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def generate_early(self):
        self.multiworld.state.smmrcs[self.player] = APCollectionState(self.map_rando)

    def create_items(self):
        pool = []
        for idx, type_count in enumerate(self.map_rando.randomizer.initial_items_remaining):
            for item_count in range(type_count):
                mr_item = SMMRItem(SMMapRandoWorld.item_id_to_name[items_start_id + idx], 
                            ItemClassification.progression if idx == 0 else ItemClassification.filler, 
                            items_start_id + idx, 
                            player=self.player)
                pool.append(mr_item)
        self.multiworld.itempool += pool

    def create_region(self, world: MultiWorld, player: int, name: str, locations=None, exits=None):
        ret = Region(name, player, world)
        if locations:
            for loc in locations:
                location = self.locations[loc]
                location.parent_region = ret
                ret.locations.append(location)
        if exits:
            for exit in exits:
                ret.exits.append(Entrance(player, exit, ret))
        return ret

    def create_regions(self):
        # create locations
        for loc_name, loc_id in SMMapRandoWorld.location_name_to_id.items():
            self.locations[loc_name] = SMMRLocation(self.player, loc_name, loc_id)
        
        # create regions
        regions = []
        for (vertex_name, location_name) in self.map_rando.randomizer.game_data.get_vertex_names():
            regions.append(self.create_region(  self.multiworld, 
                                                self.player, 
                                                vertex_name,
                                                [location_name] if location_name != None else None))

        self.multiworld.regions += regions

        #create entrances
        for (link_from, link_to), link_map in self.map_rando.get_links_infos().items():
            src_region = regions[link_from]
            dest_region = regions[link_to]
            srcDestEntrance = SMMREntrance(self.player, src_region.name + "->" + dest_region.name, src_region, link_map)
            src_region.exits.append(srcDestEntrance)
            srcDestEntrance.connect(dest_region)
            add_rule(srcDestEntrance, lambda state: state.smmrcs[self.player].can_traverse(link_from, srcDestEntrance.strats_links))

        self.multiworld.regions += [self.create_region(self.multiworld, self.player, 'Menu', None, ['StartAP'])]

        startAP = self.multiworld.get_entrance('StartAP', self.player)
        startAP.connect(self.multiworld.get_region("Ship", self.player))    
        
    def set_rules(self):
        self.multiworld.completion_condition[self.player] =\
        lambda state: True
    

    def collect(self, state: CollectionState, item: Item) -> bool:
        pass

    def remove(self, state: CollectionState, item: Item) -> bool:
        pass

    def create_item(self, name: str) -> Item:
        pass

    def get_filler_item_name(self) -> str:
        pass
        
    def generate_output(self, output_directory: str):
        outfilebase = self.multiworld.get_out_file_name_base(self.player)
        outputFilename = os.path.join(output_directory, f"{outfilebase}.sfc")

        shutil.copyfile(get_base_rom_path(), outputFilename)

        try:
            self.write_crc(outputFilename)
            # set rom name
            # 21 bytes
            from Main import __version__
            self.romName = bytearray(f'SMMR{__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}', 'utf8')[:21]
            self.romName.extend([0] * (21 - len(self.romName)))
            self.rom_name = self.romName
        except:
            raise
        else:
            patch = SMMapRandoDeltaPatch(os.path.splitext(outputFilename)[0] + SMMapRandoDeltaPatch.patch_file_ending, player=self.player,
                                            player_name=self.multiworld.player_name[self.player], patched_path=outputFilename)
            patch.write()
        finally:
            if os.path.exists(outputFilename):
                os.unlink(outputFilename)
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def checksum_mirror_sum(self, start, length, mask = 0x800000):
        while not(length & mask) and mask:
            mask >>= 1

        part1 = sum(start[:mask]) & 0xFFFF
        part2 = 0

        next_length = length - mask
        if next_length:
            part2 = self.checksum_mirror_sum(start[mask:], next_length, mask >> 1)

            while (next_length < mask):
                next_length += next_length
                part2 += part2

        return (part1 + part2) & 0xFFFF

    def write_bytes(self, buffer, startaddress: int, values):
        buffer[startaddress:startaddress + len(values)] = values

    def write_crc(self, romName):
        with open(romName, 'rb') as stream:
            buffer = bytearray(stream.read())
            crc = self.checksum_mirror_sum(buffer, len(buffer))
            inv = crc ^ 0xFFFF
            self.write_bytes(buffer, 0x7FDC, [inv & 0xFF, (inv >> 8) & 0xFF, crc & 0xFF, (crc >> 8) & 0xFF])
        with open(romName, 'wb') as outfile:
            outfile.write(buffer)

    def modify_multidata(self, multidata: dict):
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def fill_slot_data(self): 
        slot_data = {}      
        return slot_data
    
    
class SMMRLocation(Location):
    game: str = SMMapRandoWorld.game

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(SMMRLocation, self).__init__(player, name, address, parent)

class SMMRItem(Item):
    game: str = SMMapRandoWorld.game

    def __init__(self, name, classification, code, player: int):
        super(SMMRItem, self).__init__(name, classification, code, player)

class SMMREntrance(Entrance):
    game: str = SMMapRandoWorld.game

    def __init__(self, player: int, name: str = '', parent: Region = None, strats_links: Dict[str, List[int]] = None):
        super(SMMREntrance, self).__init__(player, name, parent)
        self.strats_links = strats_links