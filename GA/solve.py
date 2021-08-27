import numpy as np
from geneticalgorithm import geneticalgorithm as ga
from data_processing import MyPreprocessor
from typing import *

class ServiceComposition:
    def __init__(self, services: List[str], fitness_func_value: float):
        self.services = services
        self.fitness_func_value = fitness_func_value

class GASolver:
    def __init__(self, file, cost_percent, reliability_percent, performance_percent, availability_percent):
        self.cost_weight = cost_percent
        self.reliability_weight = reliability_percent
        self.performance_weight = performance_percent
        self.availability_weight = availability_percent 

        self.p1 = MyPreprocessor()
        self.p1.preprocess(file)
        
        # calculate sum of max costs for each category and sum of max time for each category. 
        self.sum_of_max_cost_per_cat = sum(self.p1.max_cost_for_each_cat)
        self.sum_of_max_performance_per_cat = sum(self.p1.max_performance_for_each_cat)

        
    # fitness function 
    def fitness(self,chromosome):
        chromosome = chromosome.astype(int)

        fc = self.getfc(chromosome)
        fp = self.getfp(chromosome)
        fr = self.getfr(chromosome) 
        fa = self.getfa(chromosome) 

        fitness = fc * self.cost_weight + fr * self.reliability_weight + fp * self.performance_weight + fa * self.availability_weight
        return -fitness # return -fitness so the function is maximized. geneticalgorithm library is designed to minimize the function 

    def getfc(self,chromosome):
        sum_of_cost = 0
        count = 1
        for gene in chromosome:
            string_for_dict = "S" + str(count) + str(gene) + "cost"
            count +=1 
            cost = self.p1.service_dict[string_for_dict]
            sum_of_cost += cost
        division_result = sum_of_cost / self.sum_of_max_cost_per_cat
        fc = 1 - division_result 
        return fc

    def getfp(self,chromosome):
        sum_of_time = 0
        count = 1
        for gene in chromosome:
            string_for_dict = "S" + str(count) + str(gene) + "time"
            count +=1 
            time = self.p1.service_dict[string_for_dict]
            sum_of_time += time
        division_result = sum_of_time / self.sum_of_max_performance_per_cat
        fp = 1 - division_result
        return fp

    def getfr(self,chromosome):

        # fr_1 is fr(s1x -> s2x -> s3x)
        count = 1
        fr_1 = 1

        for gene in chromosome:
            string_for_dict = "S" + str(count) + str(gene) + "reliability"
            reliability = self.p1.service_dict[string_for_dict]
            fr_1 *= reliability
            count+=1
        
        path = [1,3]
        #fr_2 is fr(s1x -> s3x)
        fr_2 = 1
        for val in path:
            string_for_dict = "S" + str(val) + str(chromosome[val-1]) + "reliability"
            reliability = self.p1.service_dict[string_for_dict]
            fr_2 *= reliability
        
        fr = min(fr_1,fr_2)
        return fr

    def getfa(self,chromosome):

        # fa_1 is fa(s1x -> s2x -> s3x)
        count = 1
        fa_1 = 1

        for gene in chromosome:
            string_for_dict = "S" + str(count) + str(gene) + "availability"
            availability = self.p1.service_dict[string_for_dict]
            fa_1 *= availability
            count+=1
        
        path = [1,3]
        #fa_2 is fa(s1x -> s3x)
        fa_2 = 1
        for val in path:
            string_for_dict = "S" + str(val) + str(chromosome[val-1]) + "availability"
            availability = self.p1.service_dict[string_for_dict]
            fa_2 *= availability
        
        fa = min(fa_1,fa_2)
        return fa

# function that takes the sample csv input file as an argument and runs the Genetic Algorithm 
def run(csv_file, weights=None) -> ServiceComposition:
    if weights == None:
        GASolver1 = GASolver(csv_file, 0.35,0.1,0.2,0.35)
    else:
        GASolver1 = GASolver(csv_file, *weights)

    varbound=np.array(GASolver1.p1.service_range_for_each_cat)

    algorithm_param = {'max_num_iteration': 100,\
                    'population_size':50,\
                    'mutation_probability':0.1,\
                    'elit_ratio': 0.02,\
                    'crossover_probability': 0.5,\
                    'parents_portion': 0.3,\
                    'crossover_type':'uniform',\
                    'max_iteration_without_improv':None}

    model=ga(function=GASolver1.fitness,dimension=GASolver1.p1.num_cats,variable_type = "int",variable_boundaries=varbound, algorithm_parameters=algorithm_param, convergence_curve = False, progress_bar=False)

    model.run() 

    results = model.best_variable.astype(str)
    for i in range(GASolver1.p1.num_cats):
        results[i] = "S" + str(i+1) + (results[i][:-2]) 

    print("\n")
    print("RESULTS")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("composition of services: ", results)
    final_fitness = -1 * model.best_function
    print("Fitness function value", final_fitness)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("\n")

    sc: ServiceComposition = ServiceComposition(list(results), final_fitness)
    return sc

# run the function that accepts a CSV to see the resulting recommended composition of services and the fitness function value 
if __name__ == "__main__":
    run('Data_saved_3.csv')