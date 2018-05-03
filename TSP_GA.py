#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 02:07:30 2018

Travelling Salesman Problem

@author: rikeshpuri
"""
import random
import numpy as np
from tkinter import *
import time
import math
import matplotlib.pyplot as plt
import timeit

start = timeit.default_timer()


bestOrder = []
totalDestinations = 50
number_of_generations = 200
numberOfPopulation = 20000
mutationRate = 0.01

population = []
for i in range(numberOfPopulation):
    population.append(random.sample(range(0, totalDestinations), totalDestinations))
 
destinations = np.random.randint(5,695, size=(totalDestinations, 2))
generation = 0
currentBest = math.inf

root= Tk()
canvas0 = Canvas(root, width = 700, height = 20)
canvas0.pack()
l = Label(canvas0)
l.pack()
canvas1 = Canvas(root, width = 700, height = 20)
canvas1.pack()
text1 = Label(canvas1, text = "Best Result ")
text1.pack()
canvas2 = Canvas(root, width = 700, height = 700)
canvas2.pack(side = BOTTOM)

''' for ploting the distance improvement graph'''
x_coord = []
y_coord = []   
    
def runAlgorithm(population):
    fitnessScore = []
    global currentBest
    global generation
    global bestOrder
    generation = generation + 1
    l.config(text = "Generation" + str(generation))
    root.update()
    for j in range(numberOfPopulation):
        distance = 0
        order = population[j]
        for i in range(len(order)):
            p = order[i]
            if (i != 0):
                q = order[i-1]
                x1 = destinations.item((q,0))
                y1 = destinations.item((q,1))
                x2 = destinations.item((p,0))
                y2 = destinations.item((p,1))
                
                distance = distance + math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        fitnessScore.append(1/(distance +1))
        
        if (distance < currentBest):
            currentBest = distance
            bestOrder = order
            
        if(generation == number_of_generations and j == numberOfPopulation - 1): #print the final result
            canvas2.delete('all')
            root.update()
            for i in range(len(order)):
                p = bestOrder[i]
                canvas2.create_circle(destinations.item((p,0)), destinations.item((p,1)), 3, fill="blue")
                if (i != 0):
                    q = bestOrder[i-1]
                    x_1 = destinations.item((q,0))
                    y_1 = destinations.item((q,1))
                    x_2 = destinations.item((p,0))
                    y_2 = destinations.item((p,1))
                    
                    linesBest = canvas2.create_line(x_1,y_1,x_2,y_2)
                    root.update()
                    
    ''' For ploting the distance improvement graph'''
    x_coord.append(generation)
    y_coord.append(currentBest)
        
    return fitnessScore
    
    
    
def _create_circle(self, x, y, r, **kwargs):
    ''' functtionn to draw node in Tkinter '''
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle



def normalizeFitness(fitnessScore):
    ''' This function normalizes the fitness score to be the value between 0 and 1 '''
    sum = 0
    fitness = []
    for i in fitnessScore:
        sum += i
    
    for i in fitnessScore:
         fitness.append(i/sum)
        
    return fitness

def rouletteSelection(fitness, population):
    ''' 
    Roulette Selection: gets a random value,
    substracts each fitness from it until the the value is <= 0 and gets the index.
    The index is used to create a new population
    '''
    newPopulation = []
    for j in range(numberOfPopulation):
        i = 0
        r = random.random()
        while (r > 0):
            r = r - fitness[i]
            i += 1
            
        i = i - 1
        newPopulation.append(population[i])
    return newPopulation
   
def tournamentSelection(fitness, population):
    ''' 
    Tournament Selection: Selects random genes from the population
    and takes the best amoungst and appends it in the new population
    '''
    newPopulation = []
    for j in range(numberOfPopulation):
        best = 0
        for k in range(random.randint(10,200)):
            i = random.randint(0,numberOfPopulation-1)
            if fitness[i] > best:
                best = fitness[i]
                x = population[i]
                
        newPopulation.append(x)
    return newPopulation
    
def crossOver(population):
    newPopulation = []
    for i in range(numberOfPopulation):
        r = random.randint(0,(totalDestinations//2)-1)
        order = []
        for j in range(totalDestinations//2-1):
            order.append(population[i][r])
            r = r+1
            
        for j in population[numberOfPopulation - i-1]:
            if j not in order:
                order.append(j)
        newPopulation.append(order)
    return newPopulation
            
def mutationR(population, mutationRate):
    ''' 
    This function takes a random node and swaps it with its neighbour
    '''
    for i in range(numberOfPopulation):
        if (random.random() < mutationRate):
            x = random.randint(0,(totalDestinations)-1)
            y = random.randint(0,(totalDestinations)-1)
            population[i][x] , population[i][y] = population[i][y] , population[i][x]
    return population
        
            
def mutationN(population, mutationRate):
    ''' 
    This function takes a random node and swaps it with its neighbour
    '''
    for i in range(numberOfPopulation):
        if (random.random() < mutationRate):
            x = random.randint(1,(totalDestinations)-1)
            y = x - 1
            population[i][x] , population[i][y] = population[i][y] , population[i][x]
    return population
        
        


for i in range(number_of_generations):
    fitnessScore = runAlgorithm(population)
    fitness = normalizeFitness(fitnessScore)
    population = tournamentSelection(fitness, population)
    population = crossOver(population)
    population = mutationN(population, mutationRate)

stop = timeit.default_timer()
print (stop - start)

dist_graph = plt.plot(x_coord, y_coord, 'co')
plt.axis([0, max(x_coord), 0, max(y_coord)])
plt.xlabel('Generations')
plt.ylabel('Distance')
plt.show()

root.mainloop()

    


''' 
Ref: https://stackoverflow.com/questions/17985216/draw-circle-in-tkinter-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
Ref: https://www.youtube.com/watch?v=M3KTWnTrU_c
Ref: https://github.com/CodingTrain/Rainbow-Topics/issues/146
http://tributary.io/inlet/4101682/
https://arxiv.org/pdf/1402.4699.pdf
'''