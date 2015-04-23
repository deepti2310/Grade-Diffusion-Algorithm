from network_deployer import NetworkDeployer
from ngd import GD
def main():
    import io,json
    n=NetworkDeployer(x=200, y=200, radio_range = 10)
    n.deploy()
    n.build_graph()
    gd=GD(n.graph, datapackages = 300) #pass the built-up graph to GD
    
    results = []
    for cycle in range(0, 300):
        result={}
        
        seq_list=gd.simulate()
        result['source']=gd.source
        result['sink']=gd.sink
        result['seq']=seq_list
        result['cycle']=cycle
        results.append(result)
        #calculate bth
        b_th = gd.calculate_b_th(beta = 0.9)
        if b_th > 0:
            print b_th
            #call ga algorithm
            depleted_nodes = gd.get_depleted_nodes()
            print depleted_nodes
            break
    with io.open('results.json', 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(results, ensure_ascii=False)))
        
    print gd.packet_loss
if __name__=="__main__":
    main()
