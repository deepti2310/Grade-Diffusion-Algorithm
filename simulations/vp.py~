from __future__ import division
from visual import *

"""
ball = sphere(pos=(-5,0,0), radius=0.5, color=color.cyan)
wallR = box(pos=(6,0,0), size=(0.2,12,12), color=color.green)
ball.velocity = vector(25,0,0)
deltat = 0.005
t = 0
import time
#varr = arrow(pos=ball.pos, axis=ball.velocity, color=color.yellow)
while True:
    ball.pos = ball.pos+ball.velocity * deltat
    t=t+deltat
    rate(30)
"""

class NetSim(object):
    def __init__(self):
        self.points = [(3,5,0), (1,2,0), (2,7,0)]
    def simulate(self):
        nodes = []
        edges=[]
        counter=0
        for point in self.points:
            nodes.append(sphere(pos=point, radius = 0.5, color = color.red, ))
            label(pos=point, text=str(counter))
            counter+=1
        for i in range(len(self.points)-1):
            edges.append(curve(pos=[self.points[i], self.points[i+1]], radius=0.01))
        deltat=0.05
        t=5
        box(pos=(6,0,0), size=(0.2,12,12), color=color.green)    
            
        
        
s=NetSim()
s.simulate()
