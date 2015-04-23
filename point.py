class Point(object):
    def __init__(self, x=0, y=0):
        self.x=x
        self.y=y
        
    def get_distance(self, other):
        return ((self.x-other.x)**2+(self.y-other.y)**2)**(0.5)
    
    def __repr__(self):
        return ("x:{0} y:{1}".format(self.x, self.y))
   
    def get_position(self):
        return {'x':self.x, 'y':self.y}


