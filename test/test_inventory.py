from unittest import TestCase

from atlassier.inventory import Inventory


class InventoryTest(TestCase):
    def test_load_example_1(self):
        inventory = Inventory("test/example1")
        data = inventory.load()
        assert data == {"bitbucket": {"repositories": [{"name": "gdcr14"}]}}
