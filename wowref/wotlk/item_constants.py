from enum import Enum

from .dbc import ItemClass, ItemSubClass, SpellItemEnchantment


_inventory_types = [
    None,
    "Head",
    "Neck",
    "Shoulder",
    "Shirt",
    "Chest",
    "Waist",
    "Legs",
    "Feet",
    "Wrist",
    "Hands",
    "Ring",
    "Trinket",
    "One-Hand",
    "Off-Hand",
    "Ranged",
    "Back",
    "Two-Hand",
    "Bag",
    "Tabard",
    "Robe",
    "Main-Hand",
    "Off-Hand",
    "Held in Off-Hand",
    "Ammo",
    "Thrown",
    "Ranged",
    "Quiver",
    "Relic"
]

_bondings = [
    None,
    "Binds when picked up",
    "Binds when equipped",
    "Binds when used",
    "Quest Item",
    "Quest Item1"
]

_triggers = [
    'Use',
    'Equip',
    'Chance on Hit',
    'Soulstone',
    'Use',
    'Learn'
]

_classes = [
    (1, "Warrior"),
    (2, "Paladin"),
    (3, "Hunter"),
    (4, "Rogue"),
    (5, "Priest"),
    (6, "Death Knight"),
    (7, "Shaman"),
    (8, "Mage"),
    (9, "Warlock"),
    (11, "Druid")
]


def iter_allowed_classes(allowed_classes):
    for class_id, class_name in _classes:
        if (1 << (class_id - 1)) & allowed_classes:
            yield class_id, class_name


def get_bonding(bonding):
    return _bondings[bonding]


def get_trigger(trigger):
    return _triggers[trigger]


def get_inventory_type(type):
    try:
        return _inventory_types[type]
    except IndexError:
        return None


def get_class(class_id):
    return ItemClass.get_display_name(class_id)


def get_sub_class(class_id, subclass_id):
    return ItemSubClass.get_display_name(class_id, subclass_id)


def get_enchant_description(enchant_id):
    return SpellItemEnchantment.get_display_name(enchant_id)


def get_gem_item_id(enchant_id):
    return SpellItemEnchantment.get_gem_id(enchant_id)


def does_gem_match_socket(gem, socket_color_id):
    return bool(gem.color_mask & socket_color_id)


