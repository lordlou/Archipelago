﻿from enum import Enum
from logging import exception
from typing import Any, Callable, List, Sequence
import random
import typing
from BaseClasses import Location
from worlds.smz3.TotalSMZ3.Item import ItemType
from worlds.smz3.TotalSMZ3.Location import LocationType
from worlds.smz3.TotalSMZ3.Region import IMedallionAccess, IReward, RewardType, SMRegion, Z3Region
from worlds.smz3.TotalSMZ3.Regions.Zelda.EasternPalace import EasternPalace
from worlds.smz3.TotalSMZ3.Regions.Zelda.DesertPalace import DesertPalace
from worlds.smz3.TotalSMZ3.Regions.Zelda.TowerOfHera import TowerOfHera
from worlds.smz3.TotalSMZ3.Regions.Zelda.PalaceOfDarkness import PalaceOfDarkness
from worlds.smz3.TotalSMZ3.Regions.Zelda.SwampPalace import SwampPalace
from worlds.smz3.TotalSMZ3.Regions.Zelda.SkullWoods import SkullWoods
from worlds.smz3.TotalSMZ3.Regions.Zelda.ThievesTown import ThievesTown
from worlds.smz3.TotalSMZ3.Regions.Zelda.IcePalace import IcePalace
from worlds.smz3.TotalSMZ3.Regions.Zelda.MiseryMire import MiseryMire
from worlds.smz3.TotalSMZ3.Regions.Zelda.TurtleRock import TurtleRock
from worlds.smz3.TotalSMZ3.Regions.Zelda.GanonsTower import GanonsTower

from worlds.smz3.TotalSMZ3.World import World
from worlds.smz3.TotalSMZ3.Config import Config, GameMode

class KeycardPlaque:
    Level1 = 0xe0
    Level2 = 0xe1
    Boss = 0xe2
    Null = 0x00  

class KeycardDoors:
    Left = 0xd414
    Right = 0xd41a
    Up = 0xd420
    Down = 0xd426
    BossLeft = 0xc842
    BossRight = 0xc848


class KeycardEvents:
    CrateriaLevel1 = 0x0000
    CrateriaLevel2 = 0x0100
    CrateriaBoss = 0x0200
    BrinstarLevel1 = 0x0300
    BrinstarLevel2 = 0x0400
    BrinstarBoss = 0x0500
    NorfairLevel1 = 0x0600
    NorfairLevel2 = 0x0700
    NorfairBoss = 0x0800
    MaridiaLevel1 = 0x0900
    MaridiaLevel2 = 0x0a00
    MaridiaBoss = 0x0b00
    WreckedShipLevel1 = 0x0c00
    WreckedShipBoss = 0x0d00
    LowerNorfairLevel1 = 0x0e00
    LowerNorfairBoss = 0x0f00

class DropPrize(Enum):
    Heart = 0xD8
    Green = 0xD9
    Blue = 0xDA
    Red = 0xDB
    Bomb1 = 0xDC
    Bomb4 = 0xDD
    Bomb8 = 0xDE
    Magic = 0xDF
    FullMagic = 0xE0
    Arrow5 = 0xE1
    Arrow10 = 0xE2
    Fairy = 0xE3

