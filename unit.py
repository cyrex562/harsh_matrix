class UnitAttackDefense(object):
    def __init__(self):
        self.vs_ground = 0
        self.vs_air = 0
        self.vs_space = 0
        self.vs_surface = 0
        self.vs_subsurface = 0
        self.vs_cyber = 0
        self.vs_strategic = 0


class Unit(object):
    def __init__(self):
        self.id = ''
        self.name = ''
        self.unit_code = ''
        self.parent_unit = None
        self.sub_units = []
        self.actions = 0
        self.initiative = 0
        self.attack = UnitAttackDefense()
        self.defense = UnitAttackDefense()
        self.stealth = 0
        self.detect = 0
        self.command_points = 0
        self.logistic_points = 0
        self.strength = 0
        self.morale = 0


# END OF FILE #
