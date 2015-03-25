import networkx as nx
import logging
import sys
import time

settings = {
    'nodes':15,

}
def draw_graph(G):
    #pos = nx.spectral_layout(G)
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


class Point(object):
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y

        
class Rectangle(object):
    def __init__(left_bottom, left_top, right_top, right_bottom):
        self.left_bottom = left_bottom or Point()
        self.left_top = left_top or Point()
        self.right_top=right_top or Point()
        self.right_bottom = right_bottom or Point()
                 
class ReqInterestMessage(object):
    def __init__(self, veh_type, interval, duration, rect):
        self.int_type = veh_type or None
        self.int_interval = interval or None
        self.int_duration = duration or None
        self.int_rect = rect or None


class RepInterestMessage(object):
    def __init__(self, veh_type, veh_instance, location, intensity, confidence, timestamp):
        pass
    

class CacheInterestEntry(object):
    def __init__(self, node, event_rate):
        self.node = node
        self.event_rate = event_rate or 1

class InterestCache(object):
    
    def __init__(self, entries=None):
        self.entries = entries or []
    
    def add_entry(self, entry):
        self.entries.append(entry)
    
    def remove_entry(self, entry):
        pass
        
    def add_gradient(self, gradient):
        pass
    
    def remove_gradient(self,gradient):
        pass    

class DataCacheEntry(object):
    pass

class DataCache(object):
    pass
    
class Node(object):
    def __init__(self, neighbors=None, cache=None, energy=3600):
        self.neighbors = neighbors or []
        self.cache = cache
        self.energy = energy
        
    def send_interest_message(self):
        pass
    def receive_interest_message(self):
        pass
    
class GradeDiffusion(object):
    def __init__(self,graph):
        self.graph = graph;
    
    def simulate
    
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
    
def main():
    prepare_graph()
    g=GradeDiffusion(graph)
    
if __name__=="__main__":
    main()
