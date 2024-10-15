import pygame
import random
from car import *
from checkpoints import *

# Genetic algorithm wooo 
# Takes in the checkpoint manager, population
# Top performers that are kept and turned into parents of next generation
# Copies per top are exact copies with small changes
# Elitist percent is what percent of the path is changed. If it is .1 then only the last 10% is modified 
# Mutation rate is how common mutations are
# Cross over rate is how common crossover is
# Elitist percent crossover is the same but from crossover instead of mutations
class GeneticAlgorithm:
    def __init__(self, checkpoint_m, population_size=100, top_performers=5, copies_per_top =2, elitist_percent=.3, mutation_rate=.1, crossover_rate=.7, elitist_percent_crossover=.3):
        self.POP_SIZE = population_size
        self.MUTATION_RATE = mutation_rate
        self.CROSSOVER_RATE = crossover_rate
        self.TOP_PERFORMERS = top_performers
        self.COPIES_PER_TOP = copies_per_top
        self.ELITIST_PERCENT = elitist_percent
        self.checkpoint_manager = checkpoint_m
        self.ELITIST_PERCENT_CROSSOVER = elitist_percent_crossover
        

        self.generation = 1

    # First iteration, all random
    def start(self):
        return [AiCar(3, 2, self.checkpoint_manager) for _ in range(self.POP_SIZE)]

    # Finds the minimum length and then does a crossover that lies somewhere between the min length and Elitest % from the top
    # It then creates a child with the crossover where the primary parent is random
    def crossover(self, p1, p2):
        min_length = min(len(p1.path), len(p2.path))
        start = int(min_length * (1 - self.ELITIST_PERCENT_CROSSOVER))
        crossover_point = random.randint(start, min_length)
        if random.randint(0,1) == 0:
            child_path = p1.path[:crossover_point] + p2.path[crossover_point:min_length]
        else:
            child_path = p2.path[:crossover_point] + p1.path[crossover_point:min_length]
        return child_path

    # Given a path, it finds the possibilities where mutations are possible (elitist percent) then if the random number meets the mutation rate
    # Then it changes the path
    def mutate(self, path):
        mutated_path = path.copy()
        path_length = len(mutated_path)
        mutation_start = int(path_length * (1 - self.ELITIST_PERCENT))
        
        for i in range(mutation_start, path_length):
            if random.random() < self.MUTATION_RATE:
                mutated_path[i] = random.choice(AiCar.MOVES)
        
        return mutated_path

    # Creates the next gen
    def create_next_generation(self, top_cars):
        next_generation = []
        
        # For all the top cars, it creates a copy then for every COPY PER TOP, it creates another clone but mutates the end of the path
        for car in top_cars:
            new_car = AiCar(3, 2, self.checkpoint_manager)
            new_car.path = car.path.copy()
            next_generation.append(new_car)
            for _ in range(self.COPIES_PER_TOP):
                mutated_car = AiCar(3, 2, self.checkpoint_manager)
                mutated_car.path = self.mutate(car.path)
                next_generation.append(mutated_car)
        
        # For the rest of the generation, it selects 2 random parents from top cars and then does crossover (based on rate) or mutates it 
        while len(next_generation) < self.POP_SIZE:
            parent1, parent2 = random.choices(top_cars, k=2)
            
            if random.random() < self.CROSSOVER_RATE:
                child_path = self.crossover(parent1, parent2)
            else:
                child_path = random.choice([parent1, parent2]).path.copy()
            
            child_path = self.mutate(child_path)
            
            child_car = AiCar(3, 2, self.checkpoint_manager)
            child_car.path = child_path
            next_generation.append(child_car)
        
        return next_generation
