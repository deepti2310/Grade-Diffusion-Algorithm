import networkx as nx
import logging
import sys
import time
import random
from tabulate import tabulate #pip install tabulate
from collections import OrderedDict
def draw_graph(G):
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size = 700)
    nx.draw_networkx_edges(G, pos, edgelist = G.edges(), edge_color = 'b', style = 'dotted')
    nx.draw_networkx_labels(G, pos, font_size=10)
    plt.axis('on')
    plt.savefig('rendered_graph.png')
    plt.show()
try:
    import matplotlib.pyplot as plt
except:
    raise
logging.basicConfig(filename = 'gd.log', level = logging.DEBUG)

class Node(object):

    def __init__(self, nid, point, energy=3600):
        self.id = nid
        self.co_ordinates=point
        self.energy = energy
    
    def set_energy(self, n):
        self.energy = n
    
    def reduce_energy(self, r):
        self.energy -= r
    
    def __repr__(self):
        return ("ID: {0} x:{1} y:{2}".format(self.id, self.co_ordinates.x,self.co_ordinates.y))
    
    def get_position(self):
        return {'x':self.co_ordinates.x, 'y':self.co_ordinates.y}
    
    def distance(self, other):
        return self.co_ordinates.get_distance(other.co_ordinates)    

class Point(object):
    def __init__(self, x=0, y=0, energy = 3600):
        self.x=x
        self.y=y
        self.energy = energy
        
    def get_distance(self, other):
        return ((self.x-other.x)**2+(self.y-other.y)**2)**(0.5)
    
    def __repr__(self):
        return ("x:{0} y:{1}".format(self.x, self.y))
   
    def reduce_energy(self, r):
        self.energy -= r
    
    def get_energy(self):
        return self.energy
    
    def get_position(self):
        return {'x':self.x, 'y':self.y}

         
class WSNDeployer(object):
    def __init__(self, x=100, y=100, radio_range=10, min_distance=2):
        self.x=x
        self.y=y
        self.nodes = []
        self.graph = nx.Graph()
        self.counter = 0
        self.min_distance=min_distance
        self.radio_range = radio_range
        
    def _place_nodes(self, i, j, step, max_nodes):
        
        """
        Max nodes is no of nodes that i can palce inside a sub-volume
        
        Procedure: Generate a point, and make sure it is having atleast 2 units of distance apart from others, 
        once the points are selected, just create the new nodes and append them to the self.nodes
        """
        points = []
        for i in range(max_nodes):
            while(True):
                t = Point(random.randint(i,i+step), random.randint(j,j+step)) 
                if all([point.get_distance(t) > self.min_distance for point in points]):
                    points.append(t)
                    break
        
        for point in points:
            n=Node(self.counter, point)
            self.nodes.append(n)
            self.counter+=1
            
    def deploy(self):
        """
        take the area (2-Dimensional)
        and place the nodes
        """
        step = 10
        for i in range(0, self.x, step): 
            for j in range(0, self.y, step):
                self._place_nodes(i,j, step, max_nodes = 3)
    
    
    def build_graph(self):
        """
        add nodes to the graph, and create the edges in between nodes based on the distance
        if distance is less than radio_range. 
        """
        for node in self.nodes:
            self.graph.add_node(node.id, info=node)
        edges = []
        for i in range(0, len(self.nodes)):
            for j in range(i+1, len(self.nodes)):
                if (self.nodes[i].distance(self.nodes[j]) < self.radio_range):
                    edges.append((self.nodes[i].id, self.nodes[j].id,1))
        self.graph.add_weighted_edges_from(edges) 
        #show graph here
        
class GD(object):
    def __init__(self, graph, datapackages = 300):
        self.graph = graph
        self.datapackages = 300
        self.nodes = []
    
    def get_nodes(self):
        pass
    
    def random_source_sink(self):
        pass    
        
    def _pre_process(self,):
        """
        1. First generate sink and source, and make sure that sink is reachable from source
        
        """
        source, sink = self.random_source_sink()
            
        pass
    def simulate(self):
        self._pre_process()
        pass
def main():
    w=WSNDeployer(x=50, y=50, radio_range = 15)
    w.deploy()
    w.build_graph()
    gd=GD(w.graph) #pass the built-up graph to GD
    gd.simulate()
    
if __name__=="__main__":
    main()
