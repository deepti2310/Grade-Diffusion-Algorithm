import networkx as nx
import logging
import sys
import time

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

class Rectangle(object):
    def __init__(self, bottom_left, top_left, top_right, bottom_right):
        self.bottom_left = bottom_left
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_right = bottom_right


class Node(object):
    def __init__(self, nid, x, y, z ):
        self.nid = nid
        self.x=x
        self.y=y
        self.z=z
        
    def get_position(self):
        return ("x:{0} y:{0} z:{0}".format(self.x,self.y,self.z))
        
class WSNDeployer(object):
    
    def __init__(self, no_of_nodes = 3000, x=100,y=100,z=100, radio_range = 15, min_distance = 2):
        
        self.no_of_nodes = no_of_nodes
        self.x,self.y,self.z=x,y,z
        self.distance = min_distance
        self.nodes = []
    
    def place_nodes(self, i, j, k, step=10):
        pass
        
    def deploy(self):
        step = 10
        for i in range(0,self.x,step):
            for j in range(0, self.y, step):
                for k in range(0, self.z, step):
                    place_nodes(i, j, k, step)

"""
def prepare_graph():
    #global settings;
    graph = nx.Graph() 
    graph.add_node('s', name = "source", index= 's')
    graph.add_node('t', name = "destination",index='t' )
    for i in range(settings['nodes']):
        graph.add_node(i)
    edges = []
    edges.append(('s',0,1))
    edges.append(('s',1,1))
    edges.append(('s',2,1))
    for i in range(settings['nodes']):
        if i+1<settings['nodes']: edges.append((i, i+1,1))
        if i+2<settings['nodes']: edges.append((i,i+2,1))
        if i+3<settings['nodes']: edges.append((i,i+3,1))
    edges.append((settings['nodes']-3,'t',1))
    edges.append((settings['nodes']-2,'t',1))
    edges.append((settings['nodes']-1,'t',1))
    
    graph.add_weighted_edges_from(edges)
    draw_graph(graph)
    return graph
"""
def main():
    #prepare_graph()
    #g=GradeDiffusion(graph)
    pass
if __name__=="__main__":
    main()
