

class GA(object):
    def __init__(self, graph, population_size = 10, elitism_constant = None):
        self.population_size = population_size
        self.elitism_constant = elitism_constant or population_size//2
        self.graph = graph
        self.current_chromosomes = None
        
    def _get_depleted_nodes(self):
        depleted_nodes = []
        for node in self.graph:
            if self.graph.node[node]['node_obj'].get_energy() <= 0:
                depleted_nodes.append(node)
        return depleted_nodes
    
    def _initialize(self):
        for i in range(self.population_size):
            chromosome = []
            for j in range(len(self._get_depleted_nodes())):
                chromosome.append(random.randint(0,1))
            self.current_chromosomes.append(chromosome)
    
    def _elitisim_selection(self, population, records = 1):
        """
        population is a list of tuples, where each tuple is a combination of (chromosome, fitness value)
        
        """
        
        population=sorted(population, key = lambda item: item[1], reverse = True) # sort
        return [list(i[0]) for i in population[0:records]]
    
    def _calculate_cumulatiave_probability(self, population):
        """
        population is a list of tuples, where each tuple is a combination of (chromosome, fitness value)
        
        """
        sigma = sum([ fitness for chromsome, fitness in populaton])
        #now calculate the probability mass function
        pmf = []
        for chromosome, fitness in population[:-1]:
            prob = fitness * 1.0 / sigma
            pmf.append((chromosome, prob))
        else:
            last_chromosome = population[-1][0]
            last_prob = 1-sum([p for c, p in pmf])
            pmf.append((last_chromosome, last_prob))
        #now calculate cumulative distribution function
        cdf = []
        for counter, (chromosome, prob) in enumerate(pmf):
            cdf.append((chromosome, sum([j[1] for j in pmf[:i+1]])))
        return cdf

    def _select_pair(self, cdf):
        first, second = random.random(), random.random()
        f,s=None,None
        #iterate over pdf
        for chromosome, prob in cdf:
            if first <= prob and f is None:
                f = chromosome
            if second <=prob and s is None:
                s = chromosome
        return f,s

    def _crossover(self, pair):
        first, second = pair[0], pair[1]
        p = random.randint(1, len(first)-1)
        f_0, f_1 = first[:p], first[p:]
        s_0, s_1 = second[:p], second[p:]
        new_pair = f_0+s_1, s_0+f_1
        return new_pair
    
    def _mutation(self, chromosome):
        l = len(chromosome)
        rand_gene = random.randint(0, l-1)
        chromosome[rand_gene]=1-chromosome[rand_gene] #flip it
        return chromosome
                    
    def _roulette_selection(self, population, records = 1):
        population=sorted(population, key = lambda item: item[1], reverse = True)
        cdf = self._calculate_cumulative_probability(population)
        
        new_population = []
        for i in range(0, self.population_size - self.elitism_constant,2):
            pair = self._select_pair(cdf)
            crossover_pair = self._crossover(pair)
            for j in crossover_pair:
                n = self._mutation(j)
                new_population.append(n)
        return new_population[:records] 
    def _calculate_fitness_function(self, chromosome):
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
              
    def _get_solution(self, iterations = 1):
        self._initialize()
        for i in range(iterations):
            population = []
            for chromosome in self.current_population:
                key, value = self._calculate_fitness_function(chromosome)
                population.append((key, value))
                new_population = self._elitisim_selection(population = population, records = self.elitism_constant)
                new_population.extend(self._roulette_selection(population, records = self.population_size - self.elitism_constant))
                self.current_population = new_population
        c_f=[]
        for chromosome in self.current_population:
             chromosome,fitness_value = self._calculate_fitness_function(chromosome)
             c_f.append((chromosome,fitness_value))
        c_f=sorted(c_f, key = lambda item:item[1], reverse = True)
        return c_f[0]
def main():
    pass

if __name__ == "__main__":
    main()
        