class ItemMod(Enum):
    AGILITY = "%c%d Agility"
    AGILITY_SHORT = "Agility"
    ARMOR_PENETRATION_RATING = "Increases your armor penetration rating by %d."
    ARMOR_PENETRATION_RATING_SHORT = "Armor Penetration Rating"
    ATTACK_POWER = "Increases attack power by %d."
    ATTACK_POWER_SHORT = "Attack Power"
    BLOCK_RATING = "Increases your shield block rating by %d."
    BLOCK_RATING_SHORT = "Block Rating"
    BLOCK_VALUE = "Increases your shield value by %d."
    BLOCK_VALUE_SHORT = "Block Value"
    CRIT_MELEE_RATING = "Improves melee critical strike rating by %d."
    CRIT_MELEE_RATING_SHORT = "Critical Strike Rating (Melee)"
    CRIT_RANGED_RATING = "Improves ranged critical strike rating by %d."
    CRIT_RANGED_RATING_SHORT = "Critical Strike Rating (Ranged)"
    CRIT_RATING = "Improves critical strike rating by %d."
    CRIT_RATING_SHORT = "Critical Strike Rating"
    CRIT_SPELL_RATING = "Improves spell critical strike rating by %d."
    CRIT_SPELL_RATING_SHORT = "Critical Strike Rating (Spell)"
    CRIT_TAKEN_MELEE_RATING = "Improves melee critical avoidance rating by %d."
    CRIT_TAKEN_MELEE_RATING_SHORT = "Critical Strike Avoidance Rating (Melee)"
    CRIT_TAKEN_RANGED_RATING = "Improves ranged critical avoidance rating by %d."
    CRIT_TAKEN_RANGED_RATING_SHORT = "Critical Strike Avoidance Rating (Ranged)"
    CRIT_TAKEN_RATING = "Improves critical avoidance rating by %d."
    CRIT_TAKEN_RATING_SHORT = "Critical Strike Avoidance Rating"
    CRIT_TAKEN_SPELL_RATING = "Improves spell critical avoidance rating by %d."
    CRIT_TAKEN_SPELL_RATING_SHORT = "Critical Strike Avoidance Rating (Spell)"
    DAMAGE_PER_SECOND_SHORT = "Damage Per Second"
    DEFENSE_SKILL_RATING = "Increases defense rating by %d."
    DEFENSE_SKILL_RATING_SHORT = "Defense Rating"
    DODGE_RATING = "Increases your dodge rating by %d."
    DODGE_RATING_SHORT = "Dodge Rating"
    EXPERTISE_RATING = "Increases your expertise rating by %d."
    EXPERTISE_RATING_SHORT = "Expertise Rating"
    FERAL_ATTACK_POWER = "Increases attack power by %d in Cat, Bear, Dire Bear, and Moonkin forms only."
    FERAL_ATTACK_POWER_SHORT = "Attack Power In Forms"
    HASTE_MELEE_RATING = "Improves melee haste rating by %d."
    HASTE_MELEE_RATING_SHORT = "Haste Rating (Melee)"
    HASTE_RANGED_RATING = "Improves ranged haste rating by %d."
    HASTE_RANGED_RATING_SHORT = "Haste Rating (Ranged)"
    HASTE_RATING = "Improves haste rating by %d."
    HASTE_RATING_SHORT = "Haste Rating"
    HASTE_SPELL_RATING = "Improves spell haste rating by %d."
    HASTE_SPELL_RATING_SHORT = "Haste Rating (Spell)"
    HEALTH = "%c%d Health"
    HEALTH_REGEN_SHORT = "Health Per 5 Sec."
    HEALTH_REGENERATION = "Restores %d health per 5 sec."
    HEALTH_REGENERATION_SHORT = "Health Regeneration"
    HEALTH_SHORT = "Health"
    HIT_MELEE_RATING = "Improves melee hit rating by %d."
    HIT_MELEE_RATING_SHORT = "Hit Rating (Melee)"
    HIT_RANGED_RATING = "Improves ranged hit rating by %d."
    HIT_RANGED_RATING_SHORT = "Hit Rating (Ranged)"
    HIT_RATING = "Improves hit rating by %d."
    HIT_RATING_SHORT = "Hit Rating"
    HIT_SPELL_RATING = "Improves spell hit rating by %d."
    HIT_SPELL_RATING_SHORT = "Hit Rating (Spell)"
    HIT_TAKEN_MELEE_RATING = "Improves melee hit avoidance rating by %d."
    HIT_TAKEN_MELEE_RATING_SHORT = "Hit Avoidance Rating (Melee)"
    HIT_TAKEN_RANGED_RATING = "Improves ranged hit avoidance rating by %d."
    HIT_TAKEN_RANGED_RATING_SHORT = "Hit Avoidance Rating (Ranged)"
    HIT_TAKEN_RATING = "Improves hit avoidance rating by %d."
    HIT_TAKEN_RATING_SHORT = "Hit Avoidance Rating"
    HIT_TAKEN_SPELL_RATING = "Improves spell hit avoidance rating by %d."
    HIT_TAKEN_SPELL_RATING_SHORT = "Hit Avoidance Rating (Spell)"
    INTELLECT = "%c%d Intellect"
    INTELLECT_SHORT = "Intellect"
    MANA = "%c%d Mana"
    MANA_REGENERATION = "Restores %d mana per 5 sec."
    MANA_REGENERATION_SHORT = "Mana Regeneration"
    MANA_SHORT = "Mana"
    MELEE_ATTACK_POWER_SHORT = "Melee Attack Power"
    PARRY_RATING = "Increases your parry rating by %d."
    PARRY_RATING_SHORT = "Parry Rating"
    POWER_REGEN0_SHORT = "Mana Per 5 Sec."
    POWER_REGEN1_SHORT = "Rage Per 5 Sec."
    POWER_REGEN2_SHORT = "Focus Per 5 Sec."
    POWER_REGEN3_SHORT = "Energy Per 5 Sec."
    POWER_REGEN4_SHORT = "Happiness Per 5 Sec."
    POWER_REGEN5_SHORT = "Runes Per 5 Sec."
    POWER_REGEN6_SHORT = "Runic Power Per 5 Sec."
    RANGED_ATTACK_POWER = "Increases ranged attack power by %d."
    RANGED_ATTACK_POWER_SHORT = "Ranged Attack Power"
    RESILIENCE_RATING = "Improves your resilience rating by %d."
    RESILIENCE_RATING_SHORT = "Resilience Rating"
    SPELL_DAMAGE_DONE = "Increases damage done by magical spells and effects by up to %d."
    SPELL_DAMAGE_DONE_SHORT = "Bonus Damage"
    SPELL_HEALING_DONE = "Increases healing done by magical spells and effects by up to %d."
    SPELL_HEALING_DONE_SHORT = "Bonus Healing"
    SPELL_PENETRATION = "Increases spell penetration by %d."
    SPELL_PENETRATION_SHORT = "Spell Penetration"
    SPELL_POWER = "Increases spell power by %d."
    SPELL_POWER_SHORT = "Spell Power"
    SPIRIT = "%c%d Spirit"
    SPIRIT_SHORT = "Spirit"
    STAMINA = "%c%d Stamina"
    STAMINA_SHORT = "Stamina"
    STRENGTH = "%c%d Strength"
    STRENGTH_SHORT = "Strength"


