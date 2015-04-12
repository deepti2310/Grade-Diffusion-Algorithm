import networkx as nx
import logging
import sys
import time
import random
from tabulate import tabulate #pip install tabulate
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


class GradeDiffusion(object):
    def __init__(self,graph):
        self.graph = graph;
    
    def simulate(self):
        pass

class Point(object):
    def __init__(self,x=0,y=0,z=0):
        self.x=x
        self.y=y
        self.z=z
    def __sub__(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)**(0.5)
    
    def __repr__(self):
        return ("x:{0} y:{1} z:{2}".format(self.x,self.y,self.z))
class Rectangle(object):
    def __init__(self, bottom_left, top_left, top_right, bottom_right):
        self.bottom_left = bottom_left
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_right = bottom_right


class Node(object):
    def __init__(self, nid, point, energy=3600):
        self.id = nid
        self.co_ordinates=point
        self.energy = 3600
    
    def set_energy(self, n):
        self.energy = n
    
    def reduce_energy(self, r):
        self.energy -= r
    
    def __repr__(self):
        return ("ID: {0} x:{1} y:{2} z:{3}".format(self.id, self.co_ordinates.x,self.co_ordinates.y,self.co_ordinates.z))
    def get_position(self):
        return ("x:{0} y:{0} z:{0}".format(self.co_ordinates.x,self.co_ordinates.y,self.co_ordinates.z))
    def distance(self, other):
        return self.co_ordinates-other.co_ordinates    
class WSNDeployer(object):
    
    def __init__(self, no_of_nodes = 3000, x=20,y=20,z=20, radio_range = 15, min_distance = 2):
        
        self.no_of_nodes = no_of_nodes
        self.x,self.y,self.z=x,y,z
        self.distance = min_distance
        self.nodes = []
        self.radio_range = radio_range        
        self.counter=0; #node ids
        self.graph = nx.Graph()
        
    def get_nodes_info(self):
        for node in self.nodes:
            print node
            
    def place_node(self, i, j, k, step):
        """ Need to implement min distance between nodes."""
        point = Point(random.randint(i,i+step), random.randint(j,j+step), random.randint(k, k+step))
        n = Node(self.counter, point)
        self.nodes.append(n)
        self.counter+=1
        return True
                
    def place_nodes(self, i, j, k, step=10, no_of_nodes_in_sub_volume=3):
        for l in range(no_of_nodes_in_sub_volume):
            self.place_node(i,j,k, step)
        
    def deploy(self):
        step = 10    
        for i in range(0,self.x,step):
            for j in range(0, self.y, step):
                for k in range(0, self.z, step):
                    self.place_nodes(i, j, k, step, )
   
    def build_graph(self):
        for node in self.nodes:
            self.graph.add_node(node.id, info = node)
        edges = []
        for i in range(0, len(self.nodes)):
            for j in range(i+1, len(self.nodes)):
                if (self.nodes[i].distance(self.nodes[j]) < self.radio_range):
                  edges.append((self.nodes[i].id, self.nodes[j].id,1))   
        self.graph.add_weighted_edges_from(edges)
        #draw_graph(self.graph)
        
    def pre_process(self, source_id, sink_id):
        #create grade values for each node
        
        
        try:
            nx.shortest_path(self.graph, source=source_id, target = sink_id)
        except Exception, e:
            print e
            return False
        
        g = nx.shortest_path(self.graph, target = sink_id)
        for node in self.graph:
            try:
                self.graph.node[node]['grade_value']=len(g[node])-1
            except Exception,e:
                #print "error", e
                self.graph.node[node]['grade_value']=float('inf')
        #init the payload values
        print self.graph.node[source_id]['grade_value']
        
        for node in self.graph:
            self.graph.node[node]['payload_value']=0
        
                
        #create grade table
        for node in self.graph:
            table={}
            #print node, self.get_grade_value(node), self.get_reachable_nodes(node)
            for neighbor in self.get_reachable_nodes(node):
                #relay nodes are which nodes grade value is less than current node and with in the vicincity
                if self.get_grade_value(neighbor) < self.get_grade_value(node):
                    entry={}
                    entry['from']=node
                    entry['relay_node']=neighbor
                    entry['grade_value']=self.get_grade_value(neighbor)
                    entry['overload']=0
                    table[neighbor]=entry
            self.graph.node[node]['routing_table']=table
            #print self.graph.node[node]['routing_table']
        
        #create neighbors
        for node in self.graph:
            #neighbors are which are having same grade value as the current node and with in the vicincity
            neighbors=[]
            for adj_node in self.get_reachable_nodes(node):
                if self.get_grade_value(adj_node) == self.get_grade_value(node):
                    neighbors.append(adj_node)
            self.graph.node[node]['neighbors']=neighbors
        
        #outside nodes
        for node in self.graph:
            if node==sink_id:
                continue #skip sink node
            outside_node_flag=all([ self.get_grade_value(adj_node) <= self.get_grade_value(node) for adj_node in self.get_reachable_nodes(node)])
            if outside_node_flag:
                self.update_payload(node,increment=1)
            #print node, self.get_payload(node)
        return True
    def get_reachable_nodes(self, node):
        return self.graph.neighbors(node)
    
    
    def get_payload(self, node):
        return self.graph.node[node]['payload_value']
    
    def update_payload(self, node, increment=0):
        self.graph.node[node]['payload_value']+=increment
    
          
    def simulate(self, data_packages = None):
        if not data_packages:
            print "Expecting some data packages"
            sys.exit(0)
        flag = True
        #make sure you generate sink, source randomely
        #source is not equal to sink
        #make sure that sink is reachable from the source
        while(flag):
            sink_id = random.randint(0, self.counter)
            sflag=True
            while(sflag):
                source_id = random.randint(0, self.counter)
                if source_id != sink_id:
                    sflag=False
            print 'source:', source_id, 'Sink:', sink_id
            if self.pre_process(source_id, sink_id): 
                #make sure that graph is connected, and we have a connection between source and destination
                flag = False
        
        for i in range(data_packages):
            current_node = source_id
            while (current_node != sink_id):
                #select the next relay node
                current_node=self.select_relay_node(current_node) #next node
                
                #update payload of receiver
                #update overload value in grading table of sender
                #calculate the threshold L_th and based on that select neighbor node if overload of current node are over Lth
                #obtain routing table of current_node
                
            break
                
            
            
    def select_relay_node(self, current_node):
        routing_table = self.get_routing_table(current_node)
        relay_nodes = [key for key in routing_table.iterkeys()]
        return relay_nodes[0]
                
    def get_node_by_id(self, id):
        return self.graph.node[id]
    
    
    def get_routing_table(self,node):
        routing_table = self.graph.node[node]['routing_table']
        return routing_table
    
    def get_payload_value(self, node):
        payload_value = None
        return payload_value
        
    def get_grade_value(self,node):
        return self.graph.node[node]['grade_value']
       
    def get_neighbors(self, node):
        return self.graph.node[node]['neighbors']
            
    def get_remaining_energy(self, node):
        remaining_energy = None
        return remaining_energy
        
def main():
    w=WSNDeployer(x=50, y=50, z=50, radio_range = 15)
    w.deploy()
    w.build_graph()
    w.simulate(data_packages=10)
    #w.get_nodes_info()
    
if __name__=="__main__":
    main()
