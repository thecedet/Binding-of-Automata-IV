import pygame
import sys
from pygame.locals import *
from components.component import Component


class View(Component):
    def __init__(self, window, style={}, parent=None):

        self.window = window
        self.parent = parent

        super().__init__(style)

        if(self.style["background"]):
            pygame.draw.rect(self.window, self.style["background"], self.position)

    def draw(self):
        if(self.style["background"]):
            pygame.draw.rect(self.window, self.style["background"], self.position)
