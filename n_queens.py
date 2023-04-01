# mhmdjavad safi
# solving n queens using genetic algorithm
# coding at 5 farvardin 1402
# IMPORT:
import random
import matplotlib.pyplot as plt
import numpy as np
from numba import jit
from copy import deepcopy

#-------------------------
# CONSTANTS AND VARIABLES:
N = 20
POPULATION_SIZE = 50
MUTATION_RATE = 0.8
# indexes are from 0 to n-1: are the possible locations


def init_population():
    return np.random.randint(N, size=(POPULATION_SIZE*2, N+1))

@jit
def cross_over(population):
    half = N//2
    for i in range(0, POPULATION_SIZE, 2):
        population[POPULATION_SIZE+i][:half] = population[i][:half]
        population[POPULATION_SIZE+i][half:N] = population[i+1][half:N]
        population[POPULATION_SIZE + i+1][:half] = population[i+1][:half]
        population[POPULATION_SIZE + i+1][half:N] = population[i][half:N]
    return population

@jit
def mutation(population):
    chosen_ones = np.random.randint(POPULATION_SIZE,POPULATION_SIZE*2,size=(1,int(POPULATION_SIZE*MUTATION_RATE)))
    x = N-1
    for i in chosen_ones[0]:
        cell = random.randint(0, x)
        value = random.randint(0, x)
        population[i][cell] = value
    return population

@jit
def fitness(population):
    for individual in population:
        crashes = 0
        #print(individual)
        for i in range(0,N):
            for j in range(i+1,N):
                if individual[i] == individual[j]:
                    #print("vertical : ",i , " ",j)
                    crashes += 1
                if abs(i-j) == abs(individual[i]-individual[j]):
                    crashes += 1
                    #print("diagonal : ", i , " ", j)
        individual[-1] = crashes
    return population


def print_population(population):
    print(population)
    print("------end-------")

def show(solution):
    #plt.figure(figsize=(5,5))
    for i in range(N+1):
        plt.plot([0,N*2],[i*2,i*2])
        plt.plot([i*2,i*2],[0,N*2])
    for i in range(N):
        plt.scatter([i*2+1],solution[i]*2+1)
    plt.show()



POPULATION = init_population()
count = 1
while(True):
    POPULATION = cross_over(deepcopy(POPULATION))
    POPULATION = mutation(deepcopy(POPULATION))
    POPULATION = fitness(deepcopy(POPULATION))

    # sorting
    POPULATION = deepcopy(POPULATION)[deepcopy(POPULATION)[:,-1].argsort()]

    if POPULATION[0][-1] == 0:
        print("answer : ",POPULATION[0][:N])
        print_population(POPULATION[0])
        break
    print(count,"_ ",POPULATION[0][-1])
    count += 1
