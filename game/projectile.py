
import pygame
from math import *

class Projectile(pygame.sprite.Sprite):

 #--------------INIT---------------------------------------------------------------------------   
    def __init__(self,game, parent, x, y, angle, patern = "common", **kwargs):

        self.groups = game.allSprites# , game.projectiles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        pygame.mixer.Channel(1).play(pygame.mixer.Sound("src/music/shot.wav"))

        directory_list = ["src/texture/projectile_enemie.png","src/texture/explode.png","src/texture/bloc_all.png","src/texture/projectile_joueur.png"]
        sprite_list = []
		
        #for nbr_sprite in directory_list:
        #    sprite_list.append(pygame.image.load(nbr_sprite).convert())

        #for nbr_sprite in range (len(directory_list)):    
         #   sprite_list[nbr_sprite] = pygame.transform.scale(sprite_list[nbr_sprite], (20,20)) 



        self.parent = parent
        
        self.statut=["alive"]
        
        self.x = x
        self.y = y
        self.angle = angle * (3.14/180)
        self.state = 0
        self.patern = patern
        self.patern_list = { # Liste des diffÃ©rents types de projectiles
            "common" :{

                "speed" : 6,
                "sprite" : 0,
                "size" : 20
            },
            "explode" : {
                "speed" : 4,
                "sprite" : 1,
                "size": 35,
                "explode_in":  200, #random.randint(700,3000),
                "fragment":6
            },
            "player" : {
                "speed" : 14,
                "sprite" : 3,
                "size": 20,
            },
            "fast" : {
                "speed" : 12,
                "sprite" : 0,
                "size": 17,
            }  
        }

        self.size = self.patern_list[patern]["size"] # Chargement des Images
        #self.image = sprite_list[self.patern_list[patern]["sprite"]]
        self.image = pygame.image.load(directory_list[self.patern_list[patern]["sprite"]]).convert()
        self.image = pygame.transform.scale(self.image, (self.size,self.size))
        self.image.set_colorkey((0,0,0))
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()
        self.speed = self.patern_list[self.patern]["speed"]
        self.explode_in = self.patern_list["explode"]["explode_in"]


 #--------------MOVE---------------------------------------------------------------------------

    def move(self):
        self.x = self.x + self.speed * cos(self.angle)# 
        self.y = self.y + self.speed * sin(self.angle)# 
        self.state += 1
 #--------------EXPLODE-----------------------------------------------------------------------------------------
        if self.patern == "explode" and self.statut[0] != "dead": 
            self.speed = self.patern_list[self.patern]["speed"] *(1-(self.state/self.explode_in))
            if self.speed < 0.005:
                fragment = self.patern_list["explode"]["fragment"]
                self.statut[0] = "dead"

                for i in range(fragment):
                    Projectile(self.game,self.parent , self.x, self.y, i*(360/fragment) + self.angle, "common")
        self.rect.x = self.x +self.size/2
        self.rect.y = self.y +self.size/2

 #-----------------------------------------------------------------------------------------

    def collision(self, dir):
        hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            for hit in hits:
                if hit.breakable: self.game.walls.remove(hit); self.game.allSprites.remove(hit)
            self.game.allSprites.remove(self)



    
    
 #-----------------------------------------------------------------------------------------
    def update(self): #liste des actions a faire
        self.move()

        self.rect.x = self.x
        self.collision('x')
        self.rect.y = self.y
        self.collision('y')
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

