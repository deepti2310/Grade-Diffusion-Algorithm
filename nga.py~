

class GA(object):
    def __init__(self, graph, population_size = 10, elitism_constant = None):
        self.population_size = population_size
        self.elitism_constant = elitism_constant or population_size//2
        self.graph = graph
        self.current_population = None
        
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
            self.current_population.append(chromosome)
    

