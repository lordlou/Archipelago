import typing
from Options import Choice, OptionSet, Range, OptionDict, OptionList, Option, Toggle, DefaultOnToggle

class DeathLink(Choice):
    """When DeathLink is enabled and someone dies, you will die. With survive reserve tanks can save you."""
    display_name = "Death Link"
    option_disable = 0
    option_enable = 1
    option_enable_survive = 3
    alias_false = 0
    alias_true = 1
    default = 0

class RemoteItems(Toggle):
    """Indicates you get items sent from your own world. This allows coop play of a world."""
    display_name = "Remote Items"  

class Preset(Choice):
    """Skill assumptions determine which tricks the randomizer assumes the player is able to perform."""
    display_name = "Preset"
    option_Easy = 0
    option_Medium = 1
    option_Hard = 2
    option_VeryHard = 3
    option_Expert = 4
    option_Insane = 5
    option_Custom = 6
    default = 0

class Techs(OptionSet):
    "Custom list of techs used when Preset is set to Custom"
    display_name = "Techs"

class Strats(OptionSet):
    "Custom list of strats used when Preset is set to Custom"
    display_name = "Strats"

class ShinesparkTiles(Range):
    """Smaller values assume ability to short-charge over shorter distances."""
    display_name = "Shinespark tiles count"
    range_start = 14
    range_end = 32
    default = 32

class ResourceMultiplier(Range):
    """Leniency factor on assumed energy & ammo usage."""
    display_name = "Resource multiplier"
    range_start = 1
    range_end = 3
    default = 1

class EscapeTimerMultiplier(Range):
    """Leniency factor on escape timer"""
    display_name = "Escape timer multiplier"
    range_start = 1
    range_end = 3
    default = 1

class PhantoonProficiency(Range):
    """Skill level at the Phantoon fight, between 0 and 100"""
    display_name = "Phantoon proficiency"
    range_start = 0
    range_end = 100
    default = 0

class DraygonProficiency(Range):
    """Skill level at the Draygon fight, between 0 and 100"""
    display_name = "Draygon proficiency"
    range_start = 0
    range_end = 100
    default = 0

class RidleyProficiency(Range):
    """Skill level at the Ridley fight, between 0 and 100"""
    display_name = "Ridley proficiency"
    range_start = 0
    range_end = 100
    default = 0

class BotwoonProficiency(Range):
    """Skill level at the Botwoon fight, between 0 and 100"""
    display_name = "Botwoon proficiency"
    range_start = 0
    range_end = 100
    default = 0

class SaveAnimals(Toggle):
    """Take into account extra time needed in the escape"""
    display_name = "Save the animals"

class QualityOfLife(Choice):
    """
    These options help provide a smoother, more intuitive, and less tedious game experience.
    Players wanting a full experience of exploration may want to disable some of these options.
    Three presets are provided:

    - No: All quality-of-life options are turned off.
    - Default: Quality-of-life options are turned to their generally recommended settings (mostly on).
    - Max: All quality-of-life options are turned on to their highest settings.
    """
    display_name = "Quality-of-life options"
    option_no = 0
    option_yes = 1

class Objectives(Choice):
    """
    This setting determines the conditions needed to open the way to Mother Brain:

    - Bosses: Defeat Kraid, Phantoon, Draygon, and Ridley.
    - Minibosses: Defeat Spore Spawn, Crocomire, Botwoon, and Golden Torizo.
    - Metroids: Defeat all the Metroids in the four Metroid rooms.

    In every case, the way to beat the game is to escape after defeating Mother Brain. Objective rooms are marked with X's on the map.
    """
    display_name = "Remote Items"
    option_Bosses = 0
    option_Minibosses = 1
    option_Metroids = 2
    default = 0

class SupersDouble(Toggle):
    """
    If enabled, Supers will deal double damage to Mother Brain, applying to all three phases of the fight.
    Given that the randomizer does not change the ammo distribution (there are only 50 Supers in the game),
    this option reduces the need for a long "ammo hunt" before fighting Mother Brain if the player has not found Charge Beam.
    This option can be set independently of the "Mother Brain fight" setting, though in case of a "Short" Mother Brain fight,
    its practical effect is minimal.
    """
    display_name = "Supers double"

class MotherBrainShort(Toggle):
    """
    This option affects the length of the Mother Brain fight, affecting only phases 2 and 3:

    - Vanilla: The fight behaves as in the vanilla game. Some cutscenes are accelerated, but only in ways that 
    should not interfere with how the player executes the fight (including the stand-up glitch).
    - Short: The fight ends immediately after Mother Brain finishes the first Rainbow Beam attack.
    - Skip: The fight is skipped entirely.

    With the "Short" and "Skip" options, Samus will not get an energy refill before the escape, as the cutscene is 
    skipped where the refill would normally happen. However, Samus will always collect Hyper Beam.
    """
    display_name = "Mother brain short"

