import pygame
import sys
from pygame.locals import *
from libs.EventEmitter import EventEmitter

class Event():
    def __init__(self):
        self.event = EventEmitter()

    def on(self, name, callback): self.event.on(name, callback)

    
    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit();
            if event.type == pygame.MOUSEBUTTONDOWN : self.event.emit("MOUSEBUTTONDOWN", event.pos)
            if event.type == pygame.MOUSEMOTION : self.event.emit("MOUSEMOTION", event.pos)



event = Event()