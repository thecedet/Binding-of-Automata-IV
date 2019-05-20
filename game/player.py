import pygame
from math import *
from game.projectile import Projectile

screenSize = [1280,960]


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.skin = pygame.image.load("src/texture/sprite-0.png").convert()
        self.skin.set_colorkey((0,0,0))
        self.skin.set_alpha(255)
        self.skin = pygame.transform.scale(self.skin, (game.scale*2, game.scale*2))
        self.rect = self.skin.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * game.scale
        self.y = y * game.scale

        self.direction = [0,0]
        self.last_shot = 0

    def getKeys(self):
        self.vx, self.vy = 0, 0

        if self.game.playing: 
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.vx = -self.game.playerSpeed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.vx = self.game.playerSpeed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.vy = -self.game.playerSpeed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.vy = self.game.playerSpeed
            if self.vx != 0 and self.vy != 0:
                self.vx *= 0.8; self.vy *= 0.8

            if keys[pygame.K_k]:
                self.x = 800
                self.y = 800
                

    def getMouse(self):
        self.mouse = pygame.mouse.get_pos()
        self.image = self.rot_center(self.skin,self.getAngle(self.mouse))

    def click(self):
    	mouse = list(pygame.mouse.get_pressed())
    	self.getMouse()
    	if mouse[0] and pygame.time.get_ticks() - self.last_shot > 500:
            Projectile(self.game, self, self.x,self.y, self.getAngle(self.mouse), "player")
            self.last_shot = pygame.time.get_ticks()

    def rot_center(self,image, angle):# Dirige limage du joueur vers la souris
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, 0-90-angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def getAngle(self,tpos): 
        pos = list(tpos)
        if screenSize[0]/2-pos[0] == 0 : # Sert à éviter les divisions pas 0
            pos[0] = pos[0] + 1
        elif screenSize[1]/2-pos[1] == 0 :
            pos[1] = pos[1] + 1
       
        if screenSize[0]/2-pos[0] < 0 :
            angle = degrees(atan((screenSize[1]/2-pos[1])/(screenSize[0]/2-pos[0])))
        else:
            angle = 180+degrees(atan((screenSize[1]/2-pos[1])/(screenSize[0]/2-pos[0])))
        return angle # Retourne l'angle du joueur


    def collision(self, dir):
        wallHits = pygame.sprite.spritecollide(self, self.game.walls, False)
        eventHits = pygame.sprite.spritecollide(self, self.game.event, False)
        
        if dir == 'x':  
            if wallHits:
                if self.vx > 0:self.x = wallHits[0].rect.left - self.rect.width
                if self.vx < 0:self.x = wallHits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            if wallHits:
                if self.vy > 0:
                    self.y = wallHits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = wallHits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y


        if eventHits: eventHits[0].event()

    def update(self):
        self.getKeys()
        self.getMouse()
        self.click()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collision('x')
        self.rect.y = self.y
        self.collision('y')
