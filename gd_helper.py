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
    

class InterestEntry(object):
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

class DataEntry(object):
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
    

