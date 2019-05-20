import pygame
import sys
from pygame.locals import *
from components.component import Component


class Text(Component):
    def __init__(self, window,text,style={}, parent=None):

        self.window = window
        self.parent = parent

        super().__init__(style)

        self.myfont = pygame.font.SysFont(self.style["font-family"], self.style["font-size"])
        self.myfont.set_bold(self.style["font-bold"])
        self.label = self.myfont.render(text, 1, self.style["color"])

        if(self.style["shadow"]):
            self.labelS = self.myfont.render(text, 0, self.style["color"])
            self.labelS.set_alpha(50)
            window.blit(self.labelS, (self.position[0]+self.style["shadow"][0], self.position[1]+self.style["shadow"][1]))

        window.blit(self.label, self.position[:2])

    def draw(self): self.window.blit(self.label, self.position[:2])
