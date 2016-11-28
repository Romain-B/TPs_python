#! /usr/bin/env python
# -*- coding:utf-8 -*-


import random 
from numpy.random import choice
import matplotlib.pyplot as plt
from copy import copy


class Agent:
    def __init__(self, x,y, state):
	
		self.x = x
		self.y = y
		self.state = state
	
    def move(self, evt):
		if self.state != 'M':
			(new_x,new_y) = self.check_dir(evt, copy(self.x),copy(self.y))	
			while (new_x,new_y) in evt.obs :
				(new_x,new_y) = self.check_dir(evt, copy(self.x),copy(self.y))

			self.x = new_x
			self.y = new_y

    def check_dir(self, evt, new_x, new_y):

		dir = random.randint(1,5)
		if dir == 1:
			new_x = new_x+1 if new_x+1 < evt.w else 0
		if dir == 2:
			new_x = new_x-1 if new_x-1 > 0 else evt.w-1
		if dir == 3:
			new_y = new_y+1 if new_y+1 < evt.h else 0
		if dir == 4:
			new_y = new_y-1 if new_y-1 > 0 else evt.h-1

		return new_x,new_y


	
    def update(self, evt) :
		if self.state == 'I' :
			self.state = choice(['I','R','M'],1,p=[1-evt.pr-evt.pm,evt.pr,evt.pm])[0]
			
class Envir:
	def __init__(self, w,h, nb, prop, pi, pr, pm, obs=[]):
			
		nb_i = int(nb*prop)

		self.w = w
		self.h = h
		self.pop = []
		self.pi = pi
		self.pr = pr
		self.pm = pm
		self.step = 0
		self.obs = obs

			#pi, pr et pm sont ici car on donne les mêmes à tous les agents donc 
			#pour éviter de stocker 1000x les mêmes valeurs ils sont dans l'environnement.
	
		for i in range(nb):
			x = random.randint(0, w-1)
			y = random.randint(0, h-1)
			while (x,y) in self.obs :
				x = random.randint(0, w-1)
				y = random.randint(0, h-1)
			if nb_i > 0:
				state = 'I'
				nb_i -= 1
			else :
				state = 'S'

			agt = Agent(x, y, state)
			self.pop.append(agt)
	
	def move(self):
		for agt in self.pop:
		    	agt.move(self)
	
	def contact(self):
		grid = [[[] for _ in range(self.w)] for _ in range(self.h)]
		for agt in self.pop:
				grid[agt.x][agt.y].append(agt)
		return grid

	
	def infect(self, grid):
		for x in grid :
			for y in x:
				nb_I = 0
				agt_S = []
        		for agt in y :

					if agt.state == 'I':
						nb_I += 1

					if agt.state == 'S':
						agt_S.append(agt)

					else:
						agt.update(self)
					
					for agt_s in agt_S :
						a = 1-nb_I*self.pi if 1-nb_I*self.pi>=0 else 0
						b = nb_I*self.pi if nb_I*self.pi<=1 else 1
						#if a != 1 and b !=1 :
						agt_s.state = choice(['S','I'], 1, p=[a, b])[0] 
						#else:
							#agt_s.state = 'S' if a==1 else 'I'
						#print "State : ", agt_s.state, " PS : ", a," PI : ", b
						

	def run(self, steps=1):
		for i in range(steps):
			self.infect(self.contact())
			self.move()
			self.step += 1

	def stats(self):
		s_agt = []
		i_agt = []
		r_agt = []
		m_agt = []

		for agt in self.pop:
			if (agt.x, agt.y) in self.obs:
				print "PAS BON"
			if agt.state == 'S':
				s_agt.append(agt)
			elif agt.state == 'I':
				i_agt.append(agt)
			elif agt.state == 'R':
				r_agt.append(agt)
			elif agt.state == 'M':
				m_agt.append(agt)
		return {'SAINS':len(s_agt), 'INFECTES':len(i_agt), 'RESISTANTS':len(r_agt), 'MORT': len(m_agt), 'STEP':self.step}

if __name__ == '__main__':
											
    obs = []
    for i in range(100):
        obs.append((75,i))
        obs.append((50,i))
        obs.append((25,i))
    #del obs[50]

    test = Envir(100,100,1000, 0.2,1, 0.01, 0.001, obs=obs)
    save = {"SAINS" : [test.stats()['SAINS']],"INFECTES" : [test.stats()['INFECTES']],"RESISTANTS" : [test.stats()['RESISTANTS']],"MORT" : [test.stats()['MORT']],"STEP" : [test.stats()['STEP']]}
    it = 0
    for i in range(10000):
        test.run()
        it +=1
        if it>=20:
            for key in save.keys():
                save[key].append(test.stats()[key])
	    	#save['SAINS'].append(test.stats()['SAINS'])
	    	#save['INFECTES'].append(test.stats()['INFECTES'])
	    	#save['RESISTANTS'].append(test.stats()['RESISTANTS'])
	    	#save['MORT'].append(test.stats()['MORT'])
	    	#save['STEP'].append(test.stats()['STEP'])
            it = 0
	#for agt in test.pop:
    #        print "X: ",agt.x,", Y: ",agt.y
    #       if agt.x == 50 :
    #            print "HERE!"

    plt.plot(save['STEP'],save['SAINS'], label='Sains')
    plt.plot(save['STEP'],save['INFECTES'], label='Infectes')
    plt.plot(save['STEP'],save['RESISTANTS'], label='Resistants')
    plt.plot(save['STEP'],save['MORT'], label='Morts')
				
    plt.show()


