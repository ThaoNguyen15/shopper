from unittest import TestCase

from shopper.store import Item, Store, ItemMap
from shopper.shop import Shopper, GroceryList, ShoppingSession
from shopper.search import AstarStrategy, simple_heuristic

import numpy as np

class TestAstarSearch(TestCase):

    grid = np.array([[1, 0, 1, 0, 1],
                     [1, 0, 1, 0, 1],
                     [0, 0, 0, 0, 0]])
    store = Store(grid)
    imap = ItemMap({Item('rice'): (1, 1),
                    Item('ramen'): (1, 1),
                    Item('fishsauce'): (0, 1),
                    Item('honey'): (0, 3)},
                   store)
    glist = GroceryList({Item('rice'):1,
                         Item('honey'):2})
    shopper = Shopper((2, 1), store)
    
    def test_dummy_heuristic(self):
        ss = ShoppingSession(self.store, self.glist, AstarStrategy())
        ss.add_shopper(self.shopper)
        actions = ss.plan_actions()
        result = ['north', 'get_rice', 'south',
                  'east', 'east', 'north', 'north', 'get_honey']
        self.assertEqual([str(a) for a in actions], result)


    def test_simple_heuristic(self):
        ss = ShoppingSession(self.store, self.glist, AstarStrategy(),
                             simple_heuristic)
        ss.add_shopper(self.shopper)
        actions = ss.plan_actions()
        result = ['north', 'get_rice', 'south',
                  'east', 'east', 'north', 'north', 'get_honey']
        self.assertEqual([str(a) for a in actions], result)        
