from network_deployer import NetworkDeployer
from ngd import GD
from nga import GA
from ld import LD
from globalOGD import GGD
import copy
import dill
from matplotlib import pyplot as plt
import numpy as np
import pygal
"""
required modules pygal

pip install lxml
pip install cairosvg
pip install tinycss
pip install cssselect
pip install pygal
"""
"""
x = np.linspace(0, 10)

with plt.style.context('fivethirtyeight'):
    plt.plot(x, np.sin(x) + x + np.random.randn(50))
    plt.plot(x, np.sin(x) + 0.5 * x + np.random.randn(50))
    plt.plot(x, np.sin(x) + 2 * x + np.random.randn(50))

"""
plt.show()

def main():
    import io,json
    n=NetworkDeployer(x=200, y=200, radio_range = 10)
    n.deploy()
    n.build_graph()
    sink = n._get_sink()
    gd=GD(n.graph, datapackages = 300,sink = sink) #pass the built-up graph to GD
    gd._pre_process(sink)
    ld=LD(copy.deepcopy(n.graph), datapackages = 300,sink = sink) #pass the built-up graph to LD
    ld._pre_process(sink)
    ggd = GGD(copy.deepcopy(n.graph), datapackages = 300,sink = sink) #pass the built-up graph to GGD
    
    gd_power_consumption = []
    ld_power_consumption = []
    ggd_power_consumption = []
    
    gd_packet_loss = []
    ld_packet_loss = []
    ggd_packet_loss=[]

    gd_depleted_nodes = []
    ld_depleted_nodes = []
    ggd_depleted_nodes = []


    results = []
    ld_results = []
    ggd_results = []
    for cycle in range(0, 300):
        source, sink=gd._random_source_sink()
        result={}
        ld_result={}
        ggd_result={}
        seq_list=gd.simulate(source, sink)
        ld_seq_list=ld.simulate(source, sink)
        ggd_seq_list=ggd.simulate(source, sink)
        """ GD results """
        result['source']=gd.source
        result['sink']=gd.sink
        result['seq']=seq_list
        result['cycle']=cycle
        results.append(result)
        #----------------------------
        """ LD results """
        ld_result['source']=ld.source
        ld_result['sink']=ld.sink
        ld_result['seq']=ld_seq_list
        ld_result['cycle']=cycle
        ld_results.append(ld_result)
        #----------------------------
        """ GGD results """
        ggd_result['source']=ggd.source
        ggd_result['sink']=ggd.sink
        ggd_result['seq']=ggd_seq_list
        ggd_result['cycle']=cycle
        ggd_results.append(ggd_result)
        #----------------------------
        #packet loss 
        gd_packet_loss.append({'cycle':cycle, 'packet_loss': gd.packet_loss})
        ld_packet_loss.append({'cycle':cycle, 'packet_loss': ld.packet_loss})
        ggd_packet_loss.append({'cycle':cycle, 'packet_loss': ggd.packet_loss})
        
        #depleted nodes
        gd_depleted_nodes.append({'cycle':cycle, 'depleted_nodes':len(gd.get_depleted_nodes())})
        ld_depleted_nodes.append({'cycle':cycle, 'depleted_nodes':len(ld.get_depleted_nodes())})
        ggd_depleted_nodes.append({'cycle':cycle, 'depleted_nodes':len(ggd.get_depleted_nodes())})

        #calculate bth
        b_th = gd.calculate_b_th(beta = 0.9)
        if b_th > 0:
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
    ###########################################################################
    
    line_chart = pygal.Line()
    line_chart.title = 'packet_loss'
    line_chart.x_labels = map(str, range(len(gd_packet_loss)))
    line_chart.add('GD Packet Loss', [cycle['packet_loss'] for cycle in gd_packet_loss])
    line_chart.add('GGD Packet Loss',  [cycle['packet_loss'] for cycle in ggd_packet_loss])
    line_chart.add('LD Packet Loss',  [cycle['packet_loss'] for cycle in ld_packet_loss])
    line_chart.render_to_png('packet_loss.png')

    ###############################################################################
    ###########################################################################
    
    line_chart = pygal.Line()
    line_chart.title = 'Depleted Nodes'
    line_chart.x_labels = map(str, range(len(gd_depleted_nodes)))
    line_chart.add('GD Depleted Nodes', [cycle['depleted_nodes'] for cycle in gd_depleted_nodes])
    line_chart.add('GGD Depleted Nodes',  [cycle['depleted_nodes'] for cycle in ggd_depleted_nodes])
    line_chart.add('LD Depleted Nodes',  [cycle['depleted_nodes'] for cycle in ld_depleted_nodes])
    line_chart.render_to_png('depleted_nodes.png')

    ###############################################################################
    
    depleted_nodes = gd.get_depleted_nodes()
    print "GGD Depleted nodes", ggd.get_depleted_nodes()
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
