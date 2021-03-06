import logging
import networkx as nx
from point import Point
from node import Node
import random
try:
    import matplotlib.pyplot as plt
except:
    raise
logging.basicConfig(filename = 'gd.log', level = logging.DEBUG)



def draw_graph(G):
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size = 700)
    nx.draw_networkx_edges(G, pos, edgelist = G.edges(), edge_color = 'b', style = 'dotted')
    nx.draw_networkx_labels(G, pos, font_size=10)
    plt.axis('on')
    plt.savefig('rendered_graph.png')
    plt.show()
         
class NetworkDeployer(object):
    def __init__(self, x=100, y=100, radio_range=10, min_distance=2):
        self.x=x
        self.y=y
        self.nodes = []
        self.graph = nx.Graph()
        self.counter = 0
        self.min_distance=min_distance
        self.radio_range = radio_range

    def _get_sink(self):
        """
        get the sink which is in the middle of the network
        """
        #first get mid of x and y
        x,y = self.x//2,self.y//2
        p1=Point(x,y)
        min_dist=float('inf')
        sink = None
        #print len(self.nodes)
        for counter,node in enumerate(self.nodes):
            p2=node.co_ordinates
            #print p2, p1
            
            d=p1.get_distance(p2)
            #print d
            if min_dist > d :
                min_dist = d
                sink = node
        #print sink.id
        return sink.id
    def _place_nodes(self, i, j, step, max_nodes):
        
        """
        Max nodes is no of nodes that i can palce inside a sub-volume
        
        Procedure: Generate a point, and make sure it is having atleast 2 units of distance apart from others, 
        once the points are selected, just create the new nodes and append them to the self.nodes
        """
        points = []
        for k in range(max_nodes):
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
            self.graph.add_node(node.id, node_obj=node)
        edges = []
        for i in range(0, len(self.nodes)):
            for j in range(i+1, len(self.nodes)):
                if (self.nodes[i].distance(self.nodes[j]) < self.radio_range):
                    edges.append((self.nodes[i].id, self.nodes[j].id,1))
        self.graph.add_weighted_edges_from(edges) 


def main():
    n=NetworkDeployer(x=200, y=200, radio_range = 10)
    n.deploy()
    n.build_graph()
    n._get_sink()

if __name__=="__main__":
    main()
