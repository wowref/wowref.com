from django.test import TestCase

from ..items import Item, Gem


class ItemTests(TestCase):
    fixtures = ['item_hateful_mage_head.json',
                'item_glad_mage_head.json',
                'item_glad_mage_chest.json',
                'item_glad_mage_shoulders.json',
                'item_glad_mage_legs.json',
                'item_glad_mage_hands.json',
                'item_barb_of_tarasque.json',
                'item_ahune_scythe.json',
                'item_relent_caster_belt.json',
                # 'item_instance_hateful_mage_head.json',
                # 'item_instance_relent_caster_belt.json',
                'gem_delicate_scarlet_ruby.json',
                'gem_runed_cardinal_ruby.json']

    def setUp(self):
        self.item = Item(item_id=41944)  # hateful mage head
        self.barb = Item(item_id=47422)
        self.ahune = Item(item_id=35514)
        # self.head_instance = Item.from_item_instance_id(1)
        # self.belt_instance = Item.from_item_instance_id(2)
        self.maxDiff = None

    def test_using_item_id(self):
        item = Item(item_id=41944)
        self.assertEqual("Hateful Gladiator's Silk Cowl", item.name)

    def test_name(self):
        self.assertEqual("Hateful Gladiator's Silk Cowl", self.item.name)

    def test_required_level(self):
        self.assertEqual(80, self.item.required_level)

    def test_item_level(self):
        self.assertEqual(200, self.item.item_level)

    def test_quality(self):
        self.assertEqual(4, self.item.quality)

    def test_bonding(self):
        self.assertEqual("Binds when picked up", self.item.bonding)

    def test_inv_type_name(self):
        self.assertEqual("Head", self.item.inv_type_name)

    def test_inv_type_id(self):
        self.assertEqual(1, self.item.inv_type_id)

    def test_class_name(self):
        self.assertEqual("Armor", self.item.class_name)

    def test_sub_class_name(self):
        self.assertEqual("Cloth", self.item.sub_class_name)

    def test_armor(self):
        self.assertEqual(244, self.item.armor)

    def test_min_damage(self):
        self.assertIsNone(self.item.min_damage)
        self.assertEqual(108, self.barb.min_damage)

    def test_max_damage(self):
        self.assertIsNone(self.item.max_damage)
        self.assertEqual(342, self.barb.max_damage)

    def test_primary_stats(self):
        expected = ['+102 Stamina', '+45 Intellect']
        self.assertEqual(expected, self.item.primary_stats)

    def test_secondary_stats(self):
        expected = ['Increases spell power by 87.',
                    'Improves critical strike rating by 44.',
                    'Improves your resilience rating by 43.']
        self.assertEqual(expected, self.item.secondary_stats)

    def test_required_classes(self):
        expected = [{'class_id': 8, 'class_name': 'Mage'}]
        self.assertEqual(expected, self.item.required_classes)

    def test_item_set(self):
        item_set = self.item.item_set
        bonuses = item_set['bonuses']
        items = item_set['items']

        self.assertEqual("Gladiator's Regalia", item_set['name'])
        self.assertEqual(0, item_set['matched'])

        self.assertEqual({'name': "Gladiator's Silk Amice"}, items[0])
        self.assertEqual({'name': "Gladiator's Silk Cowl"}, items[1])
        self.assertEqual({'name': "Gladiator's Silk Handguards"}, items[2])
        self.assertEqual({'name': "Gladiator's Silk Raiment"}, items[3])
        self.assertEqual({'name': "Gladiator's Silk Trousers"}, items[4])

        self.assertEqual(
            {'requirement': 2,
             'description': '+100 resilience rating.'},
            bonuses[0])
        self.assertEqual(
            {'requirement': 2,
             'description': 'Increases spell power by 29.'},
            bonuses[1])
        self.assertEqual(
            {'requirement': 4,
             'description': 'Reduces the casting time of your Polymorph spell by 0.15 sec.'},
            bonuses[2])
        self.assertEqual(
            {'requirement': 4,
             'description': 'Increases spell power by 88.'},
            bonuses[3])

    def test_icon_urls(self):
        expected = {
            'small': 'http://cdn.openwow.com/images/icons/small/inv_helmet_139.jpg',
            'medium': 'http://cdn.openwow.com/images/icons/medium/inv_helmet_139.jpg',
            'large': 'http://cdn.openwow.com/images/icons/large/inv_helmet_139.jpg',
        }
        self.assertEqual(expected, self.item.icon_urls)

    def test_delay(self):
        self.assertIsNone(self.item.delay)
        self.assertEqual(1800, self.barb.delay)

    def test_speed(self):
        self.assertIsNone(self.item.speed)
        self.assertEqual("1.80", self.barb.speed)

    def test_dps(self):
        self.assertIsNone(self.item.dps)
        self.assertEqual(125.0, self.barb.dps)

    def test_spells(self):
        expected = [
            {'description': 'Increases spell power by 176.', 'trigger': 'Equip'},
            {'description': "Let the Frostscythe's chill flow through you.",
             'trigger': 'Use'},
            {'description': 'Restores 16 mana per 5 sec.', 'trigger': 'Equip'},
        ]
        self.assertEqual(expected, self.ahune.spells)

        self.assertIsNone(self.item.spells)

    def test_has_flag(self):
        self.assertEqual(True, self.barb.has_flag(4))  # Heroic

    # def test_enchantments(self):
    #     enchantments = self.head_instance.enchantments
    #     self.assertEqual(len(enchantments), 12)

    #     # Has enchant and gem in slot 2
    #     expected = [
    #         3002, 0, 0, 3447, 0, 0, 0, 0, 0, 0, 0, 0
    #     ]
    #     self.assertEqual(expected, enchantments)

    # def test_enchant(self):
    #     expected = "+22 Spell Power and +14 Hit Rating"
    #     self.assertEqual(expected, self.head_instance.enchant)
    #     self.assertIsNone(self.item.enchant)

    def test_gems_should_be_none_if_item_is_not_item_instance(self):
        self.assertEqual([None, None, None], self.item.gems)

    # def test_gems_should_have_three_members(self):
    #     gems = self.head_instance.gems
    #     self.assertEqual(3, len(gems))

    # def test_gems_with_no_blacksmith_socket_gem(self):
    #     # Delicate scarlet ruby
    #     gem = Gem(3447)
    #     gems = self.head_instance.gems
    #     self.assertIsNone(gems[0])
    #     self.assertIsNone(gems[2])
    #     self.assertEqual(gem.name, gems[1].name)

    # def test_gems_with_blacksmith_socket_gem(self):
    #     # Runed cardinal ruby.
    #     gem = Gem(3520)
    #     gems = self.belt_instance.gems
    #     self.assertIsNone(gems[0])
    #     self.assertIsNone(gems[2])
    #     self.assertEqual(gem.name, gems[1].name)

    def test_sockets_should_have_three_members(self):
        self.assertEqual(3, len(self.item.sockets))

    def test_sockets_with_no_gems(self):
        expected = [
            {'color_id': 1, 'name': 'Meta Socket', 'gem': None},
            {'color_id': 2, 'name': 'Red Socket', 'gem': None},
            None
        ]
        self.assertEqual(expected, self.item.sockets)

    # def test_sockets_with_gems_using_regular_sockets(self):
        # head = self.head_instance
        # expected = [
        #     {'color_id': 1, 'name': 'Meta Socket', 'gem': None},
        #     {
        #         'color_id': 2, 'name': 'Red Socket', 'gem': {
        #             'description': "+16 Agility",
        #             'match': True,
        #             'icon_urls': {
        #                 'small': 'http://cdn.openwow.com/images/icons/small/inv_jewelcrafting_gem_28.jpg',
        #                 'medium': 'http://cdn.openwow.com/images/icons/medium/inv_jewelcrafting_gem_28.jpg',
        #                 'large': 'http://cdn.openwow.com/images/icons/large/inv_jewelcrafting_gem_28.jpg',
        #             }
        #         }
        #     },
        #     None
        # ]

        # self.assertEqual(expected, head.sockets)

    # def test_sockets_with_gems_using_blacksmith_socket(self):
    #     belt = self.belt_instance
    #     expected = [
    #         {'color_id': 8, 'name': 'Blue Socket', 'gem': None},
    #         {
    #             'color_id': 14, 'name': 'Prismatic Socket', 'gem': {
    #                 'description': '+23 Spell Power',
    #                 'match': True,
    #                 'icon_urls': {
    #                     'small': 'http://cdn.openwow.com/images/icons/small/inv_jewelcrafting_gem_37.jpg',
    #                     'medium': 'http://cdn.openwow.com/images/icons/medium/inv_jewelcrafting_gem_37.jpg',
    #                     'large': 'http://cdn.openwow.com/images/icons/large/inv_jewelcrafting_gem_37.jpg',
    #                 }
    #             }
    #         },
    #         None
    #     ]
    #     self.assertEqual(expected, belt.sockets)

    def test_socket_bonus(self):
        expected = {'description': '+8 Resilience Rating', 'active': False}
        self.assertEqual(expected, self.item.socket_bonus)


class GemTests(TestCase):
    fixtures = ['gem_delicate_scarlet_ruby.json']

    def setUp(self):
        self.scarlet_ruby = Gem(3447)

    def test_item_id(self):
        self.assertEqual(39997, self.scarlet_ruby.item_id)

    def test_description(self):
        self.assertEqual('+16 Agility', self.scarlet_ruby.description)

    def test_color_mask(self):
        self.assertEqual(2, self.scarlet_ruby.color_mask)
