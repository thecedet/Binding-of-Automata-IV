import pygame
import json
from math import *

from game.block import Block
from game.player import Player

import socket
import json
import threading

screenSize = [1280,960]


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(screenSize[0] / 2)
        y = -target.rect.y + int(screenSize[1] / 2)
        self.camera = pygame.Rect(x, y, self.width, self.height)


class Game():
    def __init__(self, surface, level):
        self.surface = surface
        self.clock = pygame.time.Clock()
        
        self.playing = True

        pygame.mixer.Channel(0).play(pygame.mixer.Sound("src/music/main.ogg"))

        self.mapBuilder(level)
        self.init()

    def mapBuilder(self, level):
        data = json.load(open(level))

        self.maxX, self.maxY = 0, 0
        self.scale = data["scale"]
        self.data = data
        for block in data["blocks"]:
            if block["x"] + block["w"] > self.maxX: self.maxX = block["x"] + block["w"]
            if block["y"] + block["h"] > self.maxY: self.maxY = block["y"] + block["h"]

        self.width = self.maxX * self.scale
        self.height = self.maxY * self.scale

        self.playerSpeed = int(data["player"]["speed"])
        self.playerSpawn = data["player"]["spawn"]

    def init(self):

        self.allSprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.event = pygame.sprite.Group()
        self.passing = pygame.sprite.Group()
        self.projectile = pygame.sprite.Group()

        Block(self, 20, 15, (255,255,255), collision=False, event=True)

        for wall in self.data["blocks"]:
            for i in range(wall["w"]):
                for j in range(wall["h"]):
                    breakable = True if "breakable" in wall.keys() else False
                    Block(self, wall["x"]+i, wall["y"]+j, wall["color"], breakable=breakable)
        self.player = Player(self, self.playerSpawn[0], self.playerSpawn[1])
        self.camera = Camera(self.width, self.height)


    def run(self):
        self.dt = self.clock.tick(60) / 1000
        self.events()
        self.update()
        self.draw()


    def update(self):
        self.allSprites.update()
        self.passing.update()
        self.camera.update(self.player)
        
        

    def draw(self):
        self.surface.fill(tuple(self.data["background"]))
        for sprite in self.allSprites:
            self.surface.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.passing:
            self.surface.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.projectile:
            self.surface.blit(sprite.image, self.camera.apply(sprite))
        
        pygame.display.flip()

        self.passing = pygame.sprite.Group()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: pygame.quit()
                if event.key == pygame.K_m:
                    pygame.mixer.music.stop()

