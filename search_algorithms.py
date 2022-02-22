from node import *
from problem import *
import heapq
import matplotlib.pyplot as plt


class PriorityQueue:
    def __init__(self, items=(), priority_function=(lambda x: x)):
        self.priority_function = priority_function
        self.pqueue = []
        for item in items:
            self.add(item)

    def add(self, item):
        pair = (self.priority_function(item), item)
        heapq.heappush(self.pqueue, pair)

    def pop(self):
        return heapq.heappop(self.pqueue)[1]

    def __len__(self):
        return len(self. pqueue)


def expand(problem, node):
    s = node.state
    actions_node = problem.actions(s)
    for action in actions_node:
        s1 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s1)
        yield Node(state=s1, parent_node=node, action_from_parent=action, path_cost=cost)


def get_path_actions(node):
    actions = []

    if node is None or node.parent_node is None:
        return actions

    while node.parent_node is not None:
        actions.append(node.action_from_parent)
        node = node.parent_node

    actions.reverse()
    return actions


def get_path_states(node):

    states = []

    if node is None:
        return states

    while node is not None:
        states.append(node.state)
        node = node.parent_node
    states.reverse()
    return states


def best_first_search(problem, f):
    node = Node(problem.initial_state)
    frontier = PriorityQueue([node], f)
    reached = {problem.initial_state: node}

    while frontier.__len__() > 0:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            s = child.state
            if (s not in reached) or (child.path_cost < reached[s].path_cost):
                reached[s] = child
                frontier.add(child)
    return None


def best_first_search_treelike(problem, f):
    node = Node(problem.initial_state)
    frontier = PriorityQueue([node], f)
    while frontier.__len__() > 0:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            frontier.add(child)

    return None


def breadth_first_search(problem, treelike=False):

    if treelike:
        return best_first_search_treelike(problem, lambda node: node.depth)
    else:
        return best_first_search(problem, lambda node: node.depth)


def depth_first_search(problem, treelike=False):
    if treelike:
        return best_first_search_treelike(problem, lambda node: -node.depth)
    else:
        return best_first_search(problem, lambda node: -node.depth)


def uniform_cost_search(problem, treelike=False):

    if treelike:
        return best_first_search_treelike(problem, lambda node: node.path_cost)
    else:
        return best_first_search(problem, lambda node: node.path_cost)


def greedy_search(problem, h,  treelike=False):

    if treelike:
        return best_first_search_treelike(problem, lambda node: problem.h(node))
    else:
        return best_first_search(problem, lambda node: problem.h(node))


def astar_search(problem, h, treelike=False):
    if treelike:
        return best_first_search_treelike(problem, lambda node: (node.path_cost + problem.h(node)))
    else:
        return best_first_search(problem, lambda node: (node.path_cost + problem.h(node)))

# _____Vis_____ 
def visualize_route_problem_solution(problem, goal_node, file_name):
    keys = list(problem.map_coords.keys())

    points = list(problem.map_coords.values())
    i = 0
    keys_len = len(keys)

    while i < keys_len:
        if keys[i] == problem.initial_state:
            start = i
            del keys[i]
            keys_len -= 1

        if keys[i] == problem.goal_state:
            ends = i
            del keys[i]
            keys_len -= 1
        i += 1

    plt.scatter(points[start][0], points[start][1], c='red', marker='s')
    del points[start]

    plt.scatter(points[ends][0], points[ends][1], c='green', marker='s')
    del points[ends]

    for i in range(0, len(keys)):
        plt.scatter(points[i][0], points[i][1], c='blue', marker='s')

    # actions Path
    
    keys = list(problem.map_coords.keys())
    points = list(problem.map_coords.values())

    for i in range(0, len(keys)):
        actions = problem.actions(keys[i])
        for j in range(0, len(actions)):
            for z in range(0, len(keys)):
                if actions[j] == keys[z]:

                    plt.arrow(points[i][0], points[i][1], (points[z][0] -
                              points[i][0]), (points[z][1] - points[i][1]), color='black')

   # goal Path
    paths = get_path_states(goal_node)
    for i in range(len(paths)): # Covert to goal path to (x,y)
        for j in range(0, len(keys)):
            if paths[i] == keys[j]:
                paths[i] = points[j]


    for i in range(0, len(paths) - 1): # Draw the Path 
        plt.arrow(paths[i][0], paths[i][1], (paths[i+1][0] - paths[i][0]),
                  (paths[i+1][1] - paths[i][1]), color='magenta')

    plt.savefig(file_name,  format='png')
    plt.close()


def visualize_grid_problem_solution(problem, goal_node, file_name):

    # start Point 
    plt.scatter(problem.initial_state[0][0], problem.initial_state[0][1],  c='green', marker='s')

    # Walls Points
    for i in range(len(problem.wall_coords)):
        plt.scatter(problem.wall_coords[i][0], problem.wall_coords[i][1],  c='black', marker='s')
    # Foods Points
    for i in range(len(problem.food_coords)):
        plt.scatter(problem.food_coords[i][0], problem.food_coords[i][1],  c='red', marker='o')

    
    # path to the Goal 
    states = get_path_states(goal_node)
    
    for i in range(len(states)): # convert the states to (x,y)
       states[i] = states[i][0]

    for i in range(0,len(states)-1): # Draw the Path 
        plt.arrow(states[i][0], states[i][1], (states[i+1][0] - states[i][0] ) , (states[i+1][1] - states[i][1]), color='magenta')

    plt.savefig(file_name,  format='png')
    plt.close()