class EscapeEnemiesCleared(Toggle):
    """
    If this option is enabled, enemies do not spawn during the escape.

    If this option is disabled, in many rooms enemies will cause heavy lag and visual glitches during the escape 
    (much of which is vanilla game behavior but not normally observable in casual play).

    Note that regardless of whether or not this option is enabled, currently the randomizer opens up major 
    barriers during the escape (though a future version of the randomizer might make these behaviors become 
    part of the same option):

    - All bosses/minibosses are cleared.
    - Shaktool Room is cleared.
    - Acid Chozo Statue acid is drained.
    - Maridia Tube is broken.
    """
    display_name = "Escape enemies cleared"

class EscapeMovementItems(Toggle):
    """
    If enabled, Samus will collect and equip all movement items when acquiring Hyper Beam:

    - Varia Suit
    - Gravity Suit
    - Morph Ball
    - Bombs
    - Spring Ball
    - Screw Attack
    - Hi-Jump Boots
    - Space Jump
    - Speed Booster
    - Grapple
    - X-Ray

    The escape timer is based on an assumption that the player has all these items available. By granting them
    with Hyper Beam, it avoids the possibility of the player needing to hunt for movement items in order to 
    complete the escape fast enough.

    Note: Regardless of this setting, in this randomizer Hyper Beam always breaks bomb blocks, Super blocks,
    and Power Bomb blocks and can open blue/green gates from either side.
    """
    display_name = "Escape movement items"

class MarkMapStations(Toggle):
    """
    If enabled, the map station for the current area will always be visible as a special tile on the map even before
    you have reached it. This affects both the pause menu map and the HUD mini-map.
    """
    display_name = "Mark map stations"

class ItemMarkers(Choice):
    """
    This option affects the way that items are drawn on the map (pause menu map and HUD minimap). There are four choices:

    - Basic: All items are marked on the map with small dots.
    - Majors: Unique items, E-Tanks, and Reserve Tanks are marked with large solid dots; other items are marked with small dots.
    - Uniques: Unique items are marked with large solid dots; other items are marked with small dots.
    - 3Tiered: Unique items are marked with large solid dots; Supers, Power Bombs, E-Tanks, and Reserve
      Tanks are marked with large hollow dots; Missiles are marked with small dots.
    """
    display_name = "Item markers"
    option_Basic = 0
    option_Majors = 1
    option_Uniques = 2
    option_3Tiered = 3

class AllItemsSpawn(Toggle):
    """
    In the vanilla game, some items do not spawn until certain conditions are fulfilled:

    - Items in Wrecked Ship rooms (with the exception of the one item in Wrecked Ship Main Shaft) do not
      spawn until after Phantoon is defeated, when the rooms change to appearing "powered on".
    - The item in the left side of Morph Ball Room and in The Final Missile do not spawn until the planet is 
      awakened.
    - The item in Pit Room does not spawn until entering with Morph and Missiles collected.

    These conditions are apparently unintended artifacts of how the game was coded and are not normally 
    observable during casual play of the vanilla game. However, they can frequently be observed in the 
    randomizer, which can be counter-intuitive for players. When this quality-of-life option is enabled, these 
    items will spawn from the beginning of the game instead of requiring those conditions.
    """
    display_name = "All items spawn"

class FastElevators(Toggle):
    """
    If enabled, Samus moves up and down elevators at a faster speed.

    This also has an effect of reducing the total heat damage taken while on elevators. For example, it
    makes it more likely to be able to survive an unexpected trip down the Lower Norfair Main Hall elevator, which takes
    47 energy in each direction with this option enabled, compared to 109 energy with it disabled.
    """
    display_name = "Fast elevators"
    
class FastDoors(Toggle):
    """
    If enabled, this doubles the speed of aligning the camera and scrolling through the door. It does not affect
    the speed at which the game fades out to black or fades back in, so it should not disrupt the execution of 
    strats across rooms.
    """
    display_name = "Fast doors"


smmr_options: typing.Dict[str, type(Option)] = {
    "remote_items": RemoteItems,
    "death_link": DeathLink,
    "preset": Preset,
    "techs": Techs,
    "strats": Strats,
    "shinespark_tiles": ShinesparkTiles,
    "resource_multiplier": ResourceMultiplier,
    "escape_timer_multiplier": EscapeTimerMultiplier,
    "phantoon_proficiency": PhantoonProficiency,
    "draygon_proficiency": DraygonProficiency,
    "ridley_proficiency": RidleyProficiency,
    "botwoon_proficiency": BotwoonProficiency,
    "save_animals": SaveAnimals,
    "quality_of_life": QualityOfLife,
    "objectives": Objectives,
    #"filler_items": String,
    "supers_double": SupersDouble,
    "mother_brain_short": MotherBrainShort,
    "escape_enemies_cleared": EscapeEnemiesCleared,
    "escape_movement_items": EscapeMovementItems,
    "mark_map_stations": MarkMapStations,
    "item_markers": ItemMarkers,
    "all_items_spawn": AllItemsSpawn,
    "fast_elevators": FastElevators,
    "fast_doors": FastDoors
    }