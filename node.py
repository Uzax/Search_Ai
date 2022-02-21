#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 22:32:05 2022

@author: zayed
"""

class Node (object) : 
    def __init__(self , state, parent_node=None,action_from_parent=None,path_cost=0):
        self.state = state 
        self.parent_node = parent_node
        self.action_from_parent = action_from_parent
        self.path_cost = path_cost 
        self.depth = 0
        if parent_node:
            self.depth = parent_node.depth + 1 
            
    def __lt__ (self, other) : 
        return self.state < other.state
    