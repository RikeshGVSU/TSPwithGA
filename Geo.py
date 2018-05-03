
import random
import numpy as np
from tkinter import *
import time
import math
import timeit
from math import sin, cos, sqrt, atan2, radians;
import pandas as pd

start = timeit.default_timer()
bestOrder = []
number_of_generations = 100
numberOfPopulation = 10000
mutationRate = 0.2
file="latlong1.csv"
a=[]

def distance_calculator(lat_first,long_first,lat_second,long_second):

        R = 6373.0
        lat_first=radians(lat_first);
        long_first=radians(long_first);
        lat_second=radians(lat_second);
        long_second=radians(long_second);
        diff_lon = long_second - long_first
        diff_lat = lat_second  - lat_first

        a = sin(diff_lat / 2)**2 + cos(lat_first) * cos(lat_second) * sin(diff_lon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance=R*c;
        return distance;
        

 
def distance_matrix(latitude,longitude):
    '''returns the matrix of distance between different cities'''
    for i in range(len(latitude)):
        b=[]
        for j in range (len(latitude)):
            b.append(distance_calculator(latitude[i],longitude[i],latitude[j],longitude[j]))
        a.append(b)

    return a





input=pd.read_csv(file);
input_df = pd.DataFrame(input);
latitude_a = input_df['latitude'];
longitude_a = input_df['longitude'];
city_a=input_df['city']


matrix = distance_matrix(latitude_a,longitude_a);
totalDestinations = len(input_df);

population = []
for i in range(numberOfPopulation):
    population.append(random.sample(range(0, totalDestinations), totalDestinations))
 
generation = 0
currentBest = math.inf

    
    
def runAlgorithm(population):
    fitnessScore = []
    global currentBest
    global generation
    global bestOrder
    generation = generation + 1
    
    
    for j in range(numberOfPopulation):
        distance = 0
        order = population[j]
        for i in range(len(order)):
            p = order[i]
            if (i != 0):
                q = order[i-1]                               
                distance = distance + matrix[p][q]
        fitnessScore.append(1/(distance +1))
        
        if (distance < currentBest):
            currentBest = distance
            bestOrder = order
            df_2=[]
            for i in bestOrder:
                
                df_3=(latitude_a[i],longitude_a[i],city_a[i]);
                df_2.append(df_3)

            output_dataframe=pd.DataFrame(data=df_2,columns=["latitude","longitude","city"]);
            output_dataframe.to_csv('output6.csv', sep=",",encoding='utf-8', index=False)
            
        if(generation == number_of_generations and j == numberOfPopulation - 1): #print the final result
            print(bestOrder)
            df_2=[]
            for i in bestOrder:
                print(city_a[i],i);
                df_3=(latitude_a[i],longitude_a[i],city_a[i]);
                df_2.append(df_3)

            output_dataframe=pd.DataFrame(data=df_2,columns=["latitude","longitude","city"]);
            output_dataframe.to_csv('output6.csv', sep=",",encoding='utf-8', index=False)
                
            # print(input_df[bestOrder])

        
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
        for k in range(random.randint(50,500)):
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


    


