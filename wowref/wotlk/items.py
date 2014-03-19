from django.conf import settings
from django.utils.functional import cached_property

from .item_constants import (
    get_inventory_type, get_class, get_sub_class, format_item_stat, get_bonding,
    get_trigger, iter_allowed_classes, get_enchant_description, get_gem_item_id,
    does_gem_match_socket
)
from .models import ItemTemplate
from .dbc import ItemSet, Spell, ItemDisplayInfo, GemProperties


class Item(object):
    def __init__(self, item_id):
        self.item_id = item_id
        self._item_template = ItemTemplate.objects.get(pk=self.item_id)
        self._gems = []

        self._item_instance = None

    @cached_property
    def name(self):
        """The name of the item."""
        return self._item_template.name

    @cached_property
    def required_level(self):
        """The level that is required to equip the item or None if it is 0."""
        return self._item_template.required_level or None

    @cached_property
    def item_level(self):
        return self._item_template.item_level

    @cached_property
    def quality(self):
        """The quality number of the item."""
        return self._item_template.quality

    @cached_property
    def bonding(self):
        """The type of bond the item has.  Example: Binds when picked up."""
        return get_bonding(self._item_template.bonding)

    @cached_property
    def inv_type_name(self):
        """The inventory type of the item, such as Head or Chest."""
        return get_inventory_type(self.inv_type_id)

    @cached_property
    def inv_type_id(self):
        return self._item_template.inv_type_id

    @cached_property
    def class_name(self):
        """The class name of item, such as Weapon or Consumable."""
        return get_class(self._item_template.class_field)

    @cached_property
    def sub_class_name(self):
        """The subclass name of the item, such as Axe or Herb Bag."""
        return get_sub_class(self._item_template.class_field,
                             self._item_template.sub_class)

    @cached_property
    def display_id(self):
        return self._item_template.display_id

    @property
    def armor(self):
        """The amount of armor this item has or None if it has no armor."""
        return self._item_template.armor or None

    @property
    def min_damage(self):
        """The minimum damage the item does or None if it has no damage."""
        return int(self._item_template.dmg_min1) or None

    @property
    def max_damage(self):
        """The maximum damage the item does or None if it has no damage."""
        return int(self._item_template.dmg_max1) or None

    @cached_property
    def primary_stats(self):
        """The primary stats of an item, such as Intellect or Stamina.

        Return:
            A list of all the primary stats. One stat is a string looking
            similar to "+63 Strength" or "-30 Stamina".

            If there are no stats on the item, it will return None.

        Examples:
            Using item 41141, hateful gladiator's chain gauntlets.
            >>> Item.primary_stats
                [
                    '+44 Agaility',
                    '+76 Stamina',
                    '+25 Intellect'
                ]

        """
        primary_stats = []
        a = primary_stats.append
        item_template = self._item_template
        for i in range(1, item_template.stats_count + 1):
            stat_type = item_template['stat_type%i' % i]
            stat_value = item_template['stat_value%i' % i]

            # The primary stats are 1 through 7 but 2 is not used.
            if stat_type <= 7 and stat_type != 2:
                a(format_item_stat(stat_type, stat_value, True))

        return primary_stats or None

    @cached_property
    def secondary_stats(self):
        """The secondary stats of an item, such as dodge rating or attack power.

        Return:
            A list of all the secondary stats.  One stat is a string looking
            similar to 'Increases your attack power by 500' or
            'Improves melee critical strike rating by 55'.

            If there are no stats on the item, it will return None.

        Examples:
            using item 41141, hateful gladiator's chain gauntlets.
            >>> Item.secondary_stats
                [
                    'Increases attack power by 72',
                    'Increases your critical strike rating by 35',
                    'Improves your resilience rating by 35',
                    'Reduces the cooldown of your Tranquilizing Shot by 2 seconds.
                ]

            using item 6256, a fishing pole with no stats.
            >>> Item.secondary_stats
                None

        """
        secondary_stats = []
        a = secondary_stats.append
        item_template = self._item_template
        for i in range(1, item_template.stats_count + 1):
            stat_type = item_template['stat_type%i' % i]
            stat_value = item_template['stat_value%i' % i]

            if stat_type >= 12:
                a(format_item_stat(stat_type, stat_value))

        return secondary_stats or None

    @cached_property
    def required_classes(self):
        """The classes that are able to use this item.

        Return:
            A list of the classes.  Each member of the list is a dict with
            two keys. class_id and class_name.

            If there are no requirements then return None.

        """
        return [
            {'class_name': class_name, 'class_id': class_id}
            for class_id, class_name
            in iter_allowed_classes(self._item_template.allowable_class)
        ] or None

    @property
    def description(self):
        return self._item_template.description or None

    @cached_property
    def icon_urls(self):
        """All the icon urls for this item.

        Return:
            A dict with 3 keys representing the different size icon urls.
            The sizes are small, medium, and large.

        """
        icon = ItemDisplayInfo.get_icon_name(self._item_template.display_id)
        f = '{icon_url}/{{size}}/{icon_name}.jpg'.format(
            icon_url=settings.ICONS_URL,
            icon_name=icon
        )
        return {
            'small': f.format(size='small'),
            'medium': f.format(size='medium'),
            'large': f.format(size='large')
        }

    @property
    def delay(self):
        """The item speed in MS."""
        return self._item_template.delay or None

    @property
    def speed(self):
        """A string representation of the item attack speed in seconds."""
        if not self.delay:
            return None
        return "{:.2f}".format(self.delay / 1000.0)

    @property
    def dps(self):
        """The amount of damage per second the item has or None if it has no dps."""
        if not self.min_damage or not self.max_damage or not self.speed:
            return None
        dps_ = ((self.min_damage + self.max_damage) / 2.0) / float(self.speed)
        return float("{:,.1f}".format(dps_))

    @property
    def arcane_res(self):
        return self._item_template.arcane_res or None

    @property
    def fire_res(self):
        return self._item_template.fire_res or None

    @property
    def frost_res(self):
        return self._item_template.frost_res or None

    @property
    def nature_res(self):
        return self._item_template.nature_res or None

    @property
    def shadow_res(self):
        return self._item_template.shadow_res or None

    @property
    def gem_properties_id(self):
        return self._item_template.gem_properties or None

    @property
    def spells(self):
        """The spells that the item has, or None if it has none.

        Return:
            A list of all the spells that the item has.  One spell is a dict
            with 2 keys.

            description: The description of the spell.
            trigger: The type of trigger the spell has, like Equip or Use.

            If there are no spells, return None.

        """

        spells = []
        a = spells.append
        for x in range(1, 6):
            spell_id = self._item_template['spell_id_%s' % x]

            if spell_id < 1:
                continue

            a({'trigger': get_trigger(self._item_template['spell_trigger_%s' % x]),
               'description': (Spell.get_formatted_description(spell_id))})

        return spells or None

    @cached_property
    def enchantments(self):
        """The ItemInstance.enchantments field without the useless 0s.

        In the ItemInstance.enchantments field there are a bunch of numbers
        separated by a space.  Each number corresponds to an enchant, except
        that there are 2 0's between each enchant that never hold information.
        This is the enchantments field without those uselesss 0s.

        Return:
            A list of all the enchantment Ids.
            The order of the most useful enchantments is as follows:
                perm_enchant, temp_enchant, gem_1, gem_2, gem_3, bonus_socket.

        """
        if not self._item_instance:
            return None

        enchantments = self._item_instance.enchantments.split(' ')
        # Only every 3rd enchant is good, and the last enchant is empty string.
        enchantments = [int(enchant) for enchant in enchantments[:-1:3]]
        return enchantments

    @property
    def enchant(self):
        """The description of the enchant that the item has, or None."""
        enchantments = self.enchantments
        if not enchantments:
            return None

        enchant = enchantments[0]
        if not enchant:
            return None
        return get_enchant_description(enchant)

    @cached_property
    def item_set(self):
        """The item set, if the item is part of an item set, otherwise None.

        Return:
            A dictionary with 4 keys.
            name: The name of the item set.
            matched: The integer number of items that are matched AKA active.

            items: A list of the items that belong to this item set.  Each
                   member of the list is a dict with one key, name, which is
                   the item name.

            bonuses: A list of the bonuses that this item set gives.  Each
                     member of the list is a dict with 2 keys, requirement and
                     description.

                     requirement: The integer number of matched items that are
                                  required to activate this bonus.

                    description: The string spell description of the bonus.
        """
        item_set_id = self._item_template.item_set
        if not item_set_id:
            return None

        item_set = ItemSet.get_item_set(item_set_id)

        items = list(ItemTemplate.objects.filter(pk__in=item_set['items']).values('name'))

        bonuses = []
        a = bonuses.append
        for threshold_pair in item_set['threshold_pairs']:
            a(
                {'requirement': threshold_pair[0],
                 'description': Spell.get_formatted_description(threshold_pair[1])}
            )

        return {
            'name': item_set['display_name'],
            'matched': 0,
            'items': items,
            'bonuses': bonuses
        }

    @property
    def gems(self):
        """The gems that the item has.

        Return:
            A list with 3 members.  Each member is a gem which corresponds to
            a socket in the item.  If the socket either does not exist, or does
            not have a gem in it then the member is None.  If it does have a gem
            then the member is a 'Gem' instance.

        """
        # Can't have any gems if there is no item instance.
        if self._item_instance is None:
            return [None, None, None]

        gems = []
        a = gems.append

        gem_enchants = self.enchantments[2:5]

        for enchant_id in gem_enchants:
            if enchant_id == 0:
                a(None)
                continue

            gem = Gem(enchant_id)
            a(gem)
        return gems

    @property
    def socket_bonus(self):
        """The socket bonus and whether or not it is active or None.

        Return:
            A dict with two keys.
            description: The description of the socket bonus.
            active: Whether or not the bonus is active.

            If there is no socket bonus, return None.

        """
        spell_id = self._item_template.socket_bonus
        if spell_id < 1:
            return None

        active = False

        if self._item_instance is not None:
            for sock in self.sockets:
                if sock['gem'] and sock['gem']['match']:
                    active = True
                    break

        description = get_enchant_description(spell_id)
        return {'description': description, 'active': active}

    @cached_property
    def sockets(self):
        """The sockets that the item has or None if it doesn't have any.

        Return:
            A list with 3 members.  Each member represents a socket.  If the
            item has no socket then that member will be None.

            If it does have the socket then it will be a dict with 3 keys.

            color_id: The integer color id of the socket.
            name: The string name of the socket.
            gem: The gem in the socket.  If there is no gem then it is None.
              If there is a gem then it is represented by a dict with 2 keys.
              description: The description of the gem. Like +16 Agility.
              match: A boolean representing if the gem matches the socket.

        Example:
            An item with 1 socket that has a gem in it.
            >>> Item.sockets
                [{'color_id': 2,
                    'name': 'Red Socket',
                    'gem': {'description': '+23 Spell Power', 'match': True}
                }, None, None]

        """
        sockets = []
        gems = self.gems
        a = sockets.append

        # First do the sockets that are on the item template.
        for x in range(1, 4):
            color = self._item_template['socket_color_%i' % x]
            if not color:
                a(None)
                continue

            socket = {}
            socket['color_id'] = color
            if color == 1:
                socket['name'] = "Meta Socket"
            elif color == 2:
                socket['name'] = "Red Socket"
            elif color == 4:
                socket['name'] = "Yellow Socket"
            elif color == 8:
                socket['name'] = 'Blue Socket'

            # Add the gem to the socket.
            # gems are 0 indexed, item_template sockets are 1 indexed.
            gem = gems[x - 1]
            socket['gem'] = self.render_gem(gem, color)
            a(socket)

        # Now add the socket from blacksmithing / belt buckle.
        # It is kind of hacky, but it works for now.
        if self.enchantments and self.enchantments[6]:
            socket = {}
            socket['color_id'] = 14
            socket['name'] = 'Prismatic Socket'

            # Any item can only have a maximum of 3 sockets.  So we find where
            # the last used socket is and insert our new blacksmithing socket
            # directly before it.
            index = sockets.index(None)

            gem = gems[index]
            socket['gem'] = self.render_gem(gem, socket_color_id=14)
            sockets.insert(index, socket)
            # Pop the last socket since there are now 4 and the maxmimum allowed
            # is 3.
            sockets.pop()

        return sockets or None

    def has_flag(self, flag):
        return bool((1 << (flag - 1)) & self._item_template.flags)

    def render_gem(self, gem, socket_color_id):
        if gem is None:
            return None
        return {'description': gem.description,
                'match': does_gem_match_socket(gem, socket_color_id),
                'icon_urls': gem.icon_urls
                }


class Gem(object):
    def __init__(self, enchant_id):
        self.enchant_id = enchant_id
        self.item_id = get_gem_item_id(self.enchant_id)
        self.item = Item(item_id=self.item_id)
        self.gem_properties_id = self.item.gem_properties_id

    @property
    def name(self):
        return self.item.name

    @property
    def icon_urls(self):
        return self.item.icon_urls

    @property
    def description(self):
        """The gem description, such as '+16 Agility'."""
        return get_enchant_description(self.enchant_id)

    @property
    def color_mask(self):
        return GemProperties.get_color_mask(self.gem_properties_id)
