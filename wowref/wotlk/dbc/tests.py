from django.test import TestCase

from . import date_diff, CharClass, CharRace, CharTitle, Spell, Zone, \
    ItemClass


class CharClassTests(TestCase):
    def test_class_name(self):
        self.assertEqual(CharClass.get_name(3), "Hunter")
        self.assertEqual(CharClass.get_name(4), "Rogue")


class CharRaceTests(TestCase):
    def test_race_name(self):
        self.assertEqual(CharRace.get_name(1), "Human")
        self.assertEqual(CharRace.get_name(4), "Night Elf")


class DateDiffTests(TestCase):
    def test_seconds(self):
        self.assertEqual(date_diff(1), '1 second')
        self.assertEqual(date_diff(5), '5 seconds')

    def test_minutes(self):
        self.assertEqual(date_diff(60), '1 minute')
        self.assertEqual(date_diff(120), '2 minutes')

        self.assertEqual(date_diff(121), '2 minutes and 1 second')
        self.assertEqual(date_diff(121, n=False), '2 minutes 1 second')
        self.assertEqual(date_diff(121, n=False, short=True), '2m 1s')


class CharTitleTests(TestCase):
    def test_title_name(self):
        self.assertEqual(CharTitle.get_name(1, 0), "Private %s")
        self.assertEqual(CharTitle.get_name(93, 0), "Loremaster %s")

    def test_clean_title_name(self):
        self.assertEqual(CharTitle.get_clean_name(1, 0), "Private")
        self.assertEqual(CharTitle.get_clean_name(110, 0), "Jenkins")


class ItemClassTests(TestCase):
    def test_get_display_name(self):
        self.assertEqual('Armor', ItemClass.get_display_name(4))


class SpellFormattedDescriptionTests(TestCase):
    def test_amplitude(self):
        """Tests the $o[1,2,3] formatter."""
        self.assertEquals(
            Spell.get_formatted_description(29838),  # second wind rank 2
            "Whenever you are struck by a Stun or Immobilize effect you will generate 20 rage "
            "and 10% of your total health over 10 seconds."
        )

        self.assertEquals(
            Spell.get_formatted_description(29834),  # second wind rank 1
            "Whenever you are struck by a Stun or Immobilize effect you will generate 10 rage "
            "and 5% of your total health over 10 seconds."
        )

    def test_false_conditional(self):
        """Tests the default false conditioner $?(cond)[true][false]"""
        self.assertEquals(
            Spell.get_formatted_description(34861),
            "Heals up to 5 friendly party or raid members within 15 yards of the target for 343 to 379."
        )

        self.assertEquals(
            Spell.get_formatted_description(31687),
            "Summon a Water Elemental to fight for the caster for 45 seconds."
        )

    def test_eval_rounding(self):
        """Tests the evaluator rounding ${$m2/1000}.1"""
        self.assertEquals(
            Spell.get_formatted_description(31683),
            "Increases the damage of your Frostbolt spell by an amount "
            "equal to 10% of your spell power and reduces the cast time by 0.2 sec."
        )

    def test_proc_chance_duration_and_radius(self):
        """Tests $h, $a, $d"""
        self.assertEquals(
            Spell.get_formatted_description(54787),
            "Gives your Ice Barrier spell a 100% chance to freeze all enemies within 10 "
            "yds for 8 seconds when it is destroyed."
        )

    def test_pluralizer_re(self):
        self.assertEquals(
            Spell.get_formatted_description(12571),
            "Increases the duration of your Chill effects by 3 secs, reduces the target's speed by an additional 10%, "
            "and reduces the target's healing received by 20%."
        )

    def test_max_targets(self):
        """Tests $i"""
        self.assertEquals(
            Spell.get_formatted_description(53385),
            "An instant weapon attack that causes 110% of weapon damage to up to 4 enemies within 8 yards.  "
            "The Divine Storm heals up to 3 party or raid members totaling 25% of the damage caused."
        )

    def test_chain_targets(self):
        """Tests $x"""
        self.assertEquals(
            Spell.get_formatted_description(53595),
            "Hammer the current target and up to 3 additional nearby targets, causing 4 times your main hand "
            "damage per second as Holy damage."
        )

    def test_m(self):
        self.assertEquals(
            Spell.get_formatted_description(55684),
            "Reduces the cooldown of your Fade spell by 9 sec."
        )

    def test_a_noindex(self):
        self.assertEquals(
            Spell.get_formatted_description(48505),
            "You summon a flurry of stars from the sky on all targets within 30 yards of the caster, each dealing 145 to "
            "167 Arcane damage. Also causes 26 Arcane damage to all other enemies within 5 yards of the enemy target. "
            "Maximum 20 stars. Lasts 10 seconds.  Shapeshifting into an animal form or mounting cancels the effect. "
            "Any effect which causes you to lose control of your character will suppress the starfall effect."
        )


class ZoneTests(TestCase):
    def test_zone_name(self):
        self.assertEqual(Zone.get_name(2), "Longshore")

    def test_zone_full_name(self):
        self.assertEqual(Zone.get_full_name(3539), "Hellfire Peninsula, The Stair of Destiny")
