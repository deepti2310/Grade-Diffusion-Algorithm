
import random
import sys
from collections import defaultdict
class GA(object):

    def __init__(self, graph, population_size = 10, elitism_constant = None):
        self.population_size = population_size or 0
        self.elitism_constant = elitism_constant or population_size//2
        self.graph = graph
        self.current_chromosomes = []
        self.depleted_nodes=[]
        self.t_n = 0
        self.t_p = 0
    
    def get_depleted_nodes(self):
        depleted_nodes = []
        for node in self.graph:
            if self.graph.node[node]['node_obj'].get_energy() <= 0:
                depleted_nodes.append(node)
        return depleted_nodes
    
    def _initialize(self):
        #initialize the necessary instance variables
        self.depleted_nodes = self.get_depleted_nodes()
        #print self.depleted_nodes
        #calculate self.t_n
        self.t_n=len(self.graph)
        #print self.t_n
        #calculate self.t_p
        for node in self.graph:
            #print self.graph.node[node]['routing_table']
            entries=len(self.graph.node[node]['routing_table']) or 0
            self.t_p+=entries
        #print self.t_p
        
        for i in range(self.population_size):
            chromosome = []
            for j in range(0,len(self.depleted_nodes)):
                chromosome.append(random.randint(0,1))
            self.current_chromosomes.append(chromosome)

    def _elitisim_selection(self, population, records = 1):
        """
        population is a list of tuples, where each tuple is a combination of (chromosome, fitness value)
        
        """
        
        population=sorted(population, key = lambda item: item[1], reverse = True) # sort
        return [list(i[0]) for i in population[0:records]]
    
    def _calculate_cumulative_probability(self, population):
        """
        population is a list of tuples, where each tuple is a combination of (chromosome, fitness value)
        
        """
        sigma = sum([ fitness for chromsome, fitness in population])
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
            cdf.append((chromosome, sum([j[1] for j in pmf[:counter+1]])))
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
    
    def _get_grade_value(self, node):
        return self.graph.node[node]['grade_value']
    
    def _get_reusable_routing_paths(self, node, replaced_nodes=None, unreplaced_nodes = None):
        entries = self.graph.node[node]['routing_table'] 
        reusable_paths = []
        for entry in entries:
            relay_node = entry['relay_node']
            if relay_node not in unreplaced_nodes:
                reusable_paths.append(entry)

        return reusable_paths

    def _calculate_fitness_function(self, chromosome):    
        f_n=0 #fitness value
        const = (1.0/self.t_p)/(1.0/self.t_n)
        #print zip(self.depleted_nodes, chromosome)
        replaced_nodes = [ node for node, flag in zip(self.depleted_nodes, chromosome) if flag == 1]
        unreplaced_nodes = [ node for node, flag in zip(self.depleted_nodes, chromosome) if flag == 1]        
        #print replaced_nodes
        replaced_nodes_by_grade_value = defaultdict(list)
        for node in replaced_nodes:
            #get grade value
            gv=self._get_grade_value(node)
            replaced_nodes_by_grade_value[gv].append(node)
        #print replaced_nodes_by_grade_value
        for gv, nodes_list in replaced_nodes_by_grade_value.iteritems():
            number_of_reusable_routing_paths = 0
            for node in nodes_list:
                number_of_reusable_routing_paths+=len(self._get_reusable_routing_paths(node, replaced_nodes=replaced_nodes,unreplaced_nodes=unreplaced_nodes ))
            #print gv
            f_n += const*(1.0/gv)*(number_of_reusable_routing_paths*1.0/len(nodes_list))
        #print chromosome,f_n
        return chromosome, f_n
        
    def _get_solution(self, iterations = 10):
        self._initialize()
        for i in range(iterations):
            population = []
            for chromosome in self.current_chromosomes:
                c, f_n = self._calculate_fitness_function(chromosome)
                population.append((c, f_n))
            for p in population:
                #print p            
                pass
            new_population = self._elitisim_selection(population = population, records = self.elitism_constant)
            #print '-'*80
            for p in new_population:
                #print p, self._calculate_fitness_function(p)
                pass
            new_population.extend(self._roulette_selection(population, records = self.population_size - self.elitism_constant))
            self.current_chromosomes = new_population
        c_f=[]
        for chromosome in self.current_chromosomes:
             chromosome,fitness_value = self._calculate_fitness_function(chromosome)
             c_f.append((chromosome,fitness_value))
        c_f=sorted(c_f, key = lambda item:item[1], reverse = True)
        return c_f[0]

import dill
def main():
    with open('my_gd.pik', 'rb') as f:
        gd = dill.load(f)
    ga = GA(gd.graph)
    print "****************"
    sol= ga._get_solution()
    replaced_nodes = [ node for node, flag in zip(ga.get_depleted_nodes(), sol[0]) if flag == 1]
    print '-'*70
    for node in replaced_nodes:
        print node, ga.graph.node[node]['grade_value'],'-',
        pass
    print replaced_nodes
if __name__ == "__main__":
    main()
        

