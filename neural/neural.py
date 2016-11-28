#! /usr/bin/env python
# -*- coding:utf-8 -*-

from random import gauss, randint, uniform, choice
import matplotlib.pyplot as plt



class Neuron :

    def __init__(self, state=0, trsh=0):
        self.state = state
        self.threshold = trsh

    def __repr__(self):
        return "State : "+str(self.state)+"\t Threshold : "+str(self.threshold)

    def signal_IN(self, weight_sum):
        if self.threshold <= weight_sum:
            self.state = 1
        else :
            self.state = -1

class Network :

    def __init__(self, initial_st, w_matrix=[]):

        self.neurons = []

        for st in initial_st :
            print st
            neu = Neuron(st[0],st[1])
            self.neurons.append(neu)

        self.weights = [[None for i in range(len(self.neurons))] for _ in range(len(self.neurons))]

        for i,a in enumerate(self.weights) :
            for j,b in enumerate(a):
                if i == j:
                    self.weights[i][j] = 0
                elif None == b:
                    b = gauss(0,1) if len(w_matrix)<=0 else w_matrix[i][j]
                    self.weights[i][j] = b
                    self.weights[j][i] = b

    def __repr__(self):

        out = ""
        for neu in self.neurons:
            out += neu.__repr__()+"\n"
        out+= "Energy :\t "+str(self.get_energy())+"\n____________________"
        return out

    def get_energy(self):
        e1 = 0
        e2 = 0
        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                e1 += self.weights[i][j]*self.neurons[i].state*self.neurons[j].state

        for neu in self.neurons :
            e2 += neu.threshold*neu.state

        return -0.5*e1+e2

    def update(self):
        i = randint(0,len(self.neurons)-1)

        weight_sum = 0
        for w in self.weights[i]:
            weight_sum += w*self.neurons[i].state

        self.neurons[i].signal_IN(weight_sum)
        #is_symetrical(self.weights)

def make_weight(patterns):
    matrix = [[0]*len(patterns[0]) for _ in range(len(patterns[0]))]

    for pattern in patterns:
        for i in range(len(pattern)):
            for j in range(len(pattern)):
                if i == j:
                    matrix[i][j] = 0
                elif j <= i :
                    b = 1/len(patterns)*(pattern[i]*pattern[j])
                    matrix[i][j] += b
                    matrix[j][i] += b
    return matrix

def is_symetrical(matrix):
    for i,a in enumerate(matrix) :
        for j,b in enumerate(matrix[i]):
            if matrix[i][j] != matrix[j][i]:
                print "\n\nERROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOR\n\n"



#On peut noter que l'on converge rapidement à un état d'équilibre


if __name__ == '__main__':

    input_ = []
 
    patterns =[[-1,1,1,-1]]
    # patterns=[[ -1,  1,  1,  1, -1, 
    #             -1,  1, -1, -1, -1,
    #             -1,  1,  1,  1, -1,
    #             -1,  1, -1,  1, -1,
    #             -1,  1,  1,  1, -1]]
    for it in range(5):
        a = [uniform(-0.5,0.5),0]#uniform(-1,1))
        input_.append(a)
    print input_

    matrix = make_weight(patterns)
    #for i in matrix:
    #    print i

    test = Network(input_)#, w_matrix = matrix)
    #print test 
    plt.ion()

    #for a in test.weights:
    #    print a

    eng = [0]
    i = 0
    t=[]
    en = []
    while len(eng) <= 30:

        if eng[0] != test.get_energy():
            eng= [test.get_energy()]
        else :
            eng.append(test.get_energy())
        t.append(i)
        en.append(test.get_energy())
        #plt.scatter(i,test.get_energy()
        plt.plot(t,en, color='blue')
        plt.pause(0.01)
        
        
        test.update()
        print test

        i+=1


    while True:
        plt.pause(0.01)



    print test
 
    
    

#patterns[0][it],0)#
