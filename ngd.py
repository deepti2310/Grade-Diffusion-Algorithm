import networkx as nx
import sys
import time
import random
from tabulate import tabulate #pip install tabulate
from collections import OrderedDict, defaultdict
#8673425
        
class GD(object):
    def __init__(self, graph, datapackages = 300, source = None, sink = None):
        self.graph = graph
        self.datapackages = 300
        self.packet_loss=0
        self.source=source
        self.sink=sink
    def _random_source_sink(self):
        """
        make sure there is a path in between source and sink 
        """
        
        no_of_nodes = len(self.graph)
        while(True):
            if not self.sink:
                source, sink = random.randint(0, no_of_nodes-1),random.randint(0, no_of_nodes-1)
            else:
                source, sink = random.randint(0, no_of_nodes-1), self.sink
            if not self.graph.node[source]['node_obj'].is_alive():
                continue
            try:
                nx.shortest_path(self.graph, source=source, target = sink)
                break
            except: 
                pass
        self.source, self.sink = source, sink
        return source, sink
    
    def _overload(self, node):
        return self.graph.node[node]['overload']
    
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
        """
         a node is either an inside node or an outside node
        """
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
                entry['overload']=0
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
        avg_overload = sum([entry['overload'] for entry in routing_table])*1.0/len(routing_table)
        current_node_payload = self._payload(current_node)
        current_node_grade = self._grade_value(current_node)
        return avg_overload * (2 + (current_node_payload*1.0/current_node_grade))
    
    def _select_relay_node(self, node):
        """
        Select a relay node to do data transfer
        1. First retrieve routing_table
        1.a if all the relay nodes overload exceeds threshold, choose a random neighbor
        2. capture the relay_nodes and its their payloads (return if there is any relay load with payload 0
        3. choose one relay node based on probability
        4. return the selected relay node
        """
        
        #Step:1
        routing_table = self._routing_table(node)
        overload_dict = OrderedDict([(entry['relay_node'], entry['overload'])for entry in routing_table])
        
        #step 1.a:
        threshold = self._threshold(node)
        s=sum([entry['overload'] for entry in routing_table])
        if s > threshold:
            try:
                return random.choice(self._neighbors(node))
            except IndexError, e:
                #if no neigbors just simply skip this step
                pass
            
        #Step: 2
        for n,overload in overload_dict.iteritems():
            if overload == 0:
                return n 
        #else
        cdf_dict = OrderedDict()
        overload_sum=sum([1.0/overload for n,overload in overload_dict.iteritems()]) 
        
        if overload_sum == 0:
            return random.choice(list(overload_dict.iterkeys()))
        #step 3 and Step 4
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
            p_old = self._payload(relay_node)
            p_new = self._payload(relay_node) + self._payload(relay_node)*1.0/self._grade_value(node)
            self.graph.node[node]['routing_table'][index]['overload']+=p_old+p_new
            #print self.graph.node[node]['routing_table'][index]['overload']
            
    def get_depleted_nodes(self):
        depleted_nodes = []
        for node in self.graph:
            if self.graph.node[node]['node_obj'].get_energy() <= 0:
                depleted_nodes.append(node)
        return depleted_nodes
            
            
    def simulate(self, source, sink):
        #source, sink = self._random_source_sink()
        #print source, sink
        seq_list=[] #just to track visited nodes
        for i in range(self.datapackages):
          current_node = source 
          seq=[]
          seq.append(current_node) 
          #print "--------------------------"
          while(current_node != sink):
            if not self.graph.node[current_node]['node_obj'].is_alive():
                self.packet_loss+=1
                break
            self.graph.node[current_node]['node_obj'].consume_tx_energy()
            relay_node = self._select_relay_node(node=current_node)
            #update routing table over-load values of current node
            self._update_routing_table(current_node, relay_node)          
            #update payload values
            if self._grade_value(current_node)==0:
                raw_input("Hmm 0 grade value")
            new_payload_value = self._payload(relay_node) + self._payload(relay_node)*1.0/self._grade_value(current_node)
            self._set_payload(node=relay_node,value = new_payload_value)
            current_node = relay_node
            seq.append(current_node) 
            
          #print "Source:", source, " Sink:", sink, "Seq:", seq, " Len:", len(seq) #print the seq of nodes traversed
          
          seq_list.append(seq)
        
        return seq_list
    def calculate_b_th(self, beta=0.9):
        b_th = 0
        grade_dict_orig = defaultdict(int)
        
        #filling the values into grade_dict_orig
        for node in self.graph:
            gv = self._grade_value(node)
            grade_dict_orig[gv]+=1
        #filling the values into grade_dict_now
        grade_dict_now = defaultdict(int)
        for node in self.graph:
            if self.graph.node[node]['node_obj'].get_energy() > 0:
                gv=self._grade_value(node)
                grade_dict_now[gv]+=1
        #T_i becomes 0 as the ratio is less than Beta ( 0<Beta<1)
        if len(grade_dict_orig) != len(grade_dict_now):
            return 1
        else:
            for key in grade_dict_orig.iterkeys():
                ratio=(grade_dict_now[key]*1.0/grade_dict_orig[key])
                #print key, grade_dict_now[key], grade_dict_orig[key],ratio
                if ratio < beta:
                    b_th+=1
        return b_th
    
        
    

