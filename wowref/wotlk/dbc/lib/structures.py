#!/usr/bin/env python

from .dbcfile import DBCFile
from .dtypes import *


class AreaTableDBC(DBCFile):
    skeleton = [
        Int32('Id'),
        Int32('Map'),

        # The parent AreaTable of this AreaTable. 0 if there is no parent.
        Int32('AreaTable'),
        Int32('AreaBit'),
        Int32('Flags'),

        # Link to SoundProviderPreferences DBC.
        Int32('SoundPreferences'),

        # Link to SoundProviderPreferences DBC.
        Int32('SoundPreferencesUnderWater'),

        # Link to SoundAmbience DBC.
        Int32('SoundAmbience'),

        # Link to ZoneMusic DBC.
        Int32('ZoneMusic'),

        # Link to ZoneIntroMusicTable DBC.
        Int32('ZoneMusicIntroTable'),

        Int32('ExplorationLevel'),
        Localization('Name'),

        # Bitmask link to FactionGroup.dbc
        Int32('FactionGroupMask'),

        Array('LiquidType', Int32, 4),

        Float('MinElevation'),
        Float('AmbientMultiplier'),
        Int32('lightid')
    ]


class ChatProfanityDBC(DBCFile):
    "A collection of all the words censored by the word filter (as a regex)"
    skeleton = [
        Int32('Id'),
        String('Word'),
        Int32('Lang'),
    ]


class GameTipsDBC(DBCFile):
    "A collection of tips displayed during loading screens"
    skeleton = [
        Int32('Id'),
        Localization('Tip'),
    ]


class SpamMessagesDBC(DBCFile):
    "A collection of Regular Expressions to match spam websites"
    skeleton = [
        Int32('Id'),
        String('RegEx'),
    ]


class AchievementDBC(DBCFile):
    skeleton = [
        Int32('Id'),
        Int32('Faction'),
        Int32('Map'),
        Int32('Parent'),
        Localization('Name'),
        Localization('Description'),
        Int32('Category'),
        Int32('Points'),
        Int32('SortOrder'),
        UInt32('Flags'),
        Int32('Icon'),
        Localization('TitleReward'),
        Int32('Count'),
        Int32('RefAchievement'),
    ]


class AchievementCategoryDBC(DBCFile):
    "Achievement Categories"
    skeleton = [
        Int32('Id'),
        Int32('Parent'),
        Localization('Name'),
        UInt32('SortOrder'),
    ]


class AchievementCriteriaDBC(DBCFile):
    skeleton = [
        Int32('Id'),
        Int32('AchievementID'),
        Int32('Type'),
        Array('Values', Int32, 6),
        Localization('Description'),
        Int32('CompletionFlag'),
        Int32('GroupFlag'),
        Int32('TimedID'),
        Int32('TimeLimit'),
        Int32('SortOrder'),
    ]


class CharTitlesDBC(DBCFile):
    skeleton = [
        Int32('Id'),
        PadByte(),  # Int32('Unknown'),
        Localization('TitleMale'),
        Localization('TitleFemale'),
        Int32('SelectionIndex'),
    ]


