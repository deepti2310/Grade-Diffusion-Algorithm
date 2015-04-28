import random
import operator
import copy
class FNRGeneticAlgorithm(object):

    def __init__(self, failed_sensor_nodes = [], nodes_info = {}, population_size = 10,  ):
        self.failed_sensor_nodes = failed_sensor_nodes
        self.sensor_nodes_info = nodes_info
        self.population_size = population_size
        self.current_population = []
        self.elitism_constant = int(population_size/2)


    def __initialize(self):
        for i in range(self.population_size):
            chromosome = []
            for j in range(len(self.failed_sensor_nodes)):
                chromosome.append(random.randint(0,1))
            self.current_population.append(chromosome)
    
    
    def __calculate_fitness_function(self, chromosome):
        """
        Implemeting some dummy fitness function
        2*x1 - 2.x2 + 3*x3 + 4*x4 - 5*x5 +2*x6 - 3*x7 + 4*x8 + 9*x9 + 10*x10
        input = [1,1,0,1,0,1,1,1,1,1]
        output = 2*1 -2*1 + 3*0+4*1-5*0+2*1-3*1+4*1+9*1+10*1 = 2-2+0+4-0+2-3+4+9+10=26
        """
        #fitness value shouldnt be a negative number
        factors_list = [2,-2,30,-4,5,2,-3,4,-9,10]
        s=sum([i*j for i,j in zip(chromosome, factors_list)])
        if s>0:
            return tuple(chromosome), s
        else:
            return tuple(chromosome), 0

                
    def __evaluation(self):
        pass

    
    def __crossover(self,pair):
        #select a point between first and last gen of a parent
        first, second = pair[0], pair[1]
        #i dont need to cross over at the beginning and at the end, as we are already having them in our new generation (remember elitism)
        p = random.randint(1, len(first)-1)
        f_0, f_1 = first[:p], first[p:]
        s_0, s_1 = second[:p], second[p:]
        new_pair = f_0+s_1, s_0+f_1
        return new_pair
    
    def __mutation(self, chromosome):
        #take length
        chromosome=list(chromosome)
        l = len(chromosome)
        rand_gene = random.randint(0,l-1)
        chromosome[rand_gene]=1-chromosome[rand_gene] #flip it
        return chromosome
    
    def __calculate_pdf(self, population):
        # calculate sigma of fitness values over the population
        sigma_f = sum([i[1] for i in population])
        #now calculate the probabilities
        p_i=[]
        for chromosome,fitness in population:
            prob = fitness*1.0/sigma_f
            p_i.append((chromosome, prob))
        last_prob = 1-sum([p for c,p in p_i[:-1]]) #just to make sure to correct rounding off errors while working wiht floats in a typical programming language
        p_i[-1]=p_i[-1][0],last_prob
        #now calculate the pdf for p
        pdf_i=[]
        for i,(chromosome, prob) in enumerate(p_i):
            if i == 0:
                pdf_i.append((chromosome, prob))
            else:
                pdf_i.append((chromosome, sum([j[1] for j in p_i[:i+1]])))
        return pdf_i
           
    def __select_pair(self, pdf):
        first, second = random.random(), random.random()
        f,s=None,None
        #iterate over pdf
        for chromosome, p in pdf:
            if first <= p and f is None:
                f = chromosome
            if second <=p and s is None:
                s = chromosome
        return f,s
    def selection(self, population = [], strategy = 'elitism', records=1, ):
        # popupation is a list of tuples, each tuple  contains  a chromosome and its fitness score
        population = copy.deepcopy(population)
        population=sorted(population, key = lambda item: item[1], reverse = True)
        
        if strategy == 'elitism':
            new_population= [list(i[0]) for i in population[0:records]]
            print len(new_population)
            return new_population
        elif strategy == 'roulette wheel':
            new_population=[]
            pdf_i=self.__calculate_pdf(population)
            for i in range(0,self.population_size-self.elitism_constant,2):
                #select pair of chromosomes
                pair = self.__select_pair(pdf_i)
                crossover_pair = self.__crossover(pair)  
                for i in crossover_pair:
                    n=self.__mutation(i)
                    new_population.append(n)
            print len(new_population[:records])
            return new_population[:records] # return the required no of records
                
                
            
            
            
    def get_solution(self, iterations=1):
        self.__initialize()
        for i in range(iterations):
            population = []
            for chromosome in self.current_population:
                key,value=self.__calculate_fitness_function(chromosome)
                population.append((key,value))
            population=sorted(population, key = lambda item: item[1], reverse = True)
            print population
            # keep the elitest chromosomes i.e., half of the chromosomes in the new
            new_population = []
            new_population=self.selection(population = population, strategy = 'elitism', records = self.elitism_constant)
            #And select the remaining half of the chromosomes by using roulette wheel selection 
            #print new_population
            new_population.extend(self.selection(population[:self.elitism_constant], strategy = 'roulette wheel', records = self.population_size - self.elitism_constant))
            #print new_population, len(new_population)
            self.current_population = copy.deepcopy(new_population)
        c_f=[]
        for c in self.current_population:
             key,value = self.__calculate_fitness_function(c)
             c_f.append((key,value))
        c_f=sorted(c_f, key = lambda item:item[1], reverse = True)
        print "***"
        print c_f   
        print "*********"
        return c_f[0]# return the best one
def main():
    g = FNRGeneticAlgorithm(failed_sensor_nodes = [9, 7, 10, 81, 23, 57, 34, 46, 66, 70], population_size=20)
    sol=g.get_solution(iterations=4 )
    print sol
    
if __name__ == "__main__":
    main()
