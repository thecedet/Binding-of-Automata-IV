import pygame
import sys
from pygame.locals import *
from window import Window
from libs.EventPygame import event



if __name__ == '__main__':
    window = Window()
    while True:
    	window.draw()
    	event.run()
