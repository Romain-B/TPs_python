#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import numpy as np
from random import randint, gauss
import matplotlib.pyplot as plt

class Cluster:
  """docstring for Cluster
  This class inputs a 2D array of data and a desired number of clusters 
  and assigns the clusters using euclidian means.

  Usage :
      mycluster = Cluster(dataset, 3)

  """
  
  def __init__(self, dataset, n_cluster):
      
    self.dataset = dataset
    for i,row in enumerate(self.dataset) :

      if len(row) <= 0:
        del self.dataset[i]

    self.ccp = len(self.dataset[0]) #cluster id column position

    self.centroid = []

    for _ in range(n_cluster):
      centro = []
      for i, dimension in enumerate(self.dataset[0]):
        centro.append(self.dataset[randint(0,len(self.dataset)-1)][i])
      self.centroid.append(centro)

    for row in self.dataset :
      row.append(-1)

    self.assign_cluster()

  def assign_cluster(self):
    """
    For each individual, computes euclidan distance to each centroid,
    assigning the closest one.

    Returns the sum of all distances to centroids
    """

    sum_dists = 0
    for ind in self.dataset :
      dists = []
      for centro in self.centroid :
        dist = 0
        for i, val in enumerate(ind) :
          if i < self.ccp :
            dist += (centro[i]-val)**2
        dists.append(dist)

      ind[self.ccp] = dists.index(min(dists))
      sum_dists += min(dists)

    return sum_dists


  def update_centroids(self):
    """
    Recomputes coordinates for the centroid according 
    to the arithmetic mean of the individuals assigned to it.
    """

    #switches columns and lines WITHOUT moving the data.
    #(for easier manipulation of each dimension)
    reverse_dataset = switch_array(self.dataset)
    
    for f, centro in enumerate(self.centroid):
      means = []    
      for col_n, col in enumerate(reverse_dataset):
        if col_n != self.ccp :
          vals = []
          for i, val in enumerate(col):
            if f == reverse_dataset[self.ccp][i]:
              vals.append(val)

        #If there are no values assigned to a cluster, random coordinates
        #are given to try and get a better position.
        means.append(np.mean(vals) if len(vals)> 0 else gauss(0,1))
      self.centroid[f] = means

  def converge(self):
    """
    Updates and assigns clusters up to convergence (sum of distances stabilizes).
    """

    sum_dists = 0
    last_sum_dist = 1
    i = 0
    
    while sum_dists != last_sum_dist :

      last_sum_dist = sum_dists

      sum_dists = self.assign_cluster()
      self.update_centroids()

      i += 1
      print "SUM_DISTS :\t", sum_dists
      raw_input("\n("+str(i)+") Press Enter...\n")



def switch_array(arr):
  """
  Switches the lines and columns without changing the data.
  Takes in argument a 2D array. Ex :

  [[1,2,3],       [[1,4,7],
   [4,5,6],  ==>   [2,5,8],
   [7,8,9]]        [3,6,9]]
   
  """
  new_arr = np.array([[None]*len(arr)]*len(arr[0]))
  for x, row in enumerate(arr) :
    for y, column in enumerate(row):
      new_arr[y,x] = column

  return new_arr


if __name__ == '__main__':

  dataset = []
  
  with open('iris.csv','rb') as ir_file:
    load = csv.reader(ir_file, delimiter=',')
    for row in load :
      if 0 <=len(row):
        dataset.append(row)

  #Tranfers the data to a numpy array      
  dataset = np.array(dataset)

  # Removes last column (string data)
  dataset = [row[:4] for row in dataset] 

  new_dataset = []
  for row in dataset :
    new_row = []
    for value in row :
      new_row.append(float(value))
    new_dataset.append(new_row)

  cluster = Cluster(new_dataset, 3)

  cluster.converge()







  