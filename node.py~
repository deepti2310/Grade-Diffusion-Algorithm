class Node(object):

    def __init__(self, nid, point, energy = 360):
        self.id = nid
        self.co_ordinates=point
        self.energy = energy
    
    def is_alive(self):
        if self.get_energy() > 0:
            return True
        else:
            return False
        
    def consume_tx_energy(self):
        if self.is_alive():
            self.energy-=1.6
            return True            
        raise ValueError("Node is not having sufficient power to transmit data, and considered to be dead")
    
    def get_energy(self):
        return self.energy
        
    def __repr__(self):
        return ("ID: {0} x:{1} y:{2}".format(self.id, self.co_ordinates.x,self.co_ordinates.y))
    
    def get_position(self):
        return {'x':self.co_ordinates.x, 'y':self.co_ordinates.y}
    
    def distance(self, other):
        return self.co_ordinates.get_distance(other.co_ordinates)    

