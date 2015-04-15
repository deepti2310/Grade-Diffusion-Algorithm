import pygame, sys
from pygame.locals import *

class Color(object):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    
    def __init__(self):
        pass
    
class NetSim(object):
    def __init__(self, f=None):
        self.f=f
        self.FPS=30
        self.fpsClock = pygame.time.Clock()
    
    def draw_circle(self, surf=None, color=Color.BLUE, center_point=None, radius = None, width=0):
        pygame.draw.circle(surf, color, center_point, radius, width)
    
    def draw_line(self, surf=None, color=Color.RED, p1 = None, p2=None, width=0):
        pygame.draw.line(surf, color,p1, p2, width)
    
    def paint(self):
        
        #########################
        p1=(100,200)
        p2=(200,300)
        p3=(300,400)
        ########################
        
        self.draw_line(self.DISPLAYSURF, Color.RED, p1, p2, 4)
        self.draw_line(self.DISPLAYSURF, Color.RED, p2, p3, 4)
        
        self.squareImg = pygame.image.load('square1.png')
        self.draw_circle(surf=self.DISPLAYSURF, color=Color.BLUE, center_point=p1, radius = 10)
        self.draw_circle(surf=self.DISPLAYSURF, color=Color.BLUE, center_point=p2, radius = 10)
        self.draw_circle(surf=self.DISPLAYSURF, color=Color.BLUE, center_point=p3, radius = 10)
    
    
    def get_position(self, p1, p2):
        p1_x,p1_y=p1
        p2_x,p2_y=p2
        
    def simulate(self):
        pygame.init()
        
        self.DISPLAYSURF = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption("Grade Diffusion")
        
        x=10
        y=20
        while True:
            self.DISPLAYSURF.fill(Color.WHITE)
            self.paint()
            self.DISPLAYSURF.blit(self.squareImg, (x, y))
            x+=2
            y+=2        
            #squareImg.scroll(x, y)
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
