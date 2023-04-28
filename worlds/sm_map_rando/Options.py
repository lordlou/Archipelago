import typing
from Options import Choice, Range, OptionDict, OptionList, Option, Toggle, DefaultOnToggle

class StartItemsRemovesFromPool(Toggle):
    """Remove items in starting inventory from pool."""
    display_name = "StartItems Removes From Item Pool"

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


smmr_options: typing.Dict[str, type(Option)] = {
    "start_inventory_removes_from_pool": StartItemsRemovesFromPool,
    "remote_items": RemoteItems,
    "death_link": DeathLink,
    }
