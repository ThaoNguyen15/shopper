from shop import ShoppingState, ShoppingSession
import heapq

class SearchNode():
    def __init__(self, actions, state: ShoppingState,
                 cost: float, parent=None):
        """
        Params:
            parent: either a Path instance or None
            action: either an list of Action instances or None
        """
        self.actions = actions
        self.state = state
        self.cost = cost
        self.parent = parent

    def get_actions(self):
        return self.actions

    def get_state(self):
        return self.state

    def get_cost(self):
        return self.cost

    def get_previous_actions(self):
        """Return all the previous nodes leading to this node in reversed order"""
        actions = []
        cur = self
        while True:
            if cur.parent is None:
                break
            else:
                actions.append(cur.actions)
                cur = cur.parent
        # convert to a flat list of actions
        return [a for sub in actions[::-1] for a in sub]

    def __lt__(self, other):
        return self.cost < other.cost

class Strategy():
    def plan(self, shopping_session: ShoppingSession):
        """Return a list of steps that shopper should take
        Returns
            paths: list of tuples
        """
        raise NotImplementedError

class AstarStrategy(Strategy):
    def plan(self, shopping_session: ShoppingSession,
                  heuristic):
        pqueue = [(0, SearchNode(None, shopping_session.get_initial_state(),
                                 0, parent=None))]
        visited_states = set([])
        while len(pqueue) > 0:
            _, path = heapq.heappop(pqueue)
            frontier = path.get_state()
            cost = path.get_cost()
            # check if the path is the goal
            if shopping_session.is_goal(frontier):
                return path.get_previous_actions()
            if frontier in visited_states:
                continue
            visited_states.add(frontier)
            for s in shopping_session.get_successors(frontier):
                actions, new_state, added_cost = s
                new_cost = cost + added_cost
                h = heuristic(new_state)
                heapq.heappush(pqueue,
                               (h+new_cost, SearchNode(actions, new_state,
                                                       new_cost, parent=path)))
        raise ValueError('No viable path found')

### Heuristic Functions ###
def simple_heuristic(state: ShoppingState):
    """Compute heuristic value of a position for the specific shopper"""
    # TODO: improve on this heuristic
    # Distance from closest goal + distance from closest goal & its furthest peers
    # Or Iteratively, sum of distances to the closest points
    locs = state.get_food_spots().keys()
    if len(locs) == 0:
        return 0
    cur_loc = state.get_position()
    # Keep it simple: Distance from the furthest goal
    return max([manhattan_distance(cur_loc, loc) for loc in locs])
    
def manhattan_distance(pos1: tuple, pos2: tuple):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
