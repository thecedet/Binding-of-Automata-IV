import pygame
import sys
from pygame.locals import *


class Component():
    def __init__(self,style):
        self.setCSS(style)

    def getCurrentSize(self):
        if self.parent == None : return (0,0,pygame.display.Info().current_w, pygame.display.Info().current_h)
        else: return self.parent.position

    def setCSS(self, style):
        if not "width" in style.keys(): style["width"] = "100%"
        if not "height" in style.keys(): style["height"] = "100%"
        if not "top" in style.keys(): style["top"] = "0%"
        if not "left" in style.keys(): style["left"] = "0%"
        if not "background" in style.keys(): style["background"] = None
        if not "padding" in style.keys(): style["padding"] = (10,10,10,10)
        if not "color" in style.keys(): style["color"] = (0,0,0)
        if not "font-family" in style.keys() : style["font-family"] = "monospace"
        if not "font-bold" in style.keys() : style["font-bold"] = False
        if not "font-size" in style.keys() : style["font-size"] = 15
        if not "shadow" in style.keys() : style["shadow"] = None
        if not "align-y" in style.keys() : None
        else: style["top"] = "50%"


        self.style = style
        self.setPosition(style)

    def setPosition(self,style):
        width = self.peutetre(self.style["width"], 2)
        height = self.peutetre(self.style["height"], 3)
        left = self.peutetre(self.style["left"], 2) + self.getCurrentSize()[0]
        top = self.peutetre(self.style["top"], 3) + self.getCurrentSize()[1]

        if "align-y" in self.style.keys(): top -= height/2

        self.position = (left,top,width,height)

    def peutetre(self, value, truc):

        if("%" in str(value)):
            return int(self.getCurrentSize()[truc]*int(value.split("%")[0])/100)
        elif("px" in str(value)):
            return int(self.getCurrentSize()[truc]/int(value.split("px")[0]))
        elif("height" in str(value)):
            return int( 100*self.peutetre(self.style["height"], 3)/self.getCurrentSize()[2] )
        elif("width" in str(value)):
            return int( 100*self.peutetre(self.style["width"], 2)/self.getCurrentSize()[3] )
        else:
            return int(self.getCurrentSize()[truc]*value)
