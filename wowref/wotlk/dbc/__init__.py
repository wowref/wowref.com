from collections import namedtuple
import concurrent.futures
import inspect
import operator
import os
import re

from .lib import (
    AreaTableDBC, CharClassDBC, CharRaceDBC, CharTitlesDBC, GemPropertiesDBC,
    ItemDBC, ItemClassDBC, ItemDisplayInfoDBC, ItemSetDBC, ItemSubClassDBC,
    SpellDBC, SpellCastTimesDBC, SpellDurationDBC, SpellIconDBC, SpellRadiusDBC,
    SpellItemEnchantmentDBC, SpellItemEnchantmentConditionDBC
)
from .timers import LoadTimerWithSuccess, LoadedRecords

import pickle


dbc_path = os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), 'files')
__all__ = [
    'CharClass', 'CharRace', 'CharTitle', 'GemProperties', 'ItemClass',
    'ItemDisplayInfo', 'ItemSet', 'ItemSubClass', 'Spell', 'SpellDuration',
    'SpellItemEnchantment', 'SpellRadius', 'Zone'
]


def load_dbc_data():
    """Loads the DBC data into memory."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for cls in sorted(__all__):
            cls = globals()[cls]
            if issubclass(cls, _DBCDataLoadable):
                executor.submit(cls.load_data)


def get_dbc_path(dbc_name):
    return os.path.join(dbc_path, '%s.dbc' % dbc_name)


def date_diff(secs, n=True, short=False):
    """
    Converts seconds to x hour(s) x minute(s) (and) x second(s)

    Args:
        secs: The seconds that you want to convert
        n: Whether or not you want the word "and" inserted in the correct
            correct places in the string.
        short: If this is True then the string will only contain the first
                letter of each time type, and no ands.

    >>> date_diff(5)
    '5 seconds'
    >>> date_diff(61)
    '1 minute and 1 second'
    >>> date_diff(3615, n=False)
    '1 hour 15 seconds'
    >>> date_diff(3615, short=True)
    '1h 15s'

    """
    time_order = (
        ('week', 60 * 60 * 24 * 7),
        ('day', 60 * 60 * 24),
        ('hour', 60 * 60),
        ('minute', 60),
        ('second', 1)
    )

    if not isinstance(secs, int):
        secs = int(secs)

    secs = abs(secs)
    if secs == 0:
        return '0 seconds'

    time_string = []
    a = time_string.append
    for name, value in time_order:
        x = (secs // value)
        if x >= 1:
            if short:
                a("%i%s" % (x, name[0]))
            else:
                a('%i %s%s' % (x, name, ('s', '')[x is 1]))
            secs -= x * value
    z = len(time_string)
    if n is True and not short and z > 1:
        time_string.insert(z - 1, 'and')

    return ' '.join(time_string)


class _DBCDataLoadable(object):
    """Base class for DBC data storage subclasses.

    DBC data storage should implement this class, it prevents it from being,
    initialized, and ensures it has a loadData class method.

    """

    def __init__(self):
        raise RuntimeError("This class should not be __init__'ed.")

    @classmethod
    def load_data(cls):
        """Load Data into this class structure..."""
        raise NotImplementedError()


class CharTitle(_DBCDataLoadable):
    @classmethod
    def load_data(cls):
        with LoadTimerWithSuccess('CharTitles', subLoad=True):
            dbc = CharTitlesDBC(get_dbc_path("CharTitles"))
            cls.title_data = [
                (f.Id, f.Id // 32, 1 << (f.Id % 32), [f.TitleMale[0], f.TitleFemale[0]], f.SelectionIndex) for f in dbc
            ]
            cls.title_data_dict = dict(
                (f[4], f) for f in cls.title_data
            )

            LoadedRecords(len(cls.title_data))

    @classmethod
    def get_title(cls, title_id):
        return cls.title_data_dict[title_id]

    @classmethod
    def get_name(cls, title_id, gender_id):
        """The title name that corresponds to the title id.

        The title may change, but often does not, depending on which gender it
        is for.

        Returns:
            str: The title with an unused string formatter.

            The string formatter is inserted where the player's name should go.

        Example:
            Note: the title_id in this example is not accurate.
            >>> CharTitle.get_name(1, 0)
                "Gladiator %s"

        """
        return cls.title_data_dict[title_id][3][gender_id]

    @classmethod
    def get_clean_name(cls, title_id, gender_id):
        """This is the same as get_name except it has no string formatting """
        name = cls.get_name(title_id, gender_id)
        name = name % ''
        return name.strip()

    @classmethod
    def __iter__(cls):
        return iter(cls.titleData)


class CharClass(_DBCDataLoadable):
    @classmethod
    def load_data(cls):
        with LoadTimerWithSuccess('ChrClasses', subLoad=True):
            dbc = CharClassDBC(get_dbc_path("ChrClasses"))
            cls.classes_data_dict = dict(
                (f.ClassID, f.name[0]) for f in dbc
            )
            LoadedRecords(len(cls.classes_data_dict))

    @classmethod
    def get_name(cls, class_id):
        return cls.classes_data_dict[class_id]


class CharRace(_DBCDataLoadable):
    @classmethod
    def load_data(cls):
        with LoadTimerWithSuccess('ChrRaces', subLoad=True):
            dbc = CharRaceDBC(get_dbc_path('ChrRaces'))
            cls.races_data_dict = dict(
                (f.RaceID, f.name[0]) for f in dbc
            )
            LoadedRecords(len(cls.races_data_dict))

    @classmethod
    def get_name(cls, race_id):
        return cls.races_data_dict[race_id]


class GemProperties(_DBCDataLoadable):
    @classmethod
    def load_data(cls):
        with LoadTimerWithSuccess('GemProperties', subLoad=True):
            dbc = GemPropertiesDBC(get_dbc_path('GemProperties'))
            cls.gem_properties = dict(
                (f.ID, (f.Type, f.SpellItemEnchantment)) for f in dbc
            )
            LoadedRecords(len(cls.gem_properties))

    @classmethod
    def get_color_mask(cls, gem_id, default=None):
        res = cls.gem_properties.get(gem_id, None)
        if res is None:
            return default
        return res[0]

    @classmethod
    def get_conditions(cls, gem_id, default=None):
        res = cls.gem_properties.get(gem_id, None)
        if res is None:
            return default

        res = res[1]
        if not res:
            return default

        e_cond = SpellItemEnchantment.getEnchantmentCondition(res)
        if not e_cond:
            return default
        return SpellItemEnchantmentCondition.getConditions(e_cond, default)


class ItemData(_DBCDataLoadable):
    @classmethod
    def load_data(cls):
        with LoadTimerWithSuccess('Item', subLoad=True):
            dbc = ItemDBC(get_dbc_path('Item'))
            cls.item = dict(
                (f.ID, f.InventoryType) for f in dbc
            )
            LoadedRecords(len(cls.item))

    @classmethod
    def get_inventory_type(cls, item_id):
        return cls.item[item_id]


class ItemClass(_DBCDataLoadable):
    @classmethod
    def load_data(cls):
        with LoadTimerWithSuccess('ItemClass', subLoad=True):
            dbc = ItemClassDBC(get_dbc_path('ItemClass'))
            cls.item_class = dict(
                (f.ID, f.Name[0]) for f in dbc
            )
            LoadedRecords(len(cls.item_class))

    @classmethod
    def get_display_name(cls, class_id):
        return cls.item_class[class_id]


class ItemDisplayInfo(_DBCDataLoadable):
    @classmethod
    def load_data(cls):
        with LoadTimerWithSuccess('ItemDisplayInfo', subLoad=True):
            dbc = ItemDisplayInfoDBC(get_dbc_path('ItemDisplayInfo'))
            cls.item_display_data_dict = dict(
                (f.ID, f.InvType) for f in dbc
            )
            LoadedRecords(len(cls.item_display_data_dict))

    @classmethod
    def get_icon_name(cls, display_id):
        """The .lower() name for the display_id."""
        return cls.item_display_data_dict[display_id].lower()


class ItemSet(_DBCDataLoadable):
    @classmethod
    def load_data(cls):
        with LoadTimerWithSuccess('ItemSet', subLoad=True):
            dbc = ItemSetDBC(get_dbc_path('ItemSet'))
            cls.item_set = {}
            for f in dbc:
                f.data['display_name'] = f.DisplayName[0]
                f.data['items'] = [i for i in f.Items if i]
                f.data['threshold_pairs'] = sorted(i for i in zip(f.Threshold, f.SpellID) if i[0] and i[1])
                cls.item_set[f.ID] = f.data
            LoadedRecords(len(cls.item_set))

    @classmethod
    def get_item_set(cls, id, default=None):
        return cls.item_set.get(id, default)


class ItemSubClass(_DBCDataLoadable):
    @classmethod
    def load_data(cls):
        with LoadTimerWithSuccess('ItemSubClass', subLoad=True):
            dbc = ItemSubClassDBC(get_dbc_path('ItemSubClass'))
            cls.item_sub_class_dict = {}
            for f in dbc:
                cls.item_sub_class_dict[f.ClassID, f.SubClassID] = f.DisplayName[0]
            LoadedRecords(len(cls.item_sub_class_dict))

    @classmethod
    def get_display_name(cls, class_id, subclass_id, default=None):
        return cls.item_sub_class_dict.get((class_id, subclass_id), default)


_Spell = namedtuple("_Spell", "SpellName SpellIconID ToolTip Description EffectBasePoints DurationIndex "
                              "MaxAffectedTargets RangeIndex ProcChance ProcCharges StackAmount "
                              "EffectAmplitude EffectRadiusIndex CastingTimeIndex "
                              "EffectMiscValue EffectMiscValueB EffectChainTarget EffectMultipleValue "
                              "EffectBonusMultiplier Effect EffectApplyAuraName EffectDieSides "
                              "Reagent ReagentCount Category Rank")


class Spell(_DBCDataLoadable):
    @classmethod
    def load_data(cls):
        with LoadTimerWithSuccess('Spell', subLoad=True):
            _cache_file = os.path.join(dbc_path, 'Spell.dbc.cache')
            if os.path.exists(_cache_file):
                cls.spell_data_dict = pickle.load(open(_cache_file, 'rb'))

            else:
                cls.spell_data_dict = {}
                dbc = SpellDBC(get_dbc_path("Spell"))

                for f in dbc:
                    cls.spell_data_dict[f.ID] = _Spell(
                        f.SpellName[0], f.SpellIconID,
                        f.ToolTip[0], f.Description[0],
                        f.EffectBasePoints, f.DurationIndex,
                        f.MaxAffectedTargets, f.RangeIndex,
                        f.ProcChance, f.ProcCharges,
                        f.StackAmount, f.EffectAmplitude,
                        f.EffectRadiusIndex, f.CastingTimeIndex,
                        f.EffectMiscValue, f.EffectMiscValueB,
                        f.EffectChainTarget, f.EffectMultipleValue,
                        f.EffectBonusMultiplier, f.Effect,
                        f.EffectApplyAuraName, f.EffectDieSides,
                        f.Reagent, f.ReagentCount, f.Category, f.Rank
                    )

                pickle.dump(cls.spell_data_dict, open(_cache_file, 'wb'), -1)

            LoadedRecords(len(cls.spell_data_dict))

    @classmethod
    def get_name(cls, id):
        return cls.spell_data_dict[id].SpellName

    @classmethod
    def get_category(cls, id):
        return cls.spell_data_dict[id].Category

    @classmethod
    def get_icon_id(cls, id):
        return cls.spell_data_dict[id].SpellIconID

    @classmethod
    def get_tooltip(cls, id):
        return cls.spell_data_dict[id].ToolTip

    @classmethod
    def get_description(cls, id):
        return cls.spell_data_dict[id].Description

    @classmethod
    def get_base_points(cls, id):
        return cls.spell_data_dict[id].EffectBasePoints

    @classmethod
    def get_duration(cls, id):
        duration_id = cls.spell_data_dict[id].DurationIndex
        if not duration_id:
            return 0
        return SpellDuration.get_base_duration(duration_id)

    @classmethod
    def get_max_targets(cls, id):
        return cls.spell_data_dict[id].MaxAffectedTargets

    @classmethod
    def get_range_index(cls, id):
        return cls.spell_data_dict[id].RangeIndex

    @classmethod
    def get_effect_amplitude(cls, id):
        return cls.spell_data_dict[id].EffectAmplitude

    @classmethod
    def get_max_effect_radius(cls, id):
        return [SpellRadius.get_max_radius(i) if i else 0 for i in cls.spell_data_dict[id].EffectRadiusIndex]

    @classmethod
    def get_proc_chance(cls, id):
        return cls.spell_data_dict[id].ProcChance

    @classmethod
    def get_proc_charges(cls, id):
        return cls.spell_data_dict[id].ProcCharges

    @classmethod
    def get_stack_amount(cls, id):
        return cls.spell_data_dict[id].StackAmount

    @classmethod
    def get_casting_time_index(cls, id):
        return cls.spell_data_dict[id].CastingTimeIndex

    @classmethod
    def get_casting_times(cls, id):
        return [SpellCastTimes.get_cast_time(i) if i else 0 for i in cls.get_casting_time_index(id)]

    @classmethod
    def get_misc_value(cls, id):
        return cls.spell_data_dict[id].EffectMiscValue

    @classmethod
    def get_misc_value_b(cls, id):
        return cls.spell_data_dict[id].EffectMiscValueB

    @classmethod
    def get_chained_targets(cls, id):
        return cls.spell_data_dict[id].EffectChainTarget

    @classmethod
    def get_effect(cls, id):
        return cls.spell_data_dict[id].Effect

    @classmethod
    def get_effect_apply_aura_name(cls, id):
        return cls.spell_data_dict[id].EffectApplyAuraName

    @classmethod
    def get_die_sides(cls, id):
        return cls.spell_data_dict[id].EffectDieSides

    @classmethod
    def get_reagents(cls, id):
        return cls.spell_data_dict[id].Reagent

    @classmethod
    def get_reagents_count(cls, id):
        return cls.spell_data_dict[id].ReagentCount

    @classmethod
    def get_rank(cls, spell_id):
        return cls.spell_data_dict[spell_id].Rank[0]

    _operators = {
        "*": operator.mul,
        "+": operator.add,
        "-": operator.sub,
        "/": operator.truediv
    }

    _indexed_values = 'sotmMSax'
    _format_re = re.compile(r"""
            \$              # Start with a dollar sign
            (?:             # our first match group for formula ( /1000;
               (?P<f_operator>[/\+\-\*])   # Operator
               (?P<f_rhs>\d+)            # Right hand side
               ;
            )?
            (?P<ref_id>\d+)?
            (?P<type>(SPH|MW|mw)|[hinuSmMsdDaotx])
            (?P<index>\d+)?
            (?:\.
                (?P<round>\d+)
            )?
        """, re.VERBOSE)

    _condition_re = re.compile(r"""
            \$\?
            \(? # Conditional match type
                (?P<type>s)     # Search type s=spell, ???
                (?P<ref_id>\d+)
            \)? # Id to match
            \[(?P<true>[^\]]*)\]   # True pred
            \[(?P<false>[^\]]*)\]  # False pred
        """, re.VERBOSE)

    _pluralizer_re = re.compile(r"""
        (?P<num>\d+)
        \s\$l                   # matches things like 3 $lsec:secs;
        (?P<singular>[^:]*):
        (?P<plural>[^;]*);
    """, re.VERBOSE)

    _evaluate_re = re.compile(r"""
        \$\{
            (?P<expression>[^\}]+)
        \}
        (?:\.
            (?P<round>\d+)
        )?
    """, re.VERBOSE)

    @classmethod
    def get_formatted_description(cls, id):
        """Format the description, pulling in data from all over."""

        # Description Variables
        description = cls.get_description(id)
        description = description.replace("$Ghe:she;", 'he or she')
        description = description.replace("$<mult>", "1")
        description = description.replace("$<duration>", str(Spell.get_duration(id)))
        description = description.replace("$<threat>", "10")

        def sub_points(m):
            groupdict = m.groupdict()
            dont_round = False
            spell_id = int(groupdict['ref_id'] or id)

            type = groupdict['type']
            if type in ('mw', 'MW', 'SPH'):
                return m.group(0)

            results = []

            result = cls._getters[type](spell_id)
            if type in cls._indexed_values:
                index = int(groupdict['index'] or 1) - 1
                die_sides = Spell.get_die_sides(spell_id)[index] - 1

                result = result[index] + (1 if type in 'MmoSsx' else 0)
                if type not in 'mM':
                    result = abs(result)

                if type == 'o':
                    result *= Spell.get_duration(spell_id) / Spell.get_effect_amplitude(spell_id)[index]

                results.append(result)

                if die_sides and type in 'SsMmox':
                    results.append(result + die_sides)

            else:
                results.append(result)

            results_2 = []
            for result in results:
                operator = groupdict['f_operator']
                if operator:
                    rhs = float(groupdict['f_rhs'])
                    lhs = result
                    result = cls._operators[operator](lhs, rhs)
                    if operator == '/' and lhs % rhs != 0:
                        dont_round = True

                round_digits = groupdict['round']
                if round_digits:
                    results_2.append(("%%.%if" % int(round_digits)) % float(result))
                elif isinstance(result, (int, float)):
                    if dont_round:
                        results_2.append("%s" % result)
                    else:
                        results_2.append("%i" % result)
                else:
                    results_2.append(str(result))

            return " to ".join(results_2)

        def do_eval(m):
            code = m.group('expression')
            if '$' in code:
                return '[%s]' % code

            result = eval(code, {}, {})
            round_digits = m.group('round')
            if round_digits:
                return ("%%.%if" % int(round_digits)) % result
            else:
                return "%i" % result

        def do_pluralize(m):
            num = int(m.group('num'))
            return "%s %s" % (m.group('num'), m.group('singular') if num == 1 else m.group('plural'))

        description = cls._format_re.sub(sub_points, description)
        description = cls._condition_re.sub(lambda m: m.group('false'), description)
        description = cls._evaluate_re.sub(do_eval, description)
        description = cls._pluralizer_re.sub(do_pluralize, description)

        return description

    @classmethod
    def __iter__(cls):
        return iter(cls.spell_data_dict)

# This has to be down here, or else it doesn't know what "Spell" is.
Spell._getters = {
    'h': Spell.get_proc_chance,
    'i': Spell.get_max_targets,
    'n': Spell.get_proc_charges,
    'u': Spell.get_stack_amount,
    'S': Spell.get_base_points,
    'm': lambda id: [p for p in Spell.get_base_points(id)],
    'M': Spell.get_base_points,
    's': Spell.get_base_points,
    'd': lambda id: date_diff(Spell.get_duration(id) // 1000),
    'D': lambda id: date_diff(Spell.get_duration(id) // 1000),
    'a': Spell.get_max_effect_radius,
    'o': Spell.get_base_points,
    't': lambda id: [i // 1000 for i in Spell.get_effect_amplitude(id)],
    'x': Spell.get_chained_targets
}


class SpellCastTimes(_DBCDataLoadable):
    @classmethod
    def load_data(cls):
        with LoadTimerWithSuccess('SpellCastTimes', subLoad=True):
            cls.cast_time_dict = {}
            dbc = SpellCastTimesDBC(get_dbc_path("SpellCastTimes"))
            for f in dbc:
                cls.cast_time_dict[f.ID] = f.CastTime

            LoadedRecords(len(cls.cast_time_dict))

    @classmethod
    def get_cast_time(cls, id):
        return cls.cast_time_dict[id]


class SpellDuration(_DBCDataLoadable):
    @classmethod
    def load_data(cls):
        with LoadTimerWithSuccess('SpellDuration', subLoad=True):
            dbc = SpellDurationDBC(get_dbc_path("SpellDuration"))
            cls.duration_data_dict = dict(
                (f.ID, f.BaseDuration) for f in dbc
            )

            LoadedRecords(len(cls.duration_data_dict))

    @classmethod
    def get_base_duration(self, id):
        return self.duration_data_dict[id]


class SpellRadius(_DBCDataLoadable):
    @classmethod
    def load_data(cls):
        with LoadTimerWithSuccess('SpellRadius', subLoad=True):
            dbc = SpellRadiusDBC(get_dbc_path("SpellRadius"))
            cls.radius_data_dict = dict((f.ID, f.RadiusMax) for f in dbc)

            LoadedRecords(len(cls.radius_data_dict))

    @classmethod
    def get_max_radius(cls, id):
        return cls.radius_data_dict[id]


class SpellIcon(_DBCDataLoadable):
    @classmethod
    def load_data(cls):
        with LoadTimerWithSuccess('SpellIcon', subLoad=True):
            dbc = SpellIconDBC(get_dbc_path('SpellIcon'))
            cls.spell_icon_data_dict = dict(
                (f.ID, f.Icon) for f in dbc
            )
            LoadedRecords(len(cls.spell_icon_data_dict))

    @classmethod
    def get_icon(cls, icon_id):
        return cls.spell_icon_data_dict[icon_id].replace('Interface\\Icons\\', '')


class SpellItemEnchantment(_DBCDataLoadable):
    @classmethod
    def load_data(cls):
        with LoadTimerWithSuccess('SpellItemEnchantment', subLoad=True):
            dbc = SpellItemEnchantmentDBC(get_dbc_path('SpellItemEnchantment'))
            cls.spell_item_enchantment = {}
            for f in dbc:
                cls.spell_item_enchantment[f.ID] = (f.DisplayName[0], f.GemID, f.EnchantmentCondition)
            LoadedRecords(len(cls.spell_item_enchantment))

    @classmethod
    def get_display_name(cls, id, default=None):
        i = cls.spell_item_enchantment.get(id, None)
        if i is None:
            return default
        return i[0]

    @classmethod
    def get_gem_id(cls, id, default=None):
        i = cls.spell_item_enchantment.get(id, None)
        if i is None:
            return default
        return i[1]

    @classmethod
    def get_enchantment_condition(cls, id, default=None):
        i = cls.spell_item_enchantment.get(id, None)
        if i is None:
            return default
        return i[2]


class SpellItemEnchantmentCondition(_DBCDataLoadable):
    @classmethod
    def load_data(cls):
        with LoadTimerWithSuccess('SpellItemEnchantmentCondition', subLoad=True):
            dbc = SpellItemEnchantmentConditionDBC(get_dbc_path('SpellItemEnchantmentCondition'))
            cls.spell_item_enchantment_condition = dict(
                (f.ID, f) for f in dbc
            )
            LoadedRecords(len(cls.spell_item_enchantment_condition))

    @classmethod
    def get_conditions(cls, id, default=None):
        return cls.spell_item_enchantment_condition.get(id, default)


class Zone(_DBCDataLoadable):
    @classmethod
    def load_data(cls):
        with LoadTimerWithSuccess('Zone', subLoad=True):
            dbc = AreaTableDBC(get_dbc_path("AreaTable"))
            cls.zone_data = [
                (f.Id, f.Map, f.Name, f.AreaTable) for f in dbc
            ]
            cls.zone_data_dict = dict(
                (f[0], f) for f in cls.zone_data
            )
            LoadedRecords(len(cls.zone_data))

    @classmethod
    def get_name(cls, zone_id):
        return cls.zone_data_dict[zone_id][2][0]

    @classmethod
    def get_full_name(cls, zone_id):
        """The zone name, including it's parents."""
        parent = cls.zone_data_dict[zone_id][3]
        if parent == 0:
            return cls.get_name(zone_id)
        else:
            return "%s, %s" % (cls.get_name(parent), cls.get_name(zone_id))
