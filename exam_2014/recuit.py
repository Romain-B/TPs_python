#! /usr/bin/env python
# -*- coding:utf-8 -*-

from random import gauss
from math import exp
from numpy.random import choice

class Recuit:
  """docstring for Recuit"""
  def __init__(self, par_tuple, s0):
    
    self.gamma = par_tuple[0]     #System parameter
    self.t = par_tuple[1]         #Temperature of system

    self.s = s0                   #System state
    self.e = self.fct_F(self.s)   #Energy of System 

  def __repr__(self):
    return "Temperature :\t"+str(self.t)+"\nEnergy :\t" +str(self.e)+"\nState :\t"+str(self.s)

  def fct_F(self,s):
    return s**2

  def fct_N(self):
    return self.s + gauss(0,1)

  def calc_p(self, new_e):
    if new_e < self.e :
      return 1
    else :
      p = exp((self.e - new_e)/self.t)
      return p 

  def system_update(self, it):
    print self

    for i in range(it):
      sn = self.fct_N()
      en = self.fct_F(sn)
      p = self.calc_p(en)

      updt = choice([True,False],1,p=[p,1-p])[0]

      if updt :
        self.s = sn
        self.e = en

      self.t = self.t*self.gamma
      print self






if __name__ == '__main__':
  test = Recuit((0.9,10), gauss(10,1)) #((gamma,t0),s0)

  test.system_update(5)