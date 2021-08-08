from ..generic.Rules import set_rule, add_rule

from graph.vanilla.graph_locations import locationsDict
from logic.logic import Logic

def add_accessFrom_rule(location, player, accessFrom):
    add_rule(location, lambda state: any((state.can_reach(accessName, player=player) and rule(state.smbm[player])) for accessName, rule in accessFrom.items()))

def add_postAvailable_rule(location, player, func):
    add_rule(location, lambda state: func(state.smbm[player]))

def set_available_rule(location, player, func):
    set_rule(location, lambda state: func(state.smbm[player]))

def set_entrance_rule(entrance, player, func):
    set_rule(entrance, lambda state: func(state.smbm[player]))

def set_rules(world, player):
    world.completion_condition[player] = lambda state: state.has('Mother Brain', player)

    for key, value in locationsDict.items():
        location = world.get_location(key, player)
        set_available_rule(location, player, value.Available)
        if value.AccessFrom is not None:
            add_accessFrom_rule(location, player, value.AccessFrom)
        if value.PostAvailable is not None:
            add_postAvailable_rule(location, player, value.PostAvailable)
            
    for accessPoint in Logic.accessPoints:
        for key, value1 in accessPoint.intraTransitions.items():
            set_entrance_rule(world.get_entrance(accessPoint.Name + "|" + key, player), player, value1)
