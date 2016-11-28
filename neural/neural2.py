#! /usr/bin/env python
# -*- coding:utf-8 -*-

from random import gauss, randint
import matplotlib.pyplot as plt
from time import sleep


class Neuron:
    """docstring for Neuron"""
    def __init__(self, state, threshold):
        self.threshold = threshold
        self.state = state

    def signal(self, weight_sum):
        if self.threshold <= weight_sum:
            self.state = 1
        else :
            self.state = -1

class Network:
    """docstring for Network"""
    def __init__(self, initial_states, thresholds, weight_matrix=[]):

        self.neurons = []
        for i,state in enumerate(initial_states) :
            self.neurons.append(Neuron(initial_states[i],thresholds[i]))
        
        

        if 0 >= len(weight_matrix):
            self.weight_matrix = [[None for _ in self.neurons] for _ in self.neurons]
            for i, row in enumerate(self.weight_matrix):
                for j, column in enumerate(row):
                    if i == j:
                        self.weight_matrix[i][j]=0
                    elif None is column :
                        temp = gauss(0,1)
                        self.weight_matrix[i][j] = temp
                        self.weight_matrix[j][i] = temp
        else :
            self.weight_matrix = weight_matrix

    def __repr__(self):
        out=""
        i = 0
        while i < 25:
            for j in range(5):
                out += "." if 1 == self.neurons[i+j].state else "O"
                
            i+=5
            out+="\n"
        return out

    def update(self):
        i = randint(0, len(self.neurons)-1)
        weight_sum = 0

        for j, val in enumerate(self.weight_matrix[i]):
            weight_sum += val*self.neurons[j].state

        print "neurone :",i,"ws :",weight_sum

        self.neurons[i].signal(weight_sum)

    def get_energy(self):
        e1 = 0
        e2 = 0

        for i, row in enumerate(self.weight_matrix):
            for j, column in enumerate(row):
                e1 += column*self.neurons[j].state*self.neurons[i].state

        for neuron in self.neurons:
            e2 += neuron.state * neuron.threshold

        return -0.5*e1+e2

def make_weight(patterns):
    matrix = [[0]*len(patterns[0]) for _ in range(len(patterns[0]))]

    for pattern in patterns:
        for i in range(len(pattern)):
            for j in range(len(pattern)):
                if i == j:
                    matrix[i][j] = 0
                elif j <= i :
                    a = 1.0/len(patterns)
                    b = a*(pattern[i]*pattern[j])

                    matrix[i][j] += b
                    matrix[j][i] += b
        


    return matrix

if __name__ == '__main__':
    
    initial_states = [0]*25
    thresholds = [0]*25

    patterns=[[ -1,  1,  1,  1, -1, 
                -1,  1, -1, -1, -1,
                -1,  1,  1,  1, -1,
                -1,  1, -1,  1, -1,
                -1,  1,  1,  1, -1],
              [ -1,  1,  1,  1, -1,
                -1, -1, -1,  1, -1,
                -1, -1,  1, -1, -1,
                -1, -1, -1,  1, -1,
                -1,  1,  1,  1, -1]]
    #patterns =  [[1,-1,-1,1]]

    weight_matrix = make_weight(patterns)

    net = Network(initial_states, thresholds, weight_matrix)

    #plt.ion()

    eng = []
    a = []
    testit =0
    #for testit in range(100):
    while True:
        #print weight_matrix
        # for neu in net.neurons:
        #     print neu.state
        eng.append(net.get_energy())
        a.append(testit)

        sleep(0.05)
        
        #plt.plot(a,eng,color='blue')
        #plt.pause(0.01)

        net.update()
        print "\n"
        print net
        print "je suis un séparateur"
        testit += 1


    #while True:
        #plt.pause(0.01)

