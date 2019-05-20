import pygame
import sys
from pygame.locals import *
from components import Image, View, Text, Menu
from game.index import Game

class Window():
    def __init__(self):

        pygame.init()
        pygame.display.set_caption("Binding of Automata IV")
        self.window = pygame.display.set_mode((1280,960)) #,pygame.FULLSCREEN

        self.elementsDraw = [Image(self.window, "src/image/background.png")]

        main = View(self.window, style={
            "height": "86%",
            "top":"7%"
        })
        self.elementsDraw.append(Text(self.window, text="MENU PRINCIPAL",style={
            "font-size": 80,
            "left": "1%",
            "shadow": (5,5),
            "color": (58,54,42)
        }, parent=main))

        container = View(self.window, style={
            "height": "80%",
            "top":"10%",
        }, parent=main)
        

        self.elementsDraw.append(Menu(self.window,element=[
            ["Niveau 1", lambda: self.start("level1")],
            ["Niveau 2", lambda: self.start("level2")],
            ["Salle de test", self.start],
            ["Paramètre", self.start],
            ["Quitter", self.quit]
        ], style={
            "width": 1/3,
            "left": "2%",
            "top": "25%",
            "height": "50%",
            "align-y": True,
        }, parent=container))

    def start(self, level="level1"):
        self.elementsDraw = []
        self.game = Game(self.window, "levels/"+ level +".json")
    @staticmethod
    def quit(): pygame.quit()

    def draw(self):
        if self.elementsDraw == []:
            self.game.run()
        else:
            for element in self.elementsDraw: element.draw()
            pygame.display.update()