class Patch:
    allWorlds: List[World]
    myWorld: World
    seedGuid: str
    seed: int
    rnd: random.Random
    #stringTable: StringTable
    patches: Sequence[Any]

    def __init__(self, myWorld: World, allWorlds: List[World], seedGuid: str, seed: int, rnd: random.Random):
        self.myWorld = myWorld
        self.allWorlds = allWorlds
        self.seedGuid = seedGuid
        self.seed = seed
        self.rnd = rnd

    def Create(self, config: Config):
        #stringTable = new StringTable();
        self.patches = []

        self.WriteMedallions()
        self.WriteRewards()
        #WriteDungeonMusic(config.Keysanity);

        #WriteDiggingGameRng();

        #WritePrizeShuffle();

        #WriteRemoveEquipmentFromUncle(myWorld.GetLocation("Link's Uncle").Item);

        #WriteGanonInvicible(config.GanonInvincible);
        #WriteRngBlock();

        #WriteSaveAndQuitFromBossRoom();
        #WriteWorldOnAgahnimDeath();

        #WriteTexts(config);

        self.WriteSMLocations([loc for region in self.myWorld.Regions for loc in region.Locations if isinstance(region, SMRegion)])
        self.WriteZ3Locations([loc for region in self.myWorld.Regions for loc in region.Locations if isinstance(region, Z3Region)])

        #WriteStringTable();

        #WriteSMKeyCardDoors();
        #WriteZ3KeysanityFlags();

        #WritePlayerNames();
        #WriteSeedData();
        #WriteGameTitle();
        #WriteCommonFlags();

        return {patch[0]:patch[1] for patch in self.patches}
    
    def WriteMedallions(self):
        turtleRock = next(region for region in self.myWorld.Regions if isinstance(region, TurtleRock))
        miseryMire = next(region for region in self.myWorld.Regions if isinstance(region, MiseryMire))

        turtleRockAddresses = [0x308023, 0xD020, 0xD0FF, 0xD1DE ]
        miseryMireAddresses = [ 0x308022, 0xCFF2, 0xD0D1, 0xD1B0 ]

        if turtleRock.Medallion == ItemType.Bombos:
            turtleRockValues = [0x00, 0x51, 0x10, 0x00]
        elif turtleRock.Medallion == ItemType.Ether:
            turtleRockValues = [0x01, 0x51, 0x18, 0x00]
        elif turtleRock.Medallion == ItemType.Quake:
            turtleRockValues = [0x02, 0x14, 0xEF, 0xC4]
        else:
            raise exception(f"Tried using {turtleRock.Medallion} in place of Turtle Rock medallion")

        if miseryMire.Medallion == ItemType.Bombos:
            miseryMireValues = [0x00, 0x51, 0x00, 0x00]
        elif miseryMire.Medallion == ItemType.Ether:
            miseryMireValues = [0x01, 0x13, 0x9F, 0xF1]
        elif miseryMire.Medallion == ItemType.Quake:
            miseryMireValues = [0x02, 0x51, 0x08, 0x00]
        else:
            raise exception(f"Tried using {miseryMire.Medallion} in place of Misery Mire medallion")

        self.patches += [(Snes(addr), [value]) for addr, value in zip(turtleRockAddresses, turtleRockValues)]
        self.patches += [(Snes(addr), [value]) for addr, value in zip(miseryMireAddresses, miseryMireValues)]

    def WriteRewards(self):
        crystalsBlue = [ 1, 2, 3, 4, 7 ]
        self.rnd.shuffle(crystalsBlue)
        crystalsRed = [ 5, 6 ]
        self.rnd.shuffle(crystalsRed)
        crystalRewards = crystalsBlue + crystalsRed

        pendantsGreen = [ 1 ]
        pendantsBlueRed = [ 2, 3 ]
        self.rnd.shuffle(pendantsBlueRed)
        pendantRewards = pendantsGreen + pendantsBlueRed

        regions = [region for region in self.myWorld.Regions if isinstance(region, IReward)]
        crystalRegions = [region for region in regions if region.Reward == RewardType.CrystalBlue] +  [region for region in regions if region.Reward == RewardType.CrystalRed]
        pendantRegions = [region for region in regions if region.Reward == RewardType.PendantGreen] +  [region for region in regions if region.Reward == RewardType.PendantNonGreen]

        self.patches += self.RewardPatches(crystalRegions, crystalRewards, self.CrystalValues)
        self.patches += self.RewardPatches(pendantRegions, pendantRewards, self.PendantValues)

    def RewardPatches(self, regions: List[IReward], rewards: List[int], rewardValues: Callable):
        addresses = [self.RewardAddresses(region) for region in regions]
        values = [rewardValues(reward) for reward in rewards]
        associations = zip(addresses, values)
        return [(Snes(i), [b]) for association in associations for i,b in zip(association[0], association[1])]

    def RewardAddresses(self, region: IReward):
        regionType = {
                    EasternPalace : [ 0x2A09D, 0xABEF8, 0xABEF9, 0x308052, 0x30807C, 0x1C6FE ],
                    DesertPalace : [ 0x2A09E, 0xABF1C, 0xABF1D, 0x308053, 0x308078, 0x1C6FF ],
                    TowerOfHera : [ 0x2A0A5, 0xABF0A, 0xABF0B, 0x30805A, 0x30807A, 0x1C706 ],
                    PalaceOfDarkness : [ 0x2A0A1, 0xABF00, 0xABF01, 0x308056, 0x30807D, 0x1C702 ],
                    SwampPalace : [ 0x2A0A0, 0xABF6C, 0xABF6D, 0x308055, 0x308071, 0x1C701 ],
                    SkullWoods : [ 0x2A0A3, 0xABF12, 0xABF13, 0x308058, 0x30807B, 0x1C704 ],
                    ThievesTown : [ 0x2A0A6, 0xABF36, 0xABF37, 0x30805B, 0x308077, 0x1C707 ],
                    IcePalace : [ 0x2A0A4, 0xABF5A, 0xABF5B, 0x308059, 0x308073, 0x1C705 ],
                    MiseryMire : [ 0x2A0A2, 0xABF48, 0xABF49, 0x308057, 0x308075, 0x1C703 ],
                    TurtleRock : [ 0x2A0A7, 0xABF24, 0xABF25, 0x30805C, 0x308079, 0x1C708 ]
                    }
        result = regionType.get(type(region), None)
        if result is None:
            raise exception(f"Region {result} should not be a dungeon reward region")
        else:
            return result

    def CrystalValues(self, crystal: int):
        crystalMap = {
                1 : [ 0x02, 0x34, 0x64, 0x40, 0x7F, 0x06 ],
                2 : [ 0x10, 0x34, 0x64, 0x40, 0x79, 0x06 ],
                3 : [ 0x40, 0x34, 0x64, 0x40, 0x6C, 0x06 ],
                4 : [ 0x20, 0x34, 0x64, 0x40, 0x6D, 0x06 ],
                5 : [ 0x04, 0x32, 0x64, 0x40, 0x6E, 0x06 ],
                6 : [ 0x01, 0x32, 0x64, 0x40, 0x6F, 0x06 ],
                7 : [ 0x08, 0x34, 0x64, 0x40, 0x7C, 0x06 ],
                }
        result = crystalMap.get(crystal, None)
        if result is None:
            raise exception(f"Tried using {result} as a crystal number")
        else:
            return result

    def PendantValues(self, pendant: int):
        pendantMap = {
                    1 : [ 0x04, 0x38, 0x62, 0x00, 0x69, 0x01 ],
                    2 : [ 0x01, 0x32, 0x60, 0x00, 0x69, 0x03 ],
                    3 : [ 0x02, 0x34, 0x60, 0x00, 0x69, 0x02 ],
                    }
        result = pendantMap.get(pendant, None)
        if result is None:
            raise exception(f"Tried using {result} as a pendant number")
        else:
            return result
    
    def WriteSMLocations(self, locations: List[Location]):
        def GetSMItemPLM(location:Location):
            itemMap = {
                    ItemType.ETank : 0xEED7,
                    ItemType.Missile : 0xEEDB,
                    ItemType.Super : 0xEEDF,
                    ItemType.PowerBomb : 0xEEE3,
                    ItemType.Bombs : 0xEEE7,
                    ItemType.Charge : 0xEEEB,
                    ItemType.Ice : 0xEEEF,
                    ItemType.HiJump : 0xEEF3,
                    ItemType.SpeedBooster : 0xEEF7,
                    ItemType.Wave : 0xEEFB,
                    ItemType.Spazer : 0xEEFF,
                    ItemType.SpringBall : 0xEF03,
                    ItemType.Varia : 0xEF07,
                    ItemType.Plasma : 0xEF13,
                    ItemType.Grapple : 0xEF17,
                    ItemType.Morph : 0xEF23,
                    ItemType.ReserveTank : 0xEF27,
                    ItemType.Gravity : 0xEF0B,
                    ItemType.XRay : 0xEF0F,
                    ItemType.SpaceJump : 0xEF1B,
                    ItemType.ScrewAttack : 0xEF1F
                    }
            plmId = 0xEFE0 if self.myWorld.Config.GameMode == GameMode.Multiworld else \
                                itemMap.get(location.APLocation.item.item.Type, 0xEFE0)
            if (plmId == 0xEFE0):
                plmId += 4 if location.Type == LocationType.Chozo else 8 if location.Type == LocationType.Hidden else 0
            else:
                plmId += 0x54 if location.Type == LocationType.Chozo else 0xA8 if location.Type == LocationType.Hidden else 0
            return plmId

        for location in locations:
            if (self.myWorld.Config.GameMode == GameMode.Multiworld):
                self.patches.append((Snes(location.Address), getWordArray(GetSMItemPLM(location))))
                self.patches.append(self.ItemTablePatch(location, self.GetZ3ItemId(location)))
            else:
                plmId = GetSMItemPLM(location)
                self.patches.append((Snes(location.Address), getWordArray(plmId)))
                if (plmId >= 0xEFE0):
                    self.patches.append((Snes(location.Address + 5), [self.GetZ3ItemId(location)]))

    def WriteZ3Locations(self, locations: List[Location]):
        for location in locations:
            if (location.Type == LocationType.HeraStandingKey):
                self.patches.append((Snes(0x9E3BB), [0xE4] if location.APLocation.item.item.Type == ItemType.KeyTH else [0xEB]))
            elif (location.Type in [LocationType.Pedestal, LocationType.Ether, LocationType.Bombos]):
                pass
                #text = Texts.ItemTextbox(location.Item);
                #dialog = Dialog.Simple(text);
                #if (location.Type == LocationType.Pedestal) {
                #    stringTable.SetPedestalText(text);
                #    patches.Add((Snes(0x308300), dialog));
                #}
                #else if (location.Type == LocationType.Ether) {
                #    stringTable.SetEtherText(text);
                #    patches.Add((Snes(0x308F00), dialog));
                #}
                #else if (location.Type == LocationType.Bombos) {
                #    stringTable.SetBombosText(text);
                #    patches.Add((Snes(0x309000), dialog));
                #}

            if (self.myWorld.Config.GameMode == GameMode.Multiworld):
                self.patches.append((Snes(location.Address), [(location.Id - 256)]))
                self.patches.append(self.ItemTablePatch(location, self.GetZ3ItemId(location)))
            else:
                self.patches.append((Snes(location.Address), [self.GetZ3ItemId(location)]))

    def GetZ3ItemId(self, location: Location):
        item = location.APLocation.item.item
        itemDungeon = None
        if item.IsKey:
            itemDungeon = ItemType.Key if (not item.World.Config.Keysanity or item.Type != ItemType.KeyHC) else ItemType.KeyHC
        elif item.IsBigKey: 
            itemDungeon = ItemType.BigKey
        elif item.IsMap:
            itemDungeon = ItemType.Map if (not item.World.Config.Keysanity or item.Type != ItemType.MapHC) else ItemType.MapHC
        elif item.IsCompass:
            itemDungeon = ItemType.Compass

        value = item.Type if location.Type == LocationType.NotInDungeon or \
            not (item.IsDungeonItem and location.Region.IsRegionItem(item) and item.World == self.myWorld) else itemDungeon
            
        return value.value

    def ItemTablePatch(self, location: Location, itemId: int):
        itemtype = 0 if location.Item.World == location.Region.World else 1
        owner = location.Item.World.Id
        return (0x386000 + (location.Id * 8), [itemtype, itemId, owner, 0])
