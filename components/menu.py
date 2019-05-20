import pygame
import sys
from pygame.locals import *
from components.component import Component
from components.view import View
from components.button import Button


class Menu(Component):
    def __init__(self, window,element=[], style={}, parent=None):


        self.window = window
        self.parent = parent

        #super().__init__(style)


        menu = View(self.window, style=style, parent=parent)
        layer = View(self.window, style={
            "width": "5%",
            "background": (112,109,90),
        }, parent=menu)
        overflow = View(self.window, style={
            "width": "20%",
            "left": "60%",
            "background": (141,138,119),
        }, parent=layer)


        nbr = len(element)
        self.buttons = []
        size = int(parent.position[3]*100/nbr/parent.position[3] - (nbr-1))
        for i in range(nbr):
            self.buttons.append(Button(window,element[i][0], style={
                "width": "90%",
                "left": "10%",
                "height": str(size)+"%",
                "top": str(size*i + i*nbr)+"%",
                "background": (137,134,115),
                "after-color": (37,37,25)
            },parent=menu, callback=element[i][1]))

    def draw(self):
        for i in self.buttons: i.draw()

    def destroy(self):
        for i in self.buttons: del i