_int_to_str = {
    0: ItemMod.MANA.value,
    1: ItemMod.HEALTH.value,
    3: ItemMod.AGILITY.value,
    4: ItemMod.STRENGTH.value,
    5: ItemMod.INTELLECT.value,
    6: ItemMod.SPIRIT.value,
    7: ItemMod.STAMINA.value,
    12: ItemMod.DEFENSE_SKILL_RATING.value,
    13: ItemMod.DODGE_RATING.value,
    14: ItemMod.PARRY_RATING.value,
    15: ItemMod.BLOCK_RATING.value,
    16: ItemMod.HIT_MELEE_RATING.value,
    17: ItemMod.HIT_RANGED_RATING.value,
    18: ItemMod.HIT_SPELL_RATING.value,
    19: ItemMod.CRIT_MELEE_RATING.value,
    20: ItemMod.CRIT_RANGED_RATING.value,
    21: ItemMod.CRIT_SPELL_RATING.value,
    22: ItemMod.HIT_TAKEN_MELEE_RATING.value,
    23: ItemMod.HIT_TAKEN_RANGED_RATING.value,
    24: ItemMod.HIT_TAKEN_SPELL_RATING.value,
    25: ItemMod.CRIT_TAKEN_MELEE_RATING.value,
    26: ItemMod.CRIT_TAKEN_RANGED_RATING.value,
    27: ItemMod.CRIT_TAKEN_SPELL_RATING.value,
    28: ItemMod.HASTE_MELEE_RATING.value,
    29: ItemMod.HASTE_RANGED_RATING.value,
    30: ItemMod.HASTE_SPELL_RATING.value,
    31: ItemMod.HIT_RATING.value,
    32: ItemMod.CRIT_RATING.value,
    33: ItemMod.HIT_TAKEN_RATING.value,
    34: ItemMod.CRIT_TAKEN_RATING.value,
    35: ItemMod.RESILIENCE_RATING.value,
    36: ItemMod.HASTE_RATING.value,
    37: ItemMod.EXPERTISE_RATING.value,
    38: ItemMod.ATTACK_POWER.value,
    39: ItemMod.RANGED_ATTACK_POWER.value,
    40: ItemMod.FERAL_ATTACK_POWER.value,
    41: ItemMod.SPELL_HEALING_DONE.value,
    42: ItemMod.SPELL_DAMAGE_DONE.value,
    43: ItemMod.MANA_REGENERATION.value,
    44: ItemMod.ARMOR_PENETRATION_RATING.value,
    45: ItemMod.SPELL_POWER.value,
    46: ItemMod.HEALTH_REGENERATION.value,
    47: ItemMod.SPELL_PENETRATION.value,
    48: ItemMod.BLOCK_VALUE.value
}


def format_item_stat(stat_type, stat_value, with_sign=False):
    if with_sign:
        stat_value = int(stat_value)
        return _int_to_str[stat_type] % ('+' if stat_value > 0 else '-', stat_value)
    else:
        return _int_to_str[stat_type] % int(stat_value)