class SpellDBC(DBCFile):
    skeleton = [
        UInt32('ID'),
        UInt32('Category'),
        UInt32('Dispel'),
        UInt32('Mechanic'),
        UInt32('Attributes'),
        Array('AttributesEx', UInt32, 6),
        PadByte(),  # UInt32('Unk1'),
        UInt32('Stances'),
        PadByte(),  # UInt32('Unk2'),
        UInt32('StancesNot'),
        PadByte(),  # UInt32('Unk3'),
        UInt32('Targets'),
        UInt32('TargetCreatureType'),
        UInt32('RequiresSpellFocus'),
        UInt32('FacingCasterFlags'),
        UInt32('CasterAuraState'),
        UInt32('TargetAuraState'),
        UInt32('CasterAuraStateNot'),
        UInt32('TargetAuraStateNot'),
        UInt32('CasterAuraSpell'),
        UInt32('TargetAuraSpell'),
        UInt32('ExcludeCasterAuraSpell'),
        UInt32('ExcludeTargetAuraSpell'),
        UInt32('CastingTimeIndex'),
        UInt32('RecoveryTime'),
        UInt32('CategoryRecoveryTime'),
        UInt32('InterruptFlags'),
        UInt32('AuraInterruptFlags'),
        UInt32('ChannelInterruptFlags'),
        UInt32('ProcFlags'),
        UInt32('ProcChance'),
        UInt32('ProcCharges'),
        UInt32('MaxLevel'),
        UInt32('BaseLevel'),
        UInt32('SpellLevel'),
        UInt32('DurationIndex'),
        UInt32('PowerType'),
        UInt32('ManaCost'),
        UInt32('ManaCostPerLevel'),
        UInt32('ManaPerSecond'),
        UInt32('ManaPerSecondPerLevel'),
        UInt32('RangeIndex'),
        Float('Speed'),
        UInt32('ModalNextSpell'),
        UInt32('StackAmount'),
        Array('Totem', UInt32, 2),
        Array('Reagent', Int32, 8),
        Array('ReagentCount', UInt32, 8),
        Int32('EquippedItemClass'),
        Int32('EquippedItemSubClassMask'),
        Int32('EquippedItemInventoryTypeMask'),
        Array('Effect', Int32, 3),
        Array('EffectDieSides', Int32, 3),
        Array('EffectRealPointsPerLevel', Int32, 3),
        Array('EffectBasePoints', Int32, 3),
        Array('EffectMechanic', UInt32, 3),
        Array('EffectImplicitTargetA', UInt32, 3),
        Array('EffectImplicitTargetB', UInt32, 3),
        Array('EffectRadiusIndex', UInt32, 3),
        Array('EffectApplyAuraName', UInt32, 3),
        Array('EffectAmplitude', UInt32, 3),
        Array('EffectMultipleValue', Float, 3),
        Array('EffectChainTarget', UInt32, 3),
        Array('EffectItemType', UInt32, 3),
        Array('EffectMiscValue', Int32, 3),
        Array('EffectMiscValueB', Int32, 3),
        Array('EffectTriggerSpell', UInt32, 3),
        Array('EffectPointsPerComboPoint', Float, 3),
        Array('EffectSpellClassMaskA', UInt32, 3),
        Array('EffectSpellClassMaskB', UInt32, 3),
        Array('EffectSpellClassMaskC', UInt32, 3),
        Array('SpellVisual', UInt32, 2),
        UInt32('SpellIconID'),
        UInt32('ActiveIconID'),
        UInt32('SpellPriority'),
        Localization('SpellName'),
        Localization('Rank'),
        Localization('Description'),
        Localization('ToolTip'),
        UInt32('ManaCostPercentage'),
        UInt32('StartRecoveryCategory'),
        UInt32('StartRecoveryTime'),
        UInt32('MaxTargetLevel'),
        UInt32('SpellFamilyName'),
        UInt64('SpellFamilyFlags'),
        UInt32('SpellFamilyFlags2'),
        UInt32('MaxAffectedTargets'),
        UInt32('DmgClass'),
        UInt32('PreventionType'),
        UInt32('StanceOrderBar'),
        Array('DmgMultiplier', Float, 3),
        UInt32('MinFactionID'),
        UInt32('MinReputation'),
        UInt32('RequiredAuraVision'),
        Array('TotemCategory', UInt32, 2),
        Int32('AreaGroupID'),
        UInt32('SchoolMask'),
        UInt32('RuneCostID'),
        UInt32('SpellMissileID'),
        UInt32('PowerDisplayID'),
        Array('EffectBonusMultiplier', Float, 3),  # (12),#Array('Unk4', Float, 3),
        UInt32('SpellDescriptionVariableID'),
        UInt32('SpellDifficultyID'),
    ]


class FactionDBC(DBCFile):
    skeleton = [
        UInt32("ID"),
        Int32("reputationListID"),
        Array("BaseRepRaceMask", UInt32, 4),
        Array("BaseRepClassMask", UInt32, 4),
        Array("BaseRepValue", Int32, 4),
        Array("ReputationFlags", UInt32, 4),
        UInt32("team"),
        Float("spilloverRateIn"),
        Float("spilloverRateOut"),
        UInt32("spilloverMaxRankIn"),
        PadByte(4),
        Localization("name"),
        Localization("description"),
    ]


class MapDBC(DBCFile):
    skeleton = [
        UInt32("MapID"),  # 0
        String("internalname"),  # 1
        UInt32("map_type"),  # 2
        PadByte(8),  # 3, 4
        Localization("name"),  # 5-21
        UInt32("linked_zone"),  # 22
        Localization("hordeIntro"),  # 23-39
        Localization("allianceIntro"),   # 40-56
        UInt32("multimap_id"),  # 57
        PadByte(),  # 58
        Int32("entrance_map"),  # 59
        Float("entrance_x"),  # 60
        Float("entrance_y"),  # 61
        PadByte(),  # 62
        UInt32("addon"),  # 63
        UInt32("unk_time"),  # 64
        UInt32("maxPlayers")  # 65
    ]


