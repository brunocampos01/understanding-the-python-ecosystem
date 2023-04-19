import random
import threading
import time


class Tree:
    def __init__(self, fruits):
        self.fruits = fruits
        self.lock = threading.Lock()

    def pick_fruit(self) -> bool:
        """
        Returns:
            bool: True if a fruit was picked,
                  False if there are no more fruits left.
        """
        with self.lock:
            if self.fruits > 0:
                self.fruits -= 1
                return True
            else:
                return False


class Basket:
    def __init__(self):
        self.fruits = 0
        self.lock = threading.Lock()

    def add_fruit(self):
        with self.lock:
            self.fruits += 1

    def remove_fruit(self) -> bool:
        """
        Returns:
            bool: True if a fruit was removed,
                  False if the basket is empty.
        """
        with self.lock:
            if self.fruits > 0:
                self.fruits -= 1
                return True
            else:
                return False


class Farmer(threading.Thread):
    def __init__(self, name, tree, dirty_basket, clean_basket):
        """
        Initialize a farmer with the given name and baskets.

        Args:
            name (str): The name of the farmer.
            tree (Tree): The tree to pick fruit from.
            dirty_basket (Basket): The basket to put dirty fruit in.
            clean_basket (Basket): The basket to put cleaned fruit in.
        """
        super().__init__()
        self.name = name
        self.tree = tree
        self.dirty_basket = dirty_basket
        self.clean_basket = clean_basket
        self.empty_tree = False
        self.time_collect_fruits = random.randint(3, 6)
        self.time_clean_fruits = random.randint(2, 4)

    def run(self):
        """
        Picks fruit from the tree and adds it to the dirty basket,
        then cleans fruit from the dirty basket and adds it to the clean basket.
        """
        while not self.empty_tree:
            # Pick fruit from tree
            time.sleep(self.time_collect_fruits)
            if self.tree.pick_fruit():
                self.dirty_basket.add_fruit()
            else:
                self.empty_tree = True
                break

            # Clean fruit and add to clean basket
            time.sleep(self.time_clean_fruits)
            if self.dirty_basket.remove_fruit():
                self.clean_basket.add_fruit()
            else:
                break


def main():
    tree = Tree(50)
    dirty_basket = Basket()
    clean_basket = Basket()

    farmers = [
        Farmer("farmer1", tree, dirty_basket, clean_basket),
        Farmer("farmer2", tree, dirty_basket, clean_basket),
        Farmer("farmer3", tree, dirty_basket, clean_basket),
        Farmer("cleaner1", tree, dirty_basket, clean_basket),
        Farmer("cleaner2", tree, dirty_basket, clean_basket),
        Farmer("cleaner3", tree, dirty_basket, clean_basket),
    ]

    # Start the threads
    for farmer in farmers:
        farmer.start()

    # Run the simulation for as long as there are active threads
    while any(farmer.is_alive() for farmer in farmers):
        time.sleep(1)
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} Tree ({tree.fruits} fruits) "
              f"- Dirty basket ({dirty_basket.fruits}) "
              f"- Clean Basket ({clean_basket.fruits}) ")


if __name__ == '__main__':
    main()