"""
    void WriteDungeonMusic(bool keysanity) {
        if (!keysanity) {
            var regions = myWorld.Regions.OfType<IReward>();
            IEnumerable<byte> music;
            var pendantRegions = regions.Where(x => new[] { PendantGreen, PendantNonGreen }.Contains(x.Reward));
            var crystalRegions = regions.Where(x => new[] { CrystalBlue, CrystalRed }.Contains(x.Reward));
            regions = pendantRegions.Concat(crystalRegions);
            music = new byte[] {
                0x11, 0x11, 0x11, 0x16, 0x16,
                0x16, 0x16, 0x16, 0x16, 0x16,
            };
            patches.AddRange(MusicPatches(regions, music));
        }
    }

    IEnumerable<byte> RandomDungeonMusic() {
        while (true) yield return rnd.Next(2) == 0 ? (byte)0x11 : (byte)0x16;
    }

    IEnumerable<(int, byte[])> MusicPatches(IEnumerable<IReward> regions, IEnumerable<byte> music) {
        var addresses = regions.Select(MusicAddresses);
        var associations = addresses.Zip(music, (a, b) => (a, b));
        return associations.SelectMany(x => x.a.Select(i => (Snes(i), new byte[] { x.b })));
    }

    int[] MusicAddresses(IReward region) {
        return region switch {
            EasternPalace _ => new[] { 0x2D59A },
            DesertPalace _ => new[] { 0x2D59B, 0x2D59C, 0x2D59D, 0x2D59E },
            TowerOfHera _ => new[] { 0x2D5C5, 0x2907A, 0x28B8C },
            PalaceOfDarkness _ => new[] { 0x2D5B8 },
            SwampPalace _ => new[] { 0x2D5B7 },
            SkullWoods _ => new[] { 0x2D5BA, 0x2D5BB, 0x2D5BC, 0x2D5BD, 0x2D608, 0x2D609, 0x2D60A, 0x2D60B },
            ThievesTown _ => new[] { 0x2D5C6 },
            IcePalace _ => new[] { 0x2D5BF },
            MiseryMire _ => new[] { 0x2D5B9 },
            TurtleRock _ => new[] { 0x2D5C7, 0x2D5A7, 0x2D5AA, 0x2D5AB },
            var x => throw new InvalidOperationException($"Region {x} should not be a dungeon music region"),
        };
    }

    void WritePrizeShuffle() {
        const int prizePackItems = 56;
        const int treePullItems = 3;

        IEnumerable<byte> bytes;
        byte drop, final;

        var pool = new DropPrize[] {
            Heart, Heart, Heart, Heart, Green, Heart, Heart, Green,         // pack 1
            Blue, Green, Blue, Red, Blue, Green, Blue, Blue,                // pack 2
            FullMagic, Magic, Magic, Blue, FullMagic, Magic, Heart, Magic,  // pack 3
            Bomb1, Bomb1, Bomb1, Bomb4, Bomb1, Bomb1, Bomb8, Bomb1,         // pack 4
            Arrow5, Heart, Arrow5, Arrow10, Arrow5, Heart, Arrow5, Arrow10, // pack 5
            Magic, Green, Heart, Arrow5, Magic, Bomb1, Green, Heart,        // pack 6
            Heart, Fairy, FullMagic, Red, Bomb8, Heart, Red, Arrow10,       // pack 7
            Green, Blue, Red, // from pull trees
            Green, Red, // from prize crab
            Green, // stunned prize
            Red, // saved fish prize
        }.AsEnumerable();

        var prizes = pool.Shuffle(rnd).Cast<byte>();

        /* prize pack drop order */
        (bytes, prizes) = prizes.SplitOff(prizePackItems);
        patches.Add((Snes(0x6FA78), bytes.ToArray()));

        /* tree pull prizes */
        (bytes, prizes) = prizes.SplitOff(treePullItems);
        patches.Add((Snes(0x1DFBD4), bytes.ToArray()));

        /* crab prizes */
        (drop, final, prizes) = prizes;
        patches.Add((Snes(0x6A9C8), new[] { drop }));
        patches.Add((Snes(0x6A9C4), new[] { final }));

        /* stun prize */
        (drop, prizes) = prizes;
        patches.Add((Snes(0x6F993), new[] { drop }));

        /* fish prize */
        (drop, _) = prizes;
        patches.Add((Snes(0x1D82CC), new[] { drop }));

        patches.AddRange(EnemyPrizePackDistribution());

        /* Pack drop chance */
        /* Normal difficulty is 50%. 0 => 100%, 1 => 50%, 3 => 25% */
        const int nrPacks = 7;
        const byte probability = 1;
        patches.Add((Snes(0x6FA62), Repeat(probability, nrPacks).ToArray()));
    }

    IEnumerable<(int, byte[])> EnemyPrizePackDistribution() {
        var (prizePacks, duplicatePacks) = EnemyPrizePacks();

        var n = prizePacks.Sum(x => x.bytes.Length);
        var randomization = PrizePackRandomization(n, 1);

        var patches = prizePacks.Select(x => {
            IEnumerable<byte> packs;
            (packs, randomization) = randomization.SplitOff(x.bytes.Length);
            return (x.offset, bytes: x.bytes.Zip(packs, (b, p) => (byte)(b | p)).ToArray());
        }).ToList();

        var duplicates =
            from d in duplicatePacks
            from p in patches
            where p.offset == d.src
            select (d.dest, p.bytes);
        patches.AddRange(duplicates.ToList());

        return patches.Select(x => (Snes(x.offset), x.bytes));
    }

    /* Guarantees at least s of each prize pack, over a total of n packs.
        * In each iteration, from the product n * m, use the guaranteed number
        * at k, where k is the "row" (integer division by m), when k falls
        * within the list boundary. Otherwise use the "column" (modulo by m)
        * as the random element.
        */
    IEnumerable<byte> PrizePackRandomization(int n, int s) {
        const int m = 7;
        var g = Repeat(Range(0, m), s).SelectMany(x => x).ToList();

        IEnumerable<int> randomization(int n) {
            n = m * n;
            while (n > 0) {
                var r = rnd.Next(n);
                var k = r / m;
                yield return k < g.Count ? g[k] : r % m;
                if (k < g.Count) g.RemoveAt(k);
                n -= m;
            }
        }

        return randomization(n).Select(x => (byte)(x + 1)).ToList();
    }

    /* Todo: Deadrock turns into $8F Blob when powdered, but those "onion blobs" always drop prize pack 1. */
    (IList<(int offset, byte[] bytes)>, IList<(int src, int dest)>) EnemyPrizePacks() {
        const int offset = 0xDB632;
        var patches = new[] {
            /* sprite_prep */
            (0x6888D, new byte[] { 0x00 }), // Keese DW
            (0x688A8, new byte[] { 0x00 }), // Rope
            (0x68967, new byte[] { 0x00, 0x00 }), // Crow/Dacto
            (0x69125, new byte[] { 0x00, 0x00 }), // Red/Blue Hardhat Bettle
            /* sprite properties */
            (offset+0x01, new byte[] { 0x90 }), // Vulture
            (offset+0x08, new byte[] { 0x00 }), // Octorok (One Way)
            (offset+0x0A, new byte[] { 0x00 }), // Octorok (Four Way)
            (offset+0x0D, new byte[] { 0x80, 0x90 }), // Buzzblob, Snapdragon
            (offset+0x11, new byte[] { 0x90, 0x90, 0x00 }), // Hinox, Moblin, Mini Helmasaur
            (offset+0x18, new byte[] { 0x90, 0x90 }), // Mini Moldorm, Poe/Hyu
            (offset+0x20, new byte[] { 0x00 }), // Sluggula
            (offset+0x22, new byte[] { 0x80, 0x00, 0x00 }), // Ropa, Red Bari, Blue Bari
            // Blue Soldier/Tarus, Green Soldier, Red Spear Soldier
            // Blue Assault Soldier, Red Assault Spear Soldier/Tarus
            // Blue Archer, Green Archer
            // Red Javelin Soldier, Red Bush Javelin Soldier
            // Red Bomb Soldiers, Green Soldier Recruits,
            // Geldman, Toppo
            (offset+0x41, new byte[] { 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x10, 0x90, 0x90, 0x80 }),
            (offset+0x4F, new byte[] { 0x80 }), // Popo 2
            (offset+0x51, new byte[] { 0x80 }), // Armos
            (offset+0x55, new byte[] { 0x00, 0x00 }), // Ku, Zora
            (offset+0x58, new byte[] { 0x90 }), // Crab
            (offset+0x64, new byte[] { 0x80 }), // Devalant (Shooter)
            (offset+0x6A, new byte[] { 0x90, 0x90 }), // Ball N' Chain Trooper, Cannon Soldier
            (offset+0x6D, new byte[] { 0x80, 0x80 }), // Rat/Buzz, (Stal)Rope
            (offset+0x71, new byte[] { 0x80 }), // Leever
            (offset+0x7C, new byte[] { 0x90 }), // Initially Floating Stal
            (offset+0x81, new byte[] { 0xC0 }), // Hover
            // Green Eyegore/Mimic, Red Eyegore/Mimic
            // Detached Stalfos Body, Kodongo
            (offset+0x83, new byte[] { 0x10, 0x10, 0x10, 0x00 }),
            (offset+0x8B, new byte[] { 0x10 }), // Gibdo
            (offset+0x8E, new byte[] { 0x00, 0x00 }), // Terrorpin, Blob
            (offset+0x91, new byte[] { 0x10 }), // Stalfos Knight
            (offset+0x99, new byte[] { 0x10 }), // Pengator
            (offset+0x9B, new byte[] { 0x10 }), // Wizzrobe
            // Blue Zazak, Red Zazak, Stalfos
            // Green Zirro, Blue Zirro, Pikit
            (offset+0xA5, new byte[] { 0x10, 0x10, 0x10, 0x80, 0x80, 0x80 }),
            (offset+0xC7, new byte[] { 0x10 }), // Hokku-Bokku
            (offset+0xC9, new byte[] { 0x10 }), // Tektite
            (offset+0xD0, new byte[] { 0x10 }), // Lynel
            (offset+0xD3, new byte[] { 0x00 }), // Stal
        };
        var duplicates = new[] {
            /* Popo2 -> Popo. Popo is not used in vanilla Z3, but we duplicate from Popo2 just to be sure */
            (offset + 0x4F, offset + 0x4E),
        };
        return (patches, duplicates);
    }

    void WriteTexts(Config config) {
        var regions = myWorld.Regions.OfType<IReward>();
        var greenPendantDungeon = regions.Where(x => x.Reward == PendantGreen).Cast<Region>().First();
        var redCrystalDungeons = regions.Where(x => x.Reward == CrystalRed).Cast<Region>();

        var sahasrahla = Texts.SahasrahlaReveal(greenPendantDungeon);
        patches.Add((Snes(0x308A00), Dialog.Simple(sahasrahla)));
        stringTable.SetSahasrahlaRevealText(sahasrahla);

        var bombShop = Texts.BombShopReveal(redCrystalDungeons);
        patches.Add((Snes(0x308E00), Dialog.Simple(bombShop)));
        stringTable.SetBombShopRevealText(bombShop);

        var blind = Texts.Blind(rnd);
        patches.Add((Snes(0x308800), Dialog.Simple(blind)));
        stringTable.SetBlindText(blind);

        var tavernMan = Texts.TavernMan(rnd);
        patches.Add((Snes(0x308C00), Dialog.Simple(tavernMan)));
        stringTable.SetTavernManText(tavernMan);

        var ganon = Texts.GanonFirstPhase(rnd);
        patches.Add((Snes(0x308600), Dialog.Simple(ganon)));
        stringTable.SetGanonFirstPhaseText(ganon);

        // Todo: Verify these two are correct if ganon invincible patch is ever added
        // ganon_fall_in_alt in v30
        var ganonFirstPhaseInvincible = "You think you\nare ready to\nface me?\n\nI will not die\n\nunless you\ncomplete your\ngoals. Dingus!";
        patches.Add((Snes(0x309100), Dialog.Simple(ganonFirstPhaseInvincible)));

        // ganon_phase_3_alt in v30
        var ganonThirdPhaseInvincible = "Got wax in\nyour ears?\nI cannot die!";
        patches.Add((Snes(0x309200), Dialog.Simple(ganonThirdPhaseInvincible)));
        // ---

        var silversLocation = allWorlds.SelectMany(world => world.Locations).Where(l => l.ItemIs(SilverArrows, myWorld)).First();
        var silvers = config.GameMode == GameMode.Multiworld ?
            Texts.GanonThirdPhaseMulti(silversLocation.Region, myWorld) :
            Texts.GanonThirdPhaseSingle(silversLocation.Region);
        patches.Add((Snes(0x308700), Dialog.Simple(silvers)));
        stringTable.SetGanonThirdPhaseText(silvers);

        var triforceRoom = Texts.TriforceRoom(rnd);
        patches.Add((Snes(0x308400), Dialog.Simple(triforceRoom)));
        stringTable.SetTriforceRoomText(triforceRoom);
    }

    void WriteStringTable() {
        // Todo: v12, base table in asm, use move instructions in seed patch
        patches.Add((Snes(0x1C8000), stringTable.GetPaddedBytes()));
    }

    void WritePlayerNames() {
        patches.AddRange(allWorlds.Select(world => (0x385000 + (world.Id * 16), PlayerNameBytes(world.Player))));
    }

    byte[] PlayerNameBytes(string name) {
        name = name.Length > 12 ? name[..12].TrimEnd() : name;

        const int width = 12;
        var pad = (width - name.Length) / 2;
        name = name.PadLeft(name.Length + pad);
        name = name.PadRight(width);

        return AsAscii(name).Concat(UintBytes(0)).ToArray();
    }

    void WriteSeedData() {
        var configField =
            ((myWorld.Config.Race ? 1 : 0) << 15) |
            ((myWorld.Config.Keysanity ? 1 : 0) << 13) |
            ((myWorld.Config.GameMode == GameMode.Multiworld ? 1 : 0) << 12) |
            ((int)myWorld.Config.Z3Logic << 10) |
            ((int)myWorld.Config.SMLogic << 8) |
            (Randomizer.version.Major << 4) |
            (Randomizer.version.Minor << 0);

        patches.Add((Snes(0x80FF50), UshortBytes(myWorld.Id)));
        patches.Add((Snes(0x80FF52), UshortBytes(configField)));
        patches.Add((Snes(0x80FF54), UintBytes(seed)));
        /* Reserve the rest of the space for future use */
        patches.Add((Snes(0x80FF58), Repeat<byte>(0x00, 8).ToArray()));
        patches.Add((Snes(0x80FF60), AsAscii(seedGuid)));
        patches.Add((Snes(0x80FF80), AsAscii(myWorld.Guid)));
    }

    void WriteCommonFlags() {
        /* Common Combo Configuration flags at [asm]/config.asm */
        if (myWorld.Config.GameMode == GameMode.Multiworld) {
            patches.Add((Snes(0xF47000), UshortBytes(0x0001)));
        }
        if (myWorld.Config.Keysanity) {
            patches.Add((Snes(0xF47006), UshortBytes(0x0001)));
        }
    }

    void WriteGameTitle() {
        var z3Glitch = myWorld.Config.Z3Logic switch {
            Z3Logic.Nmg => "N",
            Z3Logic.Owg => "O",
            _ => "C",
        };
        var smGlitch = myWorld.Config.SMLogic switch {
            SMLogic.Normal => "N",
            SMLogic.Hard => "H",
            _ => "X",
        };
        var title = AsAscii($"ZSM{Randomizer.version}{z3Glitch}{smGlitch}{seed:X8}".PadRight(21)[..21]);
        patches.Add((Snes(0x00FFC0), title));
        patches.Add((Snes(0x80FFC0), title));
    }

    void WriteZ3KeysanityFlags() {
        if (myWorld.Config.Keysanity) {
            patches.Add((Snes(0x40003B), new byte[] { 1 })); // MapMode #$00 = Always On (default) - #$01 = Require Map Item
            patches.Add((Snes(0x400045), new byte[] { 0x0f })); // display ----dcba a: Small Keys, b: Big Key, c: Map, d: Compass
        }
    }

    void WriteSMKeyCardDoors() {
        if (!myWorld.Config.Keysanity)
            return;

        ushort plaquePLm = 0xd410;

        var doorList = new List<ushort[]> {
                        // RoomId  Door Facing                yyxx  Keycard Event Type                   Plaque type               yyxx, Address (if 0 a dynamic PLM is created)
            // Crateria
            new ushort[] { 0x91F8, KeycardDoors.Right,      0x2601, KeycardEvents.CrateriaLevel1,        KeycardPlaque.Level1,   0x2400, 0x0000 },  // Crateria - Landing Site - Door to gauntlet
            new ushort[] { 0x91F8, KeycardDoors.Left,       0x168E, KeycardEvents.CrateriaLevel1,        KeycardPlaque.Level1,   0x148F, 0x801E },  // Crateria - Landing Site - Door to landing site PB
            new ushort[] { 0x948C, KeycardDoors.Left,       0x062E, KeycardEvents.CrateriaLevel2,        KeycardPlaque.Level2,   0x042F, 0x8222 },  // Crateria - Before Moat - Door to moat (overwrite PB door)
            new ushort[] { 0x99BD, KeycardDoors.Left,       0x660E, KeycardEvents.CrateriaBoss,          KeycardPlaque.Boss,     0x640F, 0x8470 },  // Crateria - Before G4 - Door to G4
            new ushort[] { 0x9879, KeycardDoors.Left,       0x062E, KeycardEvents.CrateriaBoss,          KeycardPlaque.Boss,     0x042F, 0x8420 },  // Crateria - Before BT - Door to Bomb Torizo
            
            // Brinstar
            new ushort[] { 0x9F11, KeycardDoors.Left,       0x060E, KeycardEvents.BrinstarLevel1,        KeycardPlaque.Level1,   0x040F, 0x8784 },  // Brinstar - Blue Brinstar - Door to ceiling e-tank room

            new ushort[] { 0x9AD9, KeycardDoors.Right,      0xA601, KeycardEvents.BrinstarLevel2,        KeycardPlaque.Level2,   0xA400, 0x0000 },  // Brinstar - Green Brinstar - Door to etecoon area                
            new ushort[] { 0x9D9C, KeycardDoors.Down,       0x0336, KeycardEvents.BrinstarBoss,          KeycardPlaque.Boss,     0x0234, 0x863A },  // Brinstar - Pink Brinstar - Door to spore spawn                
            new ushort[] { 0xA130, KeycardDoors.Left,       0x161E, KeycardEvents.BrinstarLevel2,        KeycardPlaque.Level2,   0x141F, 0x881C },  // Brinstar - Pink Brinstar - Door to wave gate e-tank
            new ushort[] { 0xA0A4, KeycardDoors.Left,       0x062E, KeycardEvents.BrinstarLevel2,        KeycardPlaque.Level2,   0x042F, 0x0000 },  // Brinstar - Pink Brinstar - Door to spore spawn super

            new ushort[] { 0xA56B, KeycardDoors.Left,       0x161E, KeycardEvents.BrinstarBoss,          KeycardPlaque.Boss,     0x141F, 0x8A1A },  // Brinstar - Before Kraid - Door to Kraid

            // Upper Norfair
            new ushort[] { 0xA7DE, KeycardDoors.Right,      0x3601, KeycardEvents.NorfairLevel1,         KeycardPlaque.Level1,   0x3400, 0x8B00 },  // Norfair - Business Centre - Door towards Ice
            new ushort[] { 0xA923, KeycardDoors.Right,      0x0601, KeycardEvents.NorfairLevel1,         KeycardPlaque.Level1,   0x0400, 0x0000 },  // Norfair - Pre-Crocomire - Door towards Ice

            new ushort[] { 0xA788, KeycardDoors.Left,       0x162E, KeycardEvents.NorfairLevel2,         KeycardPlaque.Level2,   0x142F, 0x8AEA },  // Norfair - Lava Missile Room - Door towards Bubble Mountain
            new ushort[] { 0xAF72, KeycardDoors.Left,       0x061E, KeycardEvents.NorfairLevel2,         KeycardPlaque.Level2,   0x041F, 0x0000 },  // Norfair - After frog speedway - Door to Bubble Mountain
            new ushort[] { 0xAEDF, KeycardDoors.Down,       0x0206, KeycardEvents.NorfairLevel2,         KeycardPlaque.Level2,   0x0204, 0x0000 },  // Norfair - Below bubble mountain - Door to Bubble Mountain
            new ushort[] { 0xAD5E, KeycardDoors.Right,      0x0601, KeycardEvents.NorfairLevel2,         KeycardPlaque.Level2,   0x0400, 0x0000 },  // Norfair - LN Escape - Door to Bubble Mountain
            
            new ushort[] { 0xA923, KeycardDoors.Up,         0x2DC6, KeycardEvents.NorfairBoss,           KeycardPlaque.Boss,     0x2EC4, 0x8B96 },  // Norfair - Pre-Crocomire - Door to Crocomire

            // Lower Norfair
            new ushort[] { 0xB4AD, KeycardDoors.Left,       0x160E, KeycardEvents.LowerNorfairLevel1,    KeycardPlaque.Level1,   0x140F, 0x0000 },  // Lower Norfair - WRITG - Door to Amphitheatre
            new ushort[] { 0xAD5E, KeycardDoors.Left,       0x065E, KeycardEvents.LowerNorfairLevel1,    KeycardPlaque.Level1,   0x045F, 0x0000 },  // Lower Norfair - Exit - Door to "Reverse LN Entry"
            new ushort[] { 0xB37A, KeycardDoors.Right,      0x0601, KeycardEvents.LowerNorfairBoss,      KeycardPlaque.Boss,     0x0400, 0x8EA6 },  // Lower Norfair - Pre-Ridley - Door to Ridley

            // Maridia
            new ushort[] { 0xD0B9, KeycardDoors.Left,       0x065E, KeycardEvents.MaridiaLevel1,         KeycardPlaque.Level1,   0x045F, 0x0000 },  // Maridia - Mt. Everest - Door to Pink Maridia
            new ushort[] { 0xD5A7, KeycardDoors.Right,      0x1601, KeycardEvents.MaridiaLevel1,         KeycardPlaque.Level1,   0x1400, 0x0000 },  // Maridia - Aqueduct - Door towards Beach

            new ushort[] { 0xD617, KeycardDoors.Left,       0x063E, KeycardEvents.MaridiaLevel2,         KeycardPlaque.Level2,   0x043F, 0x0000 },  // Maridia - Pre-Botwoon - Door to Botwoon
            new ushort[] { 0xD913, KeycardDoors.Right,      0x2601, KeycardEvents.MaridiaLevel2,         KeycardPlaque.Level2,   0x2400, 0x0000 },  // Maridia - Pre-Colloseum - Door to post-botwoon

            new ushort[] { 0xD78F, KeycardDoors.Right,      0x2601, KeycardEvents.MaridiaBoss,           KeycardPlaque.Boss,     0x2400, 0xC73B },  // Maridia - Precious Room - Door to Draygon

            new ushort[] { 0xDA2B, KeycardDoors.BossLeft,   0x164E, 0x00f0, /* Door id 0xf0 */           KeycardPlaque.None,     0x144F, 0x0000 },  // Maridia - Change Cac Alley Door to Boss Door (prevents key breaking)

            // Wrecked Ship
            new ushort[] { 0x93FE, KeycardDoors.Left,       0x167E, KeycardEvents.WreckedShipLevel1,     KeycardPlaque.Level1,   0x147F, 0x0000 },  // Wrecked Ship - Outside Wrecked Ship West - Door to Reserve Tank Check
            new ushort[] { 0x968F, KeycardDoors.Left,       0x060E, KeycardEvents.WreckedShipLevel1,     KeycardPlaque.Level1,   0x040F, 0x0000 },  // Wrecked Ship - Outside Wrecked Ship West - Door to Bowling Alley
            new ushort[] { 0xCE40, KeycardDoors.Left,       0x060E, KeycardEvents.WreckedShipLevel1,     KeycardPlaque.Level1,   0x040F, 0x0000 },  // Wrecked Ship - Gravity Suit - Door to Bowling Alley

            new ushort[] { 0xCC6F, KeycardDoors.Left,       0x064E, KeycardEvents.WreckedShipBoss,       KeycardPlaque.Boss,     0x044F, 0xC29D },  // Wrecked Ship - Pre-Phantoon - Door to Phantoon
            
        };

        ushort doorId = 0x0000;
        int plmTablePos = 0xf800;
        foreach (var door in doorList) {
            var doorArgs = door[4] != KeycardPlaque.None ? doorId | door[3] : door[3];
            if (door[6] == 0) {
                // Write dynamic door
                var doorData = door[0..3].SelectMany(x => UshortBytes(x)).Concat(UshortBytes(doorArgs)).ToArray();
                patches.Add((Snes(0x8f0000 + plmTablePos), doorData));
                plmTablePos += 0x08;
            } else {
                // Overwrite existing door
                var doorData = door[1..3].SelectMany(x => UshortBytes(x)).Concat(UshortBytes(doorArgs)).ToArray();
                patches.Add((Snes(0x8f0000 + door[6]), doorData));
                if((door[3] == KeycardEvents.BrinstarBoss && door[0] != 0x9D9C) || door[3] == KeycardEvents.LowerNorfairBoss || door[3] == KeycardEvents.MaridiaBoss || door[3] == KeycardEvents.WreckedShipBoss) {
                    // Overwrite the extra parts of the Gadora with a PLM that just deletes itself
                    patches.Add((Snes(0x8f0000 + door[6] + 0x06), new byte[] { 0x2F, 0xB6, 0x00, 0x00, 0x00, 0x00, 0x2F, 0xB6, 0x00, 0x00, 0x00, 0x00 }));
                }
            }

            // Plaque data
            if (door[4] != KeycardPlaque.None) {
                var plaqueData = UshortBytes(door[0]).Concat(UshortBytes(plaquePLm)).Concat(UshortBytes(door[5])).Concat(UshortBytes(door[4])).ToArray();
                patches.Add((Snes(0x8f0000 + plmTablePos), plaqueData));
                plmTablePos += 0x08;
            }
            doorId += 1;
        }

        patches.Add((Snes(0x8f0000 + plmTablePos), new byte[] { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 }));
    }

    void WriteDiggingGameRng() {
        byte digs = (byte)(rnd.Next(30) + 1);
        patches.Add((Snes(0x308020), new byte[] { digs }));
        patches.Add((Snes(0x1DFD95), new byte[] { digs }));
    }

    // Removes Sword/Shield from Uncle by moving the tiles for
    // sword/shield to his head and replaces them with his head.
    void WriteRemoveEquipmentFromUncle(Item item) {
        if (item.Type != ProgressiveSword) {
            patches.AddRange(new[] {
                (Snes(0xDD263), new byte[] { 0x00, 0x00, 0xF6, 0xFF, 0x00, 0x0E }),
                (Snes(0xDD26B), new byte[] { 0x00, 0x00, 0xF6, 0xFF, 0x00, 0x0E }),
                (Snes(0xDD293), new byte[] { 0x00, 0x00, 0xF6, 0xFF, 0x00, 0x0E }),
                (Snes(0xDD29B), new byte[] { 0x00, 0x00, 0xF7, 0xFF, 0x00, 0x0E }),
                (Snes(0xDD2B3), new byte[] { 0x00, 0x00, 0xF6, 0xFF, 0x02, 0x0E }),
                (Snes(0xDD2BB), new byte[] { 0x00, 0x00, 0xF6, 0xFF, 0x02, 0x0E }),
                (Snes(0xDD2E3), new byte[] { 0x00, 0x00, 0xF7, 0xFF, 0x02, 0x0E }),
                (Snes(0xDD2EB), new byte[] { 0x00, 0x00, 0xF7, 0xFF, 0x02, 0x0E }),
                (Snes(0xDD31B), new byte[] { 0x00, 0x00, 0xE4, 0xFF, 0x08, 0x0E }),
                (Snes(0xDD323), new byte[] { 0x00, 0x00, 0xE4, 0xFF, 0x08, 0x0E }),
            });
        }
        if (item.Type != ProgressiveShield) {
            patches.AddRange(new[] {
                (Snes(0xDD253), new byte[] { 0x00, 0x00, 0xF6, 0xFF, 0x00, 0x0E }),
                (Snes(0xDD25B), new byte[] { 0x00, 0x00, 0xF6, 0xFF, 0x00, 0x0E }),
                (Snes(0xDD283), new byte[] { 0x00, 0x00, 0xF6, 0xFF, 0x00, 0x0E }),
                (Snes(0xDD28B), new byte[] { 0x00, 0x00, 0xF7, 0xFF, 0x00, 0x0E }),
                (Snes(0xDD2CB), new byte[] { 0x00, 0x00, 0xF6, 0xFF, 0x02, 0x0E }),
                (Snes(0xDD2FB), new byte[] { 0x00, 0x00, 0xF7, 0xFF, 0x02, 0x0E }),
                (Snes(0xDD313), new byte[] { 0x00, 0x00, 0xE4, 0xFF, 0x08, 0x0E }),
            });
        }
    }

    void WriteGanonInvicible(GanonInvincible invincible) {
        /* Defaults to $00 (never) at [asm]/z3/randomizer/tables.asm */
        var value = invincible switch {
            GanonInvincible.Never => 0x00,
            GanonInvincible.Always => 0x01,
            GanonInvincible.BeforeAllDungeons => 0x02,
            GanonInvincible.BeforeCrystals => 0x03,
            var x => throw new ArgumentException($"Unknown Ganon invincible value {x}", nameof(invincible))
        };
        patches.Add((Snes(0x30803E), new byte[] { (byte)value }));
    }

    void WriteRngBlock() {
        /* Repoint RNG Block */
        patches.Add((0x420000, Range(0, 1024).Select(x => (byte)rnd.Next(0x100)).ToArray()));
    }

    void WriteSaveAndQuitFromBossRoom() {
        /* Defaults to $00 at [asm]/z3/randomizer/tables.asm */
        patches.Add((Snes(0x308042), new byte[] { 0x01 }));
    }

    void WriteWorldOnAgahnimDeath() {
        /* Defaults to $01 at [asm]/z3/randomizer/tables.asm */
        // Todo: Z3r major glitches disables this, reconsider extending or dropping with glitched logic later.
        //patches.Add((Snes(0x3080A3), new byte[] { 0x01 }));
    }
"""
def Snes(addr: int):
    #/* Redirect hi bank $30 access into ExHiRom lo bank $40 */
    if (addr & 0xFF8000) == 0x308000:
        addr = 0x400000 | (addr & 0x7FFF)
    else: #/* General case, add ExHi offset for banks < $80, and collapse mirroring */
        addr = (0x400000 if addr < 0x800000 else 0)| (addr & 0x3FFFFF)
    if (addr > 0x600000):
        raise Exception(f"Unmapped pc address target ${addr:x}")
    return addr

def getWord(w):
    return (w & 0x00FF, (w & 0xFF00) >> 8)

def getWordArray(w):
    return [w & 0x00FF, (w & 0xFF00) >> 8]

"""
    byte[] UintBytes(int value) => BitConverter.GetBytes((uint)value);

    byte[] UshortBytes(int value) => BitConverter.GetBytes((ushort)value);

    byte[] AsAscii(string text) => Encoding.ASCII.GetBytes(text);

}

}
"""