class CharClassDBC(DBCFile):
    skeleton = [
        UInt32("ClassID"),  # 0
        PadByte(),  # 1
        UInt32("powerType"),  # 2
        PadByte(),  # 3-4
        Localization("name"),  # 5-21
        Localization("nameFemale"),  # 21-37
        Localization("nameNeutralGender"),  # 38-54
        PadByte(),  # 55
        UInt32("spellfamily"),  # 56
        PadByte(),  # 57
        UInt32("CinematicSequence"),  # 58
        UInt32("expansion")  # 59
    ]


class CharRaceDBC(DBCFile):
    skeleton = [
        UInt32("RaceID"),
        PadByte(),
        UInt32("FactionID"),
        PadByte(),
        UInt32("model_m"),
        UInt32("model_f"),
        PadByte(),
        UInt32("TeamID"),
        PadByte(16),
        UInt32("CinematicSequence"),
        PadByte(4),
        Localization("name"),
        Localization("nameFemale"),
        Localization("nameNeutralGender"),
        PadByte(12),
        UInt32("expansion")
    ]


class ItemDisplayInfoDBC(DBCFile):
    skeleton = [
        Int32('ID'),
        PadByte(16),
        String('InvType'),
        PadByte(76)
    ]


class SpellIconDBC(DBCFile):
    skeleton = [
        Int32('ID'),
        String('Icon')
    ]


class TalentDBC(DBCFile):
    skeleton = [
        Int32('ID'),
        Int32('TalentTab'),
        Int32('Row'),
        Int32('Column'),
        Array('SpellID', Int32, 9),
        Array('ReqTalents', Int32, 3),
        Array('ReqTalentsPoints', Int32, 3),
        Int32('Flags'),  # 1 if the talent has only 1 point, otherwise 0
        Int32('ReqSpellID'),  # 0 or 339 (Only talent with 339 is Nature's Grasp (Druid) )
        Array('AllowForPetFlags', Int32, 2)
    ]


class SpellDurationDBC(DBCFile):
    skeleton = [
        Int32('ID'),
        Int32('BaseDuration'),
        Int32('PerLevel'),
        Int32('MaxDuration')
    ]


class SpellRangeDBC(DBCFile):
    skeleton = [
        Int32('ID'),
        Float('MinRangeHostile'),
        Float('MinRangeFriend'),
        Float('MaxRangeHostile'),
        Float('MaxRangeFriend'),
        Int32('Type'),
        Localization('Description'),
        Localization('ShortName')
    ]


class SpellRadiusDBC(DBCFile):
    skeleton = [
        Int32('ID'),
        Float('RadiusMin'),
        Float('RadiusPerLevel'),
        Float('RadiusMax')
    ]


class SpellCastTimesDBC(DBCFile):
    skeleton = [
        Int32('ID'),
        Int32('CastTime'),
        Float('CastTimePerLevel'),
        Int32('MinCastTime')
    ]


class TalentTabDBC(DBCFile):
    skeleton = [
        Int32('ID'),
        String('TabName'),
        PadByte(64),
        Int32('SpellIcon'),
        Int32('Races'),  # Bitmask (only for characters)
        Int32('Classes'),  # BitMask (only for characters)
        Int32('CreatureFamily'),  # BitMask (only for hunter pets)
        Int32('TabIndex'),  # 0 Based
        String('Background')
    ]


class GlyphPropertiesDBC(DBCFile):
    skeleton = [
        Int32('ID'),
        Int32('SpellID'),
        Int32('Type'),
        Int32('IconID')
    ]


class ItemSubClassDBC(DBCFile):
    skeleton = [
        Int32("ClassID"),
        Int32("SubClassID"),
        Int32("PrerequisiteProficiency"),
        Int32("PostrequisiteProficiency"),
        Int32("Flags"),
        Int32("DisplayFlags"),
        Int32("WeaponParrySeq"),
        Int32("WeaponReadySeq"),
        Int32("WeaponAttackSeq"),
        Int32("WeaponSwingSize"),
        Localization("DisplayName"),
        Localization("VerboseName")
    ]


class GemPropertiesDBC(DBCFile):
    skeleton = [
        Int32("ID"),
        Int32("SpellItemEnchantment"),
        PadByte(8),
        Int32("Type"),
    ]


