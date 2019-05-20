import pygame
import sys
from pygame.locals import *
from components.component import Component

class Image(Component):
    def __init__(self, window, src, style={}, parent=None):
        self.window = window
        self.parent = parent

        super().__init__(style)

        self.image = pygame.image.load(src)
        self.image = pygame.transform.scale(self.image, self.position[2:])
        self.draw()


    def draw(self): self.window.blit(self.image, self.position[:2])
