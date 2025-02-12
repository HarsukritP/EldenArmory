export interface Weapon {
    name: string;
    type: string;
    physical_damage: number;
    magic_damage: number;
    fire_damage: number;
    light_damage: number;
    holy_damage: number;
    crit_damage: number;
    stamina_damage: number;
    weight: number;
    upgrade_type: string;
    value: number;
    strength_scaling?: number;
    dexterity_scaling?: number;
    intelligence_scaling?: number;
    faith_scaling?: number;
    arcane_scaling?: number;
  }