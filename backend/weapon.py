import math
class Weapon:
    def __init__(self, name, weapon_type, physical_dmg, magic_dmg, fire_dmg, light_dmg, holy_dmg, crit_dmg, stamina_dmg, str_scale, dex_scale, int_scale, faith_scale, arc_scale, weight, upgrade_type, image_url, description="", level=1, stre=10, dex=10, inte=10, fai=10, arc=10):
        self._name = name
        self._type = weapon_type
        self._physicalDMG = physical_dmg
        self._magicDMG = magic_dmg
        self._fireDMG = fire_dmg
        self._lightDMG = light_dmg
        self._holyDMG = holy_dmg
        self._critDMG = crit_dmg
        self._staminaDMG = stamina_dmg
        self._strSCALE = str_scale
        self._dexSCALE = dex_scale
        self._intSCALE = int_scale
        self._faiSCALE = faith_scale
        self._arcSCALE = arc_scale
        self._weight = weight
        self._upgradeTYPE = upgrade_type
        self._imgURL = image_url
        self._description = description

        self._level = level
        self._playerSTR = stre
        self._playerDEX = dex
        self._playerINT = inte
        self._playerFAI = fai
        self._playerARC = arc

        # Store base values for scaling
        self._base_physical = physical_dmg
        self._base_magic = magic_dmg
        self._base_fire = fire_dmg
        self._base_light = light_dmg
        self._base_holy = holy_dmg

    # Getter functions with scaling calculations
    def name(self): return self._name
    def type(self): return self._type
    
    def physical_damage(self):
        damage = self._base_physical
        str_dex_scaling = (self._playerSTR * self._strSCALE + self._playerDEX * self._dexSCALE) * 0.1
        weapon_level_scaling = self._get_level_multiplier()
        return int(damage * (1 + str_dex_scaling + weapon_level_scaling))

    def magic_damage(self):
        damage = self._base_magic
        int_scaling = self._playerINT * self._intSCALE * 0.1
        weapon_level_scaling = self._get_level_multiplier()
        return int(damage * (1 + int_scaling + weapon_level_scaling))

    def fire_damage(self):
        damage = self._base_fire
        faith_scaling = self._playerFAI * self._faiSCALE * 0.1
        weapon_level_scaling = self._get_level_multiplier()
        return int(damage * (1 + faith_scaling + weapon_level_scaling))

    def light_damage(self):
        damage = self._base_light
        faith_scaling = self._playerFAI * self._faiSCALE * 0.1
        weapon_level_scaling = self._get_level_multiplier()
        return int(damage * (1 + faith_scaling + weapon_level_scaling))

    def holy_damage(self):
        damage = self._base_holy
        faith_scaling = self._playerFAI * self._faiSCALE * 0.1
        weapon_level_scaling = self._get_level_multiplier()
        return int(damage * (1 + faith_scaling + weapon_level_scaling))

    def _get_level_multiplier(self):
        if self._upgradeTYPE == 'Somber Smithing Stones':
            return 0.08 * self._level
        return 0.02 * self._level

    def crit_damage(self):
        return self._critDMG
    def stamina_damage(self):
        return self._staminaDMG
    def strength_scaling(self):
        return self._strSCALE
    def dexterity_scaling(self):
        return self._dexSCALE
    def intelligence_scaling(self):
        return self._intSCALE
    def faith_scaling(self):
        return self._faiSCALE
    def arcane_scaling(self):
        return self._arcSCALE
    def weight(self):
        return self._weight
    def upgrade_stone(self):
        return self._upgradeTYPE
    def image_url(self):
        return self._imgURL
    def description(self):
        return self._description

    def base_phys(self):
        return self._base_physical
    def base_mag(self):
        return self._base_magic
    def base_fire(self):
        return self._base_fire
    def base_light(self):
        return self._base_light
    def base_holy(self):
        return self._base_holy

    def base_total_dmg(self):
        return self._base_physical + self._base_magic + self._base_fire +self._base_light + self._base_holy

    #Value Calculations
    def _average_player_scaling_damage(self):
        return (self._playerSTR * self._strSCALE) + (self._playerDEX * self._dexSCALE) + (self._playerINT * self._intSCALE) + (self._playerFAI * self._faiSCALE) + (self._playerARC * self._arcSCALE)

    def _average_weapon_scaling_damage(self):
        if self._upgradeTYPE == 'Somber Smithing Stones':
            rate = 1.08
        else:
            rate = 1.02
        return rate * self._level

    def _max_value(self):
        return (161 / 40) + (1.02 * self._level) + ((self._playerSTR * 3.5) + (self._playerDEX * 3.5) + (self._playerINT * 3.5) + (self._playerFAI * 4.5) + (self._playerARC * 1))

    def _raw_value(self):
        damage_sum = (self.physical_damage() + self.magic_damage() + self.fire_damage() + self.light_damage() + self.holy_damage() + self._critDMG)/self._staminaDMG
        raw_value = damage_sum + self._average_player_scaling_damage() + self._average_weapon_scaling_damage()
        return raw_value

    def value(self):
        average_rating = (float((self._raw_value()/self._max_value())*100))
        return average_rating

    # Setter Functions with validation
    def set_level(self, level):
        max_level = 10 if self._upgradeTYPE == 'Somber Smithing Stones' else 25
        self._level = max(0, min(level, max_level))

    def set_player_strength(self, stat):
        self._playerSTR = max(1, min(stat, 99))

    def set_player_dexterity(self, stat):
        self._playerDEX = max(1, min(stat, 99))

    def set_player_intelligence(self, stat):
        self._playerINT = max(1, min(stat, 99))

    def set_player_faith(self, stat):
        self._playerFAI = max(1, min(stat, 99))

    def set_player_arcane(self, stat):
        self._playerARC = max(1, min(stat, 99))
    #Magic Methods

    def __repr__(self):
        return (f'{"-"*20}\nNAME: {self._name}\nTYPE: {self._type}\nPHYSICAL DAMAGE: {self._physicalDMG}\nMAGIC DAMAGE: {self._magicDMG}\nFIRE DAMAGE: {self._fireDMG}\nLIGHT DAMAGE: {self._lightDMG}\nHOLY DAMAGE: {self._holyDMG}\nCRITICAL DAMAGE: {self._critDMG}\nSTAMINA DAMAGE: {self._staminaDMG}\nSTRENGTH SCALING: {self._strSCALE}\nDEXTERITY SCALING: {self._dexSCALE}\nINTELLIGENCE SCALING: {self._intSCALE}\nFAITH SCALING: {self._faiSCALE}\nARCANE SCALING: {self._arcSCALE}\nWEIGHT: {self._weight}\nUPGRADE TYPE: {self._upgradeTYPE}\nRATING: {round(self.value(),1)}\nLEVEL: {self._level}\n{"-"*20}\n')
    def __str__(self):
        return (f'{self._name} [Type: {self._type} | Rating %: {round(self.value(),1)}% | Weight: {self._weight} | Level: {self._level}]')
    def __len__(self):
        return math.floor(self._raw_value())
    def __lt__(self, other_weapon):
        return self.value() < other_weapon.value()
    def __gt__(self, other_weapon):
        return self.value() > other_weapon.value()
    def __eq__(self, other_weapon):
        return self.value() == other_weapon.value()
    def __ge__(self, other_weapon):
        return self.value() >= other_weapon.value()
    def __le__(self, other_weapon):
        return self.value() <= other_weapon.value()
    def __ne__(self, other_weapon):
        return self.value() != other_weapon.value()
    def __add__(self, other_weapon):
        try:
            ans = self.value() + other_weapon.value()
        except TypeError:
            ans = 0
        return ans
    def __sub__(self, other_weapon):
        try:
            ans = self.value() - other_weapon.value()
        except TypeError:
            ans = 0
        return ans
    def __mul__(self, other_weapon):
        try:
            ans = self.value() * other_weapon.value()
        except TypeError:
            ans = 0
        return ans
    def __truediv__(self, other_weapon):
        try:
            ans = self.value() / other_weapon.value()
        except TypeError or ZeroDivisionError:
            ans = 0
        return ans
