#! /usr/bin/env python
#-*- coding:utf-8 -*-

from random import randint, gauss


class Perceptron:
  """docstring for Perceptron"""
  def __init__(self, dataset, b, alpha):
    
    self.alpha = alpha
    self.b = b
    self.dataset = dataset
    self.wm = [[gauss(0,self.b) for _ in range(len(self.dataset[0])-1)] for _ in range(len(self.dataset))]
    self.bin = [None]*len(self.dataset)

    self.assign_bin()

  def assign_bin(self):
    for i, elt in enumerate(self.dataset):
      s_w = 0
      for j, dim in enumerate(elt) :
        if dim != elt[-1]:
          s_w += dim*self.wm[i][j]
      self.bin[i] = 1 if s_w > 0 else -1

  def compute_weights(self):
    for i, elt in enumerate(self.dataset):
      gam = self.bin[i]
      y = elt[-1]
      for j, dim in enumerate(elt):
        if dim != elt[-1]:
          self.wm[i][j] += self.alpha*(y-gam)*dim




if __name__ == '__main__':
  

  my_dataset =  [[1,2,3,-1],[2,4,3,-1],[4,5,6,1],[8,9,4,1],[1,2,3,-1],[2,4,3,-1],[4,5,6,1],[8,9,4,1],[1,2,3,-1],[2,4,3,-1],[4,5,6,1],[8,9,4,1]]

  test = Perceptron(my_dataset, 0.1, 0.3)
  print test.wm
  print test.bin
  for i in range(5):
    test.compute_weights()
    test.assign_bin()
    print test.wm
    print test.bin
    