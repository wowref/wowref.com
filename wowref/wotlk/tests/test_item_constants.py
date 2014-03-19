from django.test import TestCase

from ..item_constants import does_gem_match_socket


class IngameObjectConstantTests(TestCase):
    def test_does_gem_match_socket(self):
        class Gem(object):
            pass
        gem = Gem()

        gem.color_mask = 2
        socket_color_id = 4
        self.assertFalse(does_gem_match_socket(gem, socket_color_id))

        gem.color_mask = 12
        self.assertTrue(does_gem_match_socket(gem, socket_color_id))
