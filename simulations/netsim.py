import pygame, sys
from pygame.locals import *
import math
class Color(object):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    
    def __init__(self):
        pass

def angle_wrt_x(A,B):
    """Return the angle between B-A and the positive x-axis.
    Values go from 0 to pi in the upper half-plane, and from 
    0 to -pi in the lower half-plane.
    """
    ax, ay = A
    bx, by = B
    return math.atan2(by-ay, bx-ax)

def dist(A,B):
    ax, ay = A
    bx, by = B
    return math.hypot(bx-ax, by-ay)
    
class NetSim(object):
    def __init__(self, f=None):
        self.f=f
        self.FPS=30
        self.fpsClock = pygame.time.Clock()
        self.points = [(100,200), (200, 300), (200,100)]
        self.node_radius=10
        
    def draw_circle(self, surf=None, color=Color.BLUE, center_point=None, width=0):
        pygame.draw.circle(surf, color, center_point, self.node_radius, width)
    
    def draw_edge(self, surf=None, color=Color.RED, p1 = None, p2=None, width=0):
        pygame.draw.line(surf, color,p1, p2, width)
    
    def paint(self):
        for i in range (len(self.points)-1):
            self.draw_edge(self.DISPLAYSURF, Color.RED, self.points[i], self.points[i+1], 1)
            
        self.squareImg = pygame.image.load('square1.png')
        for p in self.points:
            self.draw_circle(surf=self.DISPLAYSURF, color=Color.BLUE, center_point=p,  )
            
    
    def get_position(self, p1, p2, increment=10):
        p1_x,p1_y=p1
        p2_x,p2_y=p2
        dx=(p2_x-p1_x)*1.0/increment
        dy=(p2_y-p1_y)*1.0/increment        
        dx,dy=2,2
        return dx,dy
    def simulate(self):
        pygame.init()
        
        self.DISPLAYSURF = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption("Grade Diffusion")
        self.paint()
        
        while True:
            self.DISPLAYSURF.fill(Color.WHITE)
            self.paint()
            self.DISPLAYSURF.blit(self.squareImg, (10,20))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.update()
            self.fpsClock.tick(self.FPS)       

s = NetSim()
s.simulate()
"""


pygame.init()
DISPLAYSURF = pygame.display.set_mode((1200,600))
pygame.display.set_caption("Grade Diffusion")


#Draw on the surface object
pygame.draw.line(DISPLAYSURF, BLUE, (60,60), (120, 60), 4)
pygame.draw.circle(DISPLAYSURF, RED, (300,50), 20, 0)
pygame.draw.rect(DISPLAYSURF, RED, (200,150, 100,50))




"""
