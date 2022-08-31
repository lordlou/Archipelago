from __future__ import annotations
import typing

from Options import Choice, Option, Toggle

class MaxSciencePack(Choice):
    """Maximum level of science pack required to complete the game."""
    display_name = "Maximum Required Science Pack"
    option_Electromagnetic_matrix = 0
    option_Energy_matrix = 1
    option_Structure_matrix = 2
    option_Information_matrix = 3
    option_Gravity_matrix = 4
    option_Universe_matrix = 5
    default = 5

    def get_allowed_packs(self):
        return {option.replace("_", " ").capitalize() for option, value in self.options.items() if value <= self.value}

    @classmethod
    def get_ordered_science_packs(cls):
        return [option.replace("_", " ").capitalize() for option, value in sorted(cls.options.items(), key=lambda pair: pair[1])]

    def get_max_pack(self):
        return self.get_ordered_science_packs()[self.value].replace("_", " ").capitalize()

class TechTreeLayout(Choice):
    """Selects how the tech tree nodes are interwoven."""
    display_name = "Technology Tree Layout"
    option_single = 0
    option_small_diamonds = 1
    option_medium_diamonds = 2
    option_large_diamonds = 3
    option_small_pyramids = 4
    option_medium_pyramids = 5
    option_large_pyramids = 6
    option_small_funnels = 7
    option_medium_funnels = 8
    option_large_funnels = 9
    option_trees = 10
    option_choices = 11
    default = 2

class RandomTechIngredients(Toggle):
    """Random Tech Ingredients"""
    display_name = "Random Tech Ingredients"

dsp_options: typing.Dict[str, type(Option)] = {
    "max_science_pack": MaxSciencePack,
    "tech_tree_layout": TechTreeLayout,
    "random_tech_ingredients": RandomTechIngredients
    
}
