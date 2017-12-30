"""
Implenmentation of Stores and Items
"""
import numpy as np

class Item():
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        """
        Parameters:
            other: Item type
        """
        return self.name == other.name
    
class Store():
    def __init__(self, grid: np.ndarray):
        """Initiate a store layout with shelves
        Data Structure: a 0-1 matrix. shelf-cell has value 1
        Parameters:
        grid: a numpy matrix of 0-1. 1 indicate shelf locations
        """
        self.grid = grid
        self.item_map = None

    def set_item_map(self, item_map, override=False):
        """
        Parameter: 
            item_map: an ItemMap instance
        """
        if (self.item_map is not None) and (not override):
            raise ValueError('This store already has an Item Map')
        self.item_map = item_map

    def is_shelf(self, spot: tuple):
        return self.grid[spot] == 1
    
    def is_available(self, spot: tuple):
        """Check if a spot is still in grid boundary 
        and is not a shelf location"""
        if spot[0] < 0 or spot[1] < 0:
            return False
        try:
            self.grid[spot]
        except IndexError:
            return False
        return not self.is_shelf(spot)
        
class ItemMap():
    def __init__(self, init_map: dict, store: Store):
        """Initiate a map of grocery item to position that items can be reached"""
        self.imap = init_map
        self.store = store
        self.store.set_item_map(self)
        assert self.is_valid(), 'Initial Map needs to be valid'
        
    def __getitem__(self, item: Item):
        """Implement get function so ItemMap can be treated as a dictionary"""
        return self.imap[item]

    def __setitem__(self, item: Item, place: tuple): 
        """Implement set function so ItemMap can be treated as a dictionary
        Parameter: 
        """
        if not self.store.is_available(place):
            raise ValueError('Location {0} is not available'.format(place))
        self.imap[item] = place

    def __delitem__(self, item):
        """Delete item-place pair"""
        self.imap.pop(item)

    def is_valid(self):
        """Check if all items are located NOT on shelf'"""
        for s in self.imap.values():
            if not self.store.is_available(s):
                return False
        return True
    

    
    
