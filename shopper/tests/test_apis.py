from unittest import TestCase

from shopper.store import Item, Store, ItemMap
from shopper.shop import (
    Shopper, GroceryList, ShoppingSession,
    north, east, south, west, GetItem
)

from shopper.search import AstarStrategy, ShoppingState

import numpy as np
from collections import defaultdict

class TestShoppingSession(TestCase):

    grid = np.array([[1, 0, 1, 0, 1],
                     [1, 0, 1, 0, 1],
                     [0, 0, 0, 0, 0]])
    store = Store(grid)
    rice = Item('rice')
    honey = Item('honey')
    fishsauce = Item('fishsauce')
    ramen = Item('ramen')
    imap = ItemMap({rice: (1, 1),
                    ramen: (1, 1),
                    fishsauce: (0, 1),
                    honey: (0, 3)},
                   store)
    glist = GroceryList({rice:1,
                         honey:2})
    shopper = Shopper((2, 1), store)
    # Non heuristic
    ss = ShoppingSession(store, glist, AstarStrategy())
    ss.add_shopper(shopper)

    def test_generate_food_spots(self):
        fs = self.ss.generate_food_spots()
        res = {(1, 1): [self.rice], (0, 3): [self.honey]}
        self.assertEqual(fs, res)
        
    def test_get_successors(self):
        state = ShoppingState((2, 1), self.ss.generate_food_spots())
        succ = self.ss.get_successors(state)
        res = [([north, GetItem(self.rice)],
                ShoppingState((1, 1), defaultdict(list, {(0, 3): [self.honey]})),
                1),
               ([east],
                ShoppingState((2, 2), defaultdict(list, {(1, 1): [self.rice],
                                                          (0, 3): [self.honey]})),
                1),
               ([west],
                ShoppingState((2, 0), defaultdict(list, {(1, 1): [self.rice],
                                                          (0, 3): [self.honey]})),
                1)]
        self.assertEqual(res, succ)