class SpellItemEnchantmentDBC(DBCFile):
    skeleton = [
        Int32("ID"),                            # 0
        Int32("Charges"),                       # 1
        Array("SpellDispelType", Int32, 3),     # 2 - 4
        Array("MinAmount", Int32, 3),           # 5 - 7
        Array("MaxAmount", Int32, 3),           # 8 - 10
        Array("SpellID", Int32, 3),             # 11-13
        Localization("DisplayName"),            # 14 - 30
        Int32("ItemVisuals"),                   # 31
        Int32("Flags"),  # slot?                # 32
        Int32("GemID"),                         # 33
        Int32("EnchantmentCondition"),          # 34
        Int32("SkillLine"),                     # 35
        Int32("SkillLevel"),                    # 36
        Int32("RequiredLevel"),                 # 37
    ]


class SpellItemEnchantmentConditionDBC(DBCFile):
    skeleton = [
        Int32("ID"),
        Array("Color", Byte, 5),
        Array("LT_Operand", Int32, 5),
        Array("Comparator", Byte, 5),
        Array("CompareColor", Byte, 5),
        Array("Value", Int32, 5),
        Array("Logic", Byte, 5)
    ]


class SpellEffectNamesDBC(DBCFile):
    skeleton = [
        Int32("ID"),
        Array("DisplayName", String, 8),
        PadByte(4)
    ]


class ItemSetDBC(DBCFile):
    skeleton = [
        Int32("ID"),
        Localization("DisplayName"),
        Array("Items", Int32, 17),
        Array("SpellID", Int32, 8),
        Array("Threshold", Int32, 8),
        Int32("RequiredSkill"),
        Int32("RequiredSkillLevel")
    ]


class ItemDBC(DBCFile):
    skeleton = [
        Int32("ID"),
        Int32("Class"),
        Int32("SubClass"),
        Int32("Unk0"),
        Int32("Material"),
        Int32("DisplayId"),
        Int32("InventoryType"),
        Int32("Sheath"),
    ]


class ItemClassDBC(DBCFile):
    skeleton = [
        Int32("ID"),
        Int32("SubClass"),
        UInt32("IsWeapon"),  # Bool
        Localization("Name")
    ]


class SkillLineDBC(DBCFile):
    skeleton = [
        Int32("ID"),
        Int32("CategoryID"),
        Int32("SkillCostID"),
        Localization("Name"),
        Localization("Description"),
        Int32("SpellIcon"),
        Localization("Verb"),
        UInt32("CanLink")   # Bool
    ]


class SkillLineAbilityDBC(DBCFile):
    skeleton = [
        Int32("ID"),
        Int32("SkillLine"),
        Int32("Spell"),  # Spell ID that this record pertains to
        Int32("ReqRaces"),  # Bitmask of required races
        Int32("ReqClasses"),  # Bitmask of required classes
        Int32("ExRaces"),  # Bitmask of excluded races
        Int32("ExClasses"),  # Bitmask of excluded classes
        Int32("MinSkill"),  # Minimum Skill Line rank
        Int32("SpellParent"),  # The spell that supersedes Spell
        Int32("AcquireMethod"),
        Int32("GreyLevel"),  # What level the skill becomes grey
        Int32("GreenLevel"),  # What leve the skill becomes green
        Array("CharPoints", Int32, 2)
    ]


class AchievementDBC(DBCFile):
    skeleton = [
        Int32("ID"),
        Int32("Faction"),
        Int32("Map"),
        Int32("Previous"),
        Localization("Name"),
        Localization("Description"),
        Int32("Category"),
        Int32("Points"),
        Int32("OrderInGroup"),
        Int32("Flags"),
        Int32("SpellIcon"),
        Localization("Reward"),
        Int32("Demands"),
        Int32("ReferencedAchievement")
    ]


class AchievementCategoryDBC(DBCFile):
    skeleton = [
        Int32("ID"),
        Int32("ParentID"),
        Localization("Name"),
        Int32("ui_order")
    ]


class AchievementCriteriaDBC(DBCFile):
    skeleton = [
        Int32("ID"),
        Int32("AchievementID"),
        Int32("Type"),
        Int32("AssetID"),
        Int32("Quantity"),
        Int32("StartEvent"),
        Int32("StartAsset"),
        Int32("FailEvent"),
        Int32("FailAsset"),
        Localization("Description"),
        Int32("Flags"),
        Int32("TimerStartEvent"),
        Int32("TimerAssetID"),
        Int32("TimerTime"),
        Int32("ui_order")
    ]
