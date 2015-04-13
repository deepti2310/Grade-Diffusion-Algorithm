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

    def __init__(self, nid, point):
        self.id = nid
        self.co_ordinates=point
  
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

         
class NetworkDeployer(object):
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
    def __init__(self, graph, datapackages = 300, node_energy = 3600):
        self.graph = graph
        self.datapackages = 300
    
    def get_nodes(self):
        pass
    
    def _random_source_sink(self):
        """
        make sure there is a path in between source and sink 
        """
        no_of_nodes = len(self.graph)
        while(True):
            source, sink = random.randint(0, no_of_nodes),random.randint(0, no_of_nodes)
            try:
                nx.shortest_path(self.graph, source=source, target = sink)
                break
            except: 
                pass
        return source, sink
             
    def _grade_value(self,node):
        return self.graph.node[node]['grade_value']         
    
    def _reachable_nodes(self, node):
        return self.graph.neighbors(node)
    
    def _fill_grade_values(self, sink):
        """
        Find Shortest distance from every node to sink, and make it as a grade value
        if there are nodes which are unreachable from sink, make their grade value as 'infinite'
        """
        g = nx.shortest_path(self.graph, target = sink)
        for node in self.graph:
            try:
                """
                g[node] contains end points, so to count hop-count, just reduce it by 1
                """
                self.graph.node[node]['grade_value']=len(g[node])-1
            except:
                self.graph.node[node]['grade_value']=float('inf')
                
    def _inside_nodes(self, node):
        inside_nodes = []
        for adjacent_node in self._reachable_nodes(node):
            if self._grade_value(adjacent_node) < self._grade_value(node):
                 inside_nodes.append(adjacent_node)
        return inside_nodes
    
    def _outside_nodes(self, node):
        outside_nodes = []
        for adjacent_node in self._reachable_nodes(node):
            if self._grade_value(adjacent_node) >= self._grade_value(node):
                 outside_nodes.append(adjacent_node)
        return outside_nodes
    
    
    def _neighbors(self, node):
        neighbors = []
        for adjacent_node in self._reachable_nodes(node):
            if self._grade_value(adjacent_node) == self._grade_value(node):
                 neighbors.append(adjacent_node)
        return neighbors
    
        
    def _create_grade_table(self):
        for node in self.graph:
            table = []
            for inside_node in self._inside_nodes(node):
                entry = {}
                entry['current_node']=node
                entry['relay_node']= inside_node
                entry['grade_value']=self._grade_value(inside_node)
                entry['overload']=self._payload(inside_node)
                table.append(entry)
            self.graph.node[node]['routing_table']=table           
    
    def _fill_neighbors(self):
        for node in self.graph:
            self.graph.node[node]['neighbors']=self._neighbors(node)    
    
    def _fill_payload_values(self):
        """ 
        Payload values 
        """
        for node in self.graph:
            self.graph.node[node]['payload']=len(self._outside_nodes(node))
    
    def _payload(self, node):
        """
            return payload value of given node
        """
        return self.graph.node[node]['payload']
    
    def _set_payload(self, node=None, value=None):
        """
        set payload of a node
        """
        self.graph.node[node]['payload']=value
        
    def _graph_info(self):
         for node in self.graph:
            print self.graph.node[node]       
    
    def _pre_process(self,sink):
        """
        1. First generate sink and source, and make sure that sink is reachable from source
        
        """
        sink = sink
        self._fill_grade_values(sink)
        self._fill_neighbors()
        self._fill_payload_values()
        self._create_grade_table()
        
    
    def _threshold(self, current_node):
        routing_table = self._routing_table(current_node)
        
    def _select_relay_node(self, node):
        """
        Select a relay node to do data transfer
        1. First retrieve routing_table
        1.a compare the relay nodes overload with the threshold, if every relay node overload exceeds choose a random neighbor
        2. capture the relay_nodes and its their payloads (return if there is any relay load with payload 0
        3. choose one relay node based on probability
        4. return the selected relay node
        """
        #Step:1
        routing_table = self._routing_table(node)
        overload_dict = OrderedDict([(entry['relay_node'], entry['overload'])for entry in routing_table])
        
        #step 1.a:
        
        
        
        #Step: 2
        for n,overload in overload_dict.iteritems():
            if overload == 0:
                return n 
        #else
        cdf_dict = OrderedDict()
        overload_sum=sum([1.0/overload for n,overload in overload_dict.iteritems()]) 
        
        r=random.random()
        s=0
        for n, overload in overload_dict.iteritems():
            s+=(1.0/overload)
            if r <= s/overload_sum:
                return n
    
    def _routing_table(self, node):
        return self.graph.node[node]['routing_table']
    
    def _update_routing_table(self, node, relay_node):
        """
        update routing table
        1. grab the current node routing table
        2. find the relevant entry of relay_node
        3. get payload_old, and find the new payload by using equation 2 p_new
        4. update the overload by using equation 3
        """
        routing_table=self._routing_table(node)
        index=None
        for counter,entry in enumerate(routing_table):
            if entry['relay_node']==relay_node:
                index=counter #found the entry
                break
        
        if index!=None:
            #print '-',index
            #print relay_node, index
            p_old = self._payload(relay_node)
            p_new = self._payload(relay_node) + self._payload(relay_node)*1.0/self._grade_value(node)
            self.graph.node[node]['routing_table'][index]['overload']+=p_old+p_new
            
    def simulate(self):
        source, sink = self._random_source_sink()
        self._pre_process(sink)
        for i in range(self.datapackages):
          current_node = source
          print "--------------------------"
          while(current_node != sink):
            print current_node
            relay_node = self._select_relay_node(node=current_node)
            #update routing table over-load values of current node
            self._update_routing_table(current_node, relay_node)          
            #update payload values, and overload value
            new_payload_value = self._payload(relay_node) + self._payload(relay_node)*1.0/self._grade_value(current_node)
            self._set_payload(node=relay_node,value = new_payload_value)
            
            #
            current_node = relay_node
            
            
def main():
    n=NetworkDeployer(x=50, y=50, radio_range = 5)
    n.deploy()
    n.build_graph()
    gd=GD(n.graph, datapackages = 300) #pass the built-up graph to GD
    gd.simulate()
    
if __name__=="__main__":
    main()
