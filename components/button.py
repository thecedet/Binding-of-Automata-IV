import pygame
import sys
from pygame.locals import *
from components.component import Component
from components.view import View
from components.text import Text
from libs.EventPygame import event

class Button(Component):
    def __init__(self, window, text, style={}, parent=None, callback=None):



        event.on("MOUSEBUTTONDOWN", self.click)
        event.on("MOUSEMOTION", self.hover)

        

        self.window = window
        self.parent = parent
        self.text = text
        self.callback = callback

        self.style = style

        self.hover = False
        self.unhover = True

        
        super().__init__(style)

        self.background = {
            "old-background": self.style['background'],
            "old-after": self.style["after-color"],
            "background": self.style['background'],
            "after": self.style["after-color"],
            "old-text": (58,54,42),
            "text":  (58,54,42)
        }

        
        self.draw()


    def draw(self):
        self.style.update({
            "background": self.background["background"]
        })
        button = View(self.window, style=self.style, parent=self.parent)
        after = View(self.window, style={
            "height": "50%",
            "width": "7%",
            "left": "2%",
            "align-y": True,
            "background": self.background["after"]
        }, parent=button)
        text = Text(self.window, text=self.text,style={
            "font-size": 28,
            "left": "12%",
            "top": "20%",
            "color": self.background["text"],
            "font-bold": False
        }, parent=button)


    def checkPos(self, position):
        if not (position[0] > self.position[0] and position[0] < self.position[0] + self.position[2]): return False
        if not (position[1] > self.position[1] and position[1] < self.position[1] + self.position[3]): return False

        return True

    def click(self, position):
        if self.checkPos(position) :
            print("click", self.text)
            self.callback()
            self.style["background"] = (255,255,255)

    def hover(self, position):
        if self.checkPos(position) and not self.hover:
            self.hover = True
            self.unhover = False

            self.background["after"] = self.background["old-background"]
            self.background["background"] = self.background["old-after"]
            self.background["text"] = (255,255,255)
        elif not self.checkPos(position) and not self.unhover:
            self.unhover = True
            self.hover = False

            self.background["after"] = self.background["old-after"]
            self.background["background"] = self.background["old-background"]
            self.background["text"] = self.background["old-text"]
        elif self.checkPos(position) and self.hover: pass
        elif not self.checkPos(position) and self.unhover: pass
