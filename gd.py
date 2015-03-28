import networkx as nx
import logging
import sys
import time
import random

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
    def __init__(self, nid, point):
        self.id = nid
        self.co_ordinates=point
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
        draw_graph(self.graph)
    
    def pre_process(self, source_id, sink_id):
        self.all_shortest_paths(sink_id)
        
    def simulate(self):
        sink_id = random.randint(0, self.counter)
        flag = True
        while(flag):
            source_id = random.randint(0, self.counter)
            if source_id != sink_id:
                flag=False
        print 'source:', source_id, 'Sink:', sink_id
        self.pre_process(source_id, sink_id)
        
    def all_shortest_paths(self, sink):
        g = nx.shortest_path(self.graph, target = sink)
        for node in self.graph:
            #print g[node] #uncomment these to know whats going on
            self.graph.node[node]['hop_cout']=len(g[node])-1
            
        


def main():
    w=WSNDeployer()
    w.deploy()
    w.build_graph()
    w.simulate()
    #w.get_nodes_info()
    
if __name__=="__main__":
    main()
