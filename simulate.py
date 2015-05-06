from network_deployer import NetworkDeployer
from ngd import GD
from nga import GA
from ld import LD
import copy
import dill
def main():
    import io,json
    n=NetworkDeployer(x=200, y=200, radio_range = 40)
    n.deploy()
    n.build_graph()
    sink = n._get_sink()
    gd=GD(n.graph, datapackages = 300,sink = sink) #pass the built-up graph to GD
    gd._pre_process(sink)
    ld=LD(copy.deepcopy(n.graph), datapackages = 300,sink = sink) #pass the built-up graph to GD
    ld._pre_process(sink)
    
    results = []
    for cycle in range(0, 600):
        source, sink=gd._random_source_sink()
        result={}
        seq_list=gd.simulate(source, sink)
        ld_seq_list=ld.simulate(source, sink)
        result['source']=gd.source
        result['sink']=gd.sink
        result['seq']=seq_list
        result['cycle']=cycle
        results.append(result)
        #calculate bth
        b_th = gd.calculate_b_th(beta = 0.9)
        if b_th > 0:
            #print b_th
            #call ga algorithm
            depleted_nodes = gd.get_depleted_nodes()
            for d_node in depleted_nodes:
                #print gd.graph.node[d_node]['node_obj'].get_energy(), gd._grade_value(d_node), d_node
                pass
            print "depleted_nodes:", depleted_nodes
            break
    """
    with open('my_gd.pik', 'wb') as f:
        dill.dump(gd,f)
    """
    with io.open('results.json', 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(results, ensure_ascii=False)))
    depleted_nodes = gd.get_depleted_nodes()
    print "GD Depleted nodes", gd.get_depleted_nodes()
    print "LD Depleted nodes", ld.get_depleted_nodes()
    if depleted_nodes:  
        ga = GA(gd.graph)
        #print "****************"
        sol= ga._get_solution()
        replaced_nodes = [ node for node, flag in zip(ga.get_depleted_nodes(), sol[0]) if flag == 1]
        print "replaced_nodes:", replaced_nodes
    print "****************************"
if __name__=="__main__":
    main()
