#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 14:22:53 2022

@author: eebjs
"""

import numpy as np
import pandas as pd
np.array

#%% what is a class

class Tree():
    def __init__(self, species, height, dbh):
        self.species = species
        self.height = height
        self.dbh = dbh    
        biomass_estimation_table = {'oak':(0.994, -2.944, 1.935, 0.738),
                                    'birch':(0.575, -2.575, 1.827, 0.823)}
        self.biomass_estimators = biomass_estimation_table[self.species]
        
    def __str__(self):
        return f'{self.species} tree of height {self.height}m and dbh {self.dbh}m'

    def estimate_biomass(self):
        #λ × exp(p0 + p1 × lnD + p2 × lnH)
        λ, p0, p1, p2 = self.biomass_estimators
        biomass = λ * np.exp(p0 + p1 * np.log(self.dbh) + p2 * np.log(self.height))
        return biomass

    def grow(self, percent):
        self.height = self.height * (1 + percent / 100)
        self.dbh = self.dbh * (1 + percent / 100)


class Forest():
    def __init__(self, trees):
        self.trees = trees
        # check if trees is a list of trees
        if not any(isinstance(t, Tree) for t in self.trees):
            raise TypeError('trees is not a list of Trees')
            

    def __getitem__(self, item):
        return self.trees[item]

    def add_tree(self, tree):
        self.trees.append(tree)
        
        
    
#%% create tree
tree = Tree(species='oak', height=10, dbh=2)
print(tree.estimate_biomass())
tree.grow(10)
print(tree.estimate_biomass())



#%% create forest

oak_tree = Tree(species='oak', height=10, dbh=2)
birch_tree = Tree(species='birch', height=5, dbh=.6)

forest = Forest(trees = [birch_tree, oak_tree])

#%% add more trees

tree_obs = pd.read_csv('./tree_obs.csv')

for ri, row in tree_obs.iterrows():
    
    tree = Tree(species=row['species'], height=row['h'], dbh=row['dbh'])
    
    forest.add_tree(tree)