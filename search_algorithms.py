#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 22:33:47 2022

@author: zayed
"""

from node import *
from problem import *
import heapq
import matplotlib.pyplot as plt



def expand (problem , node ):
    s = node.state
    actions_node = problem.actions(s)
    for action in actions_node :
        s1= problem.result(s , action)
        cost = node.path_cost + problem.action_cost(s , action , s1)
        yield Node(state= s1 , parent_node=node, action_from_parent=action, path_cost=cost)
    



def get_path_actions(node) : 
    actions =[] 

    if node is None or node.parent_node is None:
        return actions

    while node.parent_node is None :
        actions.append(node.action)

    return actions 

def get_path_states(node): 

    states = []

    if node is None : return states

    while node.parent_node is not None  :
        states.append(node.state)
        node = node.parent_node
    return states 


def best_first_search(problem, f):
    node = Node(problem.initial_state)
    frontier = PriorityQueue([node] , f)
    reached = {problem.initial_state : node}

    while frontier : 
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node 
        for child in expand(problem, node): 
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost :
                reached[s] = child 
                frontier.add(child)
    return None




def best_first_search_treelike(problem, f):
    node = Node(problem.initial_state)
    frontier = PriorityQueue([node] , f)
    while frontier : 
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node 
        for child in expand(problem, node): 
            frontier.add(child)
    return None
        



def breadth_first_search(problem , treelike = False):

    if treelike:
         return best_first_search_treelike(problem, lambda node : node.depth)
    else:
         return best_first_search(problem, lambda node : node.depth)
  
    

def depth_first_search(problem , treelike = False):
    if treelike:
         return best_first_search_treelike(problem, lambda node : -node.depth)
    else:
         return best_first_search(problem, lambda node : -node.depth)



def uniform_cost_search (problem , treelike = False):

    if treelike :
        return best_first_search_treelike(problem, lambda node : node.path_cost)
    else:
        return best_first_search(problem, lambda node : node.path_cost)


def greedy_search(problem ,h,  treelike = False):

    if treelike:
        return best_first_search_treelike(problem, lambda node : problem.h(node))
    else:
        return best_first_search(problem, lambda node : problem.h(node))


def astar_search(problem ,h, treelike = False):
    if treelike :
        return best_first_search_treelike(problem, lambda node : (node.path_cost + problem.h(node)))
    else:
        return best_first_search(problem, lambda node : (node.path_cost + problem.h(node)))
    
    
#_______________________Vis_________________________________________

def visualize_route_problem_solution(problem, goal_node, file_name):
    paths = get_path_states(goal_node)
    

   # keys arr 
    keys = list(problem.map_coords.keys())

    points = list(problem.map_coords.values())
    i = 0 
    keys_len = len(keys)
    
    while i < keys_len:
            if keys[i] == problem.initial_state : 
                start = i 
                del keys[i]
                keys_len -=1
            
            if keys[i] == problem.goal_state :
                ends = i 
                del keys[i]
                keys_len -=1
            i += 1 

    # initial state Point : 
    plt.scatter( points[start][0], points[start][1], c = 'red' , marker = 's' , s = 50 , edgecolors='none')
    del points[start]

    # Goal state Point : 
    plt.scatter( points[ends][0], points[ends][1], c = 'green' , marker = 's' , s = 50 , edgecolors='none')
    del points[ends]


    # trans state Points :

    for i in range(0,len(keys)):
        plt.scatter(points[i][0], points[i][1] , c='blue' , marker = 's' , s = 50 , edgecolors='none')
    

    # Arrows 

    keys = list(problem.map_coords.keys())
    points = list(problem.map_coords.values())

    # black Arrow (Possible Actions ) : 
   

    for i in range(0,len(keys)):                    # find the black arrow , 
        actions = problem.actions(keys[i])          
        for j in range(0, len(actions)): 
            for z in range(0, len(keys)): 
                if actions[j] == keys[z]: 
                    
                    plt.arrow(points[i][0] , points[i][1] , (points[z][0] - points[i][0]) , (points[z][1] -  points[i][1] ) , head_width = 0)


    # path to goal arrow : 
    initial_pa = True
    notFind = True 
    for i in range(0,len(keys)):
        if notFind and len(paths) == 0 :
            break 
        if notFind: 
            nextp = paths.pop()
            notFind = False  
        if nextp == keys[i] : 
            if initial_pa:
                plt.arrow(points[start][0], points[start][1] , (points[i][0] - points[start][0] ), (points[i][1] - points[start][1]) , color = 'magenta' , head_width = 0 )
                initial_pa = False
                previous = i 
            else:
                plt.arrow(points[previous][0], points[previous][1] , (points[i][0] - points[previous][0] ), (points[i][1] - points[previous][1]) , color = 'magenta' , head_width = 0 )
                previous = i 
            notFind = True  




    plt.savefig(file_name ,  format='png')
    plt.close()


def visualize_grid_problem_solution(problem, goal_node, file_name) : 
    # initial plot 
    plt.scatter( problem.initial_state[0][0],problem.initial_state[0][1] ,  c = 'green' , marker = 's' , s = 50 , edgecolors='none')

    #walls plot 

    for i in range(len(problem.wall_coords)):
        plt.scatter( problem.wall_coords[i][0],problem.wall_coords[i][1] ,  c = 'black' , marker = 's' , s = 50 , edgecolors='none')

    
    # foods plot :

    for i in range(len(problem.food_coords)):
        plt.scatter( problem.food_coords[i][0],problem.food_coords[i][1] ,  c = 'red' , marker = 'o' , s = 50 , edgecolors='none')


    states = get_path_states(goal_node)
    paths = []
    
    for i in range(len(states)):
        paths.append(states[i][0])

    initial_pa = True

    for i in range(len(paths)):
        if initial_pa :
            after = paths.pop()
            plt.arrow(problem.initial_state[0][0],problem.initial_state[0][1] , (after[0] - problem.initial_state[0][0] ), (after[1] - problem.initial_state[0][1]) , color = 'magenta' , head_width = 0 )
            initial_pa = False 
            previous = after
        else:
            after = paths.pop()
            plt.arrow(previous[0] , previous[1], (after[0] - previous[0]) , (after[1] - previous[1]) , color = 'magenta' , head_width = 0 )
            previous = after 
        






    plt.savefig(file_name ,  format='png')
    plt.close()





class PriorityQueue:
     def __init__(self, items=(), priority_function=(lambda x: x)):
             self.priority_function = priority_function
             self.pqueue = []
             # add the items to the PQ
             for item in items:
                 self.add(item)
     """
     Add item to PQ with priority-value given by call to priority_function """
     def add(self, item):
         pair = (self.priority_function(item), item) 
         heapq.heappush(self.pqueue, pair)
     """
     pop and return item from PQ with min priority-value """
     def pop(self):
         return heapq.heappop(self.pqueue)[1]
     """
     gets number of items in PQ
     """
     def __len__(self):
         return len(self. pqueue)

