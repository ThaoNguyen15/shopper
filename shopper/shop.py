"""
Implementation of Shopper and Grocery Bags
"""
from shopper.store import Item, Store
from collections import defaultdict

class GroceryList():
    def __init__(self, init_items: dict):
        """
        Params:
        init_items: dict of Item: num_units
        """
        self.to_buy = init_items
        self.bought = defaultdict(lambda: 0)

    def buy(self, item: Item, units: int):
        self.bought[item] += units
        remaining = self.to_buy.pop(item, 0) - units
        if remaining > 0:
            self.to_buy[item] = remaining
        
    def finished(self):
        """A grocery list is finished when there's nothing to buy"""
        return self.to_buy == {}

    def units_wanted(self, item: Item):
        return self.to_buy[item]
    
class Shopper():
    def __init__(self, cur_pos: tuple, store: Store):
        self.store = store
        if self.store.is_shelf(cur_pos):
            raise ValueError('Initial value cannot be a shelf location')
        self.cur_pos = cur_pos

    def move(self, deltas: tuple):
        new_pos = (self.cur_pos[0] + deltas[0],
                   self.cur_pos[1] + deltas[1])
        if self.store.is_available(new_pos):
            self.cur_pos = new_pos
        else:
            print('Warning: Try moving to unavailable spot')

    def get_current_pos(self):
        return self.cur_pos
    
class Action():
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        """
        Parameters:
            other: another Action instance
        """
        return self.name == other.name
    
class Move(Action):
    def __init__(self, name: str, deltas: tuple):
        self.deltas = deltas
        super(self.__class__, self).__init__(name)
        
    def get_deltas(self):
        return self.deltas

north = Move('north', [-1, 0])
east = Move('east', [0, 1])
south = Move('south', [1, 0])
west = Move('west', [0, -1])

STANDARD_MOVES = [north, east, south, west]
                       
class GetItem(Action):
    def __init__(self, item: Item):
        self.item = item
        super(self.__class__, self).__init__(name='get_'+str(item))

    def get_item(self):
        return self.item
    
class ShoppingState():
    def __init__(self, pos: tuple, food_spots: dict):
        self.pos = pos
        self.food_spots = food_spots

    def __hash__(self):
        # We only care about the keys in the food_spots dict
        # which are the locations
        return hash(self.pos) & hash(tuple(self.food_spots.keys()))
    
    def get_position(self):
        return self.pos

    def get_food_spots(self):
        return self.food_spots

    def __repr__(self):
        return str(self.pos) + ':' + str(self.food_spots)

    def __eq__(self, other):
        return hash(self) == hash(other)
    
class ShoppingSession():
    def __init__(self, store: Store, glist: GroceryList, strategy,
                 heuristic=lambda x: 0):
        """
        Parameters
            strategy: a Strategy instance
            heuristic: heuristic function
        """
        self.glist = glist
        self.store = store
        self.strategy = strategy
        self.init_food_spots = self.generate_food_spots()
        self.heuristic = heuristic
        
    def add_shopper(self, shopper):
        self.shopper = shopper
        self.init_pos = shopper.get_current_pos()
        # add init state
        self.init_state = ShoppingState(self.init_pos,
                                        self.generate_food_spots())

    def get_initial_state(self):
        return self.init_state
    
    def generate_food_spots(self):
        # food_spots: a dictionary of {spot: food_list}
        food_spots = defaultdict(list)
        for item in self.glist.to_buy:
            food_spots[self.store.item_map[item]].append(item)
        return food_spots

    def is_goal(self, state: ShoppingState):
        return len(state.get_food_spots()) == 0

    def plan_actions(self):
        return self.strategy.plan(self, heuristic=self.heuristic)

    def get_successors(self, state: ShoppingState):
        """
        Return a list of tuple (actions, new_state, cost)
        Actions could be moving or take a specific grocery items off the shelves
        In the list of actions there could be only 1 moving-action
        """
        # iterate through all the possible moves
        # after moving, check to see if there's items we can take
        # update the food_spots list
        successors = []
        x, y = state.get_position()
        food_spots = state.get_food_spots()
        for move in STANDARD_MOVES:
            dx, dy = move.get_deltas()
            new_pos = (x+dx, y+dy)
            new_food_spots = food_spots.copy()
            if self.store.is_available(new_pos):
                # check if there's any item we can take
                actions = [move]
                if new_pos in food_spots:
                    actions += [GetItem(i) for i in new_food_spots.pop(new_pos)]
                successors.append((actions,
                                   ShoppingState(new_pos, new_food_spots),
                                   1))
        return successors
    



