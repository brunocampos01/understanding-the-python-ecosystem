import time
import unittest
from typing import List

from exercises.multithreading.app.pick_and_clean_fruit import (
    Tree,
    Basket,
    Farmer
)


class TestPickAndCleanFruit(unittest.TestCase):

    def setUp(self):
        self.basket = Basket()
        self.dirty_basket = Basket()
        self.clean_basket = Basket()

    def _generate_farmers(self, tree) -> List:
        return [
            Farmer("farmer1", tree, self.dirty_basket, self.clean_basket),
            Farmer("farmer2", tree, self.dirty_basket, self.clean_basket),
            Farmer("farmer3", tree, self.dirty_basket, self.clean_basket),
            Farmer("cleaner1", tree, self.dirty_basket, self.clean_basket),
            Farmer("cleaner2", tree, self.dirty_basket, self.clean_basket),
            Farmer("cleaner3", tree, self.dirty_basket, self.clean_basket),
        ]

    def test_tree_pick_fruit(self):
        tree = Tree(10)
        for i in range(10):
            self.assertTrue(tree.pick_fruit())
        self.assertFalse(tree.pick_fruit())

    def test_tree_pick_fruit_empty_tree(self):
        tree = Tree(0)
        self.assertFalse(tree.pick_fruit())

    def test_basket_add_fruit(self):
        self.basket.fruits = 0

        self.basket.add_fruit()
        self.assertEqual(self.basket.fruits, 1)
        self.basket.add_fruit()
        self.assertEqual(self.basket.fruits, 2)

    def test_basket_remove_fruit(self):
        self.basket.fruits = 8

        self.basket.remove_fruit()
        self.assertEqual(self.basket.fruits, 7)

    def test_basket_remove_fruit_empty_basket(self):
        self.basket.fruits = 0

        self.basket.remove_fruit()
        self.assertEqual(self.basket.fruits, 0)

    def test_farm_run(self):
        tree = Tree(11)
        farmers = self._generate_farmers(tree)

        for farmer in farmers:
            farmer.start()

        while any(farmer.is_alive() for farmer in farmers):
            time.sleep(0.01)

        self.assertEqual(tree.fruits, 0)
        self.assertEqual(self.dirty_basket.fruits, 0)
        self.assertEqual(self.clean_basket.fruits, 11)

    def test_farm_run_empty_tree(self):
        tree_empty = Tree(0)
        farmers = self._generate_farmers(tree_empty)

        for farmer in farmers:
            farmer.start()

        while any(farmer.is_alive() for farmer in farmers):
            time.sleep(0.01)

        self.assertEqual(tree_empty.fruits, 0)
        self.assertEqual(self.dirty_basket.fruits, 0)
        self.assertEqual(self.clean_basket.fruits, 0)


if __name__ == '__main__':
    unittest.main()
