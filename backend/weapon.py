import math

class Weapon:
    def __init__(self, name, weapon_type, physical_dmg, magic_dmg, fire_dmg, light_dmg, holy_dmg, crit_dmg, stamina_dmg, 
                 str_scale, dex_scale, int_scale, faith_scale, arc_scale, weight, upgrade_type, image_url, description="", 
                 level=0, stre=10, dex=10, inte=10, fai=10, arc=10):
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

        # Store base values
        self._base_physical = physical_dmg
        self._base_magic = magic_dmg
        self._base_fire = fire_dmg
        self._base_light = light_dmg
        self._base_holy = holy_dmg

    def name(self): return self._name
    def type(self): return self._type
    
    def physical_damage(self):
        if self._level == 0 and self._playerSTR == 10 and self._playerDEX == 10:
            return self._base_physical
            
        str_bonus = max(0, (self._playerSTR - 10) * self._strSCALE * 0.01)
        dex_bonus = max(0, (self._playerDEX - 10) * self._dexSCALE * 0.01)
        
        if self._upgradeTYPE == 'Somber Smithing Stones':
            level_bonus = 0.08 * self._level
        else:
            level_bonus = 0.02 * self._level
            
        return int(self._base_physical * (1 + str_bonus + dex_bonus + level_bonus))

    def magic_damage(self):
        if self._level == 0 and self._playerINT == 10:
            return self._base_magic
            
        int_bonus = max(0, (self._playerINT - 10) * self._intSCALE * 0.01)
        level_bonus = 0.08 * self._level if self._upgradeTYPE == 'Somber Smithing Stones' else 0.02 * self._level
        return int(self._base_magic * (1 + int_bonus + level_bonus))

    def fire_damage(self):
        if self._level == 0 and self._playerFAI == 10:
            return self._base_fire
            
        fai_bonus = max(0, (self._playerFAI - 10) * self._faiSCALE * 0.01)
        level_bonus = 0.08 * self._level if self._upgradeTYPE == 'Somber Smithing Stones' else 0.02 * self._level
        return int(self._base_fire * (1 + fai_bonus + level_bonus))

    def light_damage(self):
        if self._level == 0 and self._playerFAI == 10:
            return self._base_light
            
        fai_bonus = max(0, (self._playerFAI - 10) * self._faiSCALE * 0.01)
        level_bonus = 0.08 * self._level if self._upgradeTYPE == 'Somber Smithing Stones' else 0.02 * self._level
        return int(self._base_light * (1 + fai_bonus + level_bonus))

    def holy_damage(self):
        if self._level == 0 and self._playerFAI == 10:
            return self._base_holy
            
        fai_bonus = max(0, (self._playerFAI - 10) * self._faiSCALE * 0.01)
        level_bonus = 0.08 * self._level if self._upgradeTYPE == 'Somber Smithing Stones' else 0.02 * self._level
        return int(self._base_holy * (1 + fai_bonus + level_bonus))

    def crit_damage(self): return self._critDMG
    def stamina_damage(self): return self._staminaDMG
    def strength_scaling(self): return self._strSCALE
    def dexterity_scaling(self): return self._dexSCALE
    def intelligence_scaling(self): return self._intSCALE
    def faith_scaling(self): return self._faiSCALE
    def arcane_scaling(self): return self._arcSCALE
    def weight(self): return self._weight
    def upgrade_stone(self): return self._upgradeTYPE
    def image_url(self): return self._imgURL
    def description(self): return self._description

    def _average_player_scaling_damage(self):
        return (
            max(0, (self._playerSTR - 10) * self._strSCALE) + 
            max(0, (self._playerDEX - 10) * self._dexSCALE) + 
            max(0, (self._playerINT - 10) * self._intSCALE) + 
            max(0, (self._playerFAI - 10) * self._faiSCALE) + 
            max(0, (self._playerARC - 10) * self._arcSCALE)
        ) * 0.01

    def _average_weapon_scaling_damage(self):
        if self._upgradeTYPE == 'Somber Smithing Stones':
            rate = 0.08
        else:
            rate = 0.02
        return rate * self._level

    def value(self):
        # Calculate base damage total
        base_damage = (
            self._base_physical + 
            self._base_magic + 
            self._base_fire + 
            self._base_light + 
            self._base_holy + 
            self._critDMG
        ) / max(1, self._staminaDMG)  # Prevent division by zero
        
        # Calculate scaling factors
        level_scaling = self._average_weapon_scaling_damage()
        attr_scaling = self._average_player_scaling_damage()
        
        # Calculate final value with scaling
        scaling_multiplier = 1 + level_scaling + attr_scaling
        final_value = base_damage * scaling_multiplier
        
        # Convert to percentage and normalize
        percentage = final_value * 10  # Adjust this multiplier to get the right range
        
        return percentage

    def set_level(self, level):
        max_level = 10 if self._upgradeTYPE == 'Somber Smithing Stones' else 25
        self._level = max(0, min(level, max_level))

    def set_player_strength(self, stat): self._playerSTR = max(1, min(stat, 99))
    def set_player_dexterity(self, stat): self._playerDEX = max(1, min(stat, 99))
    def set_player_intelligence(self, stat): self._playerINT = max(1, min(stat, 99))
    def set_player_faith(self, stat): self._playerFAI = max(1, min(stat, 99))
    def set_player_arcane(self, stat): self._playerARC = max(1, min(stat, 99))

    def __repr__(self):
        return (f'{"-"*20}\nNAME: {self._name}\nTYPE: {self._type}\nPHYSICAL DAMAGE: {self._physicalDMG}\nMAGIC DAMAGE: {self._magicDMG}\nFIRE DAMAGE: {self._fireDMG}\nLIGHT DAMAGE: {self._lightDMG}\nHOLY DAMAGE: {self._holyDMG}\nCRITICAL DAMAGE: {self._critDMG}\nSTAMINA DAMAGE: {self._staminaDMG}\nSTRENGTH SCALING: {self._strSCALE}\nDEXTERITY SCALING: {self._dexSCALE}\nINTELLIGENCE SCALING: {self._intSCALE}\nFAITH SCALING: {self._faiSCALE}\nARCANE SCALING: {self._arcSCALE}\nWEIGHT: {self._weight}\nUPGRADE TYPE: {self._upgradeTYPE}\nRATING: {round(self.value(),1)}\nLEVEL: {self._level}\n{"-"*20}\n')

    def __str__(self):
        return (f'{self._name} [Type: {self._type} | Rating %: {round(self.value(),1)}% | Weight: {self._weight} | Level: {self._level}]')

    def __len__(self):
        return math.floor(self.value())

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