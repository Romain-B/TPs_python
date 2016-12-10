#! /usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
from random import randint
from copy import copy

class Environnement:
  """docstring for Environnement"""
  def __init__(self, dic, end_st, igrid):
    
    self.case_types = dic
    self.end_state = end_st
    self.grid = np.array(igrid)

  def case_possible(self, direct, pos):
    # 0,N | 1,S | 2,E | 3,W
    modx = 0
    mody = 0

    if 1 >= direct:
      mody = 1 if 0 == direct else -1
    else :
      modx = 1 if 2 == direct else -1
    x = pos[0] + modx
    y = pos[1] + mody

    if (x >= len(self.grid[0])) or (x < 0) or (y >= len(self.grid)) or (y < 0) or (None == self.grid[y,x]):
      return False
    return x,y

  def case_end(self, pos):
    if self.grid[pos[1],pos[0]] in self.end_state :
      return True
    return False

  def get_type(self, pos):
    return self.grid[pos[1],pos[0]]

    
class Platypus:
  """docstring for Platypus"""

  def __init__(self, ga, env):
    
    self.ga = ga
    self.state = (0,0) #x,y, donc grid[state[1]][state[0]] pour atteindre la case (x,y)
    self.env = env
    self.t = 0

    self.utility = np.array([[(0.0,0.0,0.0,0.0) for _ in range(len(self.env.grid[0]))] for _ in range(len(self.env.grid))])
    self.hdd = [[([],[],[],[]) for _ in range(len(self.env.grid[0]))] for _ in range(len(self.env.grid))] #Memory

    self.training_routes = []

  def move(self, direct = 6):
    
    a = False
    if direct == 6 :
      direct = randint(0,3)
      a = True
      while False == self.env.case_possible(direct, self.state):
        direct = randint(0,3)
    #else:
      #print "[move] Direct : ",direct
      #print "[move] pos BEFORE : ", self.state

    self.state = self.env.case_possible(direct, self.state)
    #print "[move] pos AFTER : ", self.state

    if a == True :
      self.save_path(direct)


  def save_path(self, direct):
    if self.t == len(self.training_routes):
      self.training_routes.append([])

    self.training_routes[self.t].append((self.state,self.env.case_types[self.env.grid[self.state[1],self.state[0]]],direct))

  def save_to_hdd(self):
    for i, step in enumerate(self.training_routes[self.t]):
      moy = 0
      for j in range(i, len(self.training_routes[self.t])):
        moy += self.training_routes[self.t][j][1]*pow(self.ga,i)
      if moy != 0:
        self.hdd[step[0][1]][step[0][0]][step[2]].append(moy)

  def make_util(self):
    for y, row in enumerate(self.hdd) :
      for x, case in enumerate(row):
        for direction, arr_rew in enumerate(case):
          arr_rew = np.array(arr_rew)
          moy = 0
          for val in arr_rew:
            moy += val
          moy /= len(arr_rew) if len(arr_rew) != 0 else 1

          if moy != 0:
            if direction == 0:
              self.utility[y-1][x][direction] = copy(moy)
            elif direction == 1:
              self.utility[y+1][x][direction] = copy(moy)
            elif direction == 2:
              self.utility[y][x-1][direction] = copy(moy)
            elif direction == 3:
              self.utility[y][x+1][direction] = copy(moy)

  def train(self, n_train=1):
    for i in range(n_train):
      end = False 
      while (end != True) :
        self.move()
        self.save_to_hdd()
        end = self.env.case_end(self.state)

      self.make_util()
      self.t += 1
      self.state = (0,0)

  def run_after_training(self):
    end = False
    self.state = (0,0)
    route = "Route : "
    #p = self.best_choice()

    while (end != True):
      d = ""
      if self.best_choice() == 0:
        d = "up"
      elif self.best_choice() == 1:
        d = "do"
      elif self.best_choice() == 2:
        d = "ri"
      elif self.best_choice() == 3:
        d = "le"
      route += d+" ,"

      print "Pos :",self.state,"  Going : "+d
      self.move(direct = self.best_choice())
      
      end = self.env.case_end(self.state)


      

    route += " "+self.env.get_type(self.state)+" !"
    return route


  def best_choice(self):
    case = self.utility[self.state[1],self.state[0]]
    print case
    max_index = (0, -10)
    for i, direct in enumerate(case) :
      
      if direct >= max_index[1] and direct != 0:
        max_index = (i, direct)
    print max_index
    return max_index[0]



  def print_route(self):
    route = "Route : "
    for case in self.training_routes[self.t-1]:
      d = ""
      if case[2] == 0:
        d = "up"
      elif case[2] == 1:
        d = "do"
      elif case[2] == 2:
        d = "ri"
      elif case[2] == 3:
        d = "le"
      route += d+" ,"
    return route





    


if __name__ == '__main__':

  case_types = {"void":-0.04, "food":1, "trap":-1 }
  end_case = ["food","trap"]

  grid = [["void",None,"void","food"],
          ["void",None,"void","trap"],
          ["void","void","void","void"]]

  my_envir = Environnement(case_types, end_case, grid)

  print my_envir.grid

  my_platypus = Platypus(0.9, my_envir)
  my_platypus.train(500)


  while True :
    raw_input("\nPress Enter...\n")
    # my_platypus.move()
    # my_platypus.save_to_hdd()
    # my_platypus.make_util()*
    print "U  "
    for a in reversed(my_platypus.utility):
      print a


    print my_platypus.run_after_training()

    #print "Tr   ",my_platypus.training_routes

    print my_envir.grid