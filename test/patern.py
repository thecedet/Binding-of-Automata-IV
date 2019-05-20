import pygame
import random
from math import *
import math
from libs.EventPygame import event

#-----------------------------------------------------------------------------------------
class Projectile():
 #--------------INIT---------------------------------------------------------------------------   
    def __init__(self, sprite, parent, x, y, angle, patern = "common", **kwargs):
        self.parent = parent
        self.sprite_list = sprite
        self.statut=["alive"]
        
        self.x = x
        self.y = y
        self.angle = angle * (3.14/180)
        self.state = 0
        self.patern = patern
        self.patern_list = { # Liste des différents types de projectiles
            "common" :{

                "speed" : 0.3,
                "sprite" : 0,
                "size" : 20
            },
            "explode" : {
                "speed" : 0.15,
                "sprite" : 1,
                "size": 35,
                "explode_in": random.randint(700,3000),
                "fragment":6
            },
            "player" : {
                "speed" : 0.7,
                "sprite" : 3,
                "size": 17,
            },
            "fast" : {
                "speed" : 0.7,
                "sprite" : 0,
                "size": 17,
            }  
        }
        self.size = self.patern_list[patern]["size"] # Chargement des Images
        self.image = sprite_list[self.patern_list[patern]["sprite"]]
        self.image = pygame.transform.scale(self.image, (self.size,self.size))
        self.image.set_colorkey((0,0,0))
        self.image.set_alpha(255)
        self.speed = self.patern_list[self.patern]["speed"]
        self.explode_in = self.patern_list["explode"]["explode_in"]


 #--------------MOVE---------------------------------------------------------------------------

    def move(self, main,entity_list):
        self.x = self.x + self.speed * cos(self.angle)
        self.y = self.y + self.speed * sin(self.angle)
        self.state += 1
 #--------------EXPLODE-----------------------------------------------------------------------------------------
        if self.patern == "explode": 
            self.speed = self.patern_list[self.patern]["speed"] *(1-(self.state/self.explode_in))
            if self.speed < 0.005:
                fragment = self.patern_list["explode"]["fragment"]
                self.statut[0] = "dead"
                for i in range(fragment):
                    entity_list.append(Projectile(self.sprite_list, self.parent ,self.x, self.y, i*(360/fragment) + self.angle, "common"))
 #-----------------------------------------------------------------------------------------

        main.blit(self.image, (self.x,self.y))
 #-----------------------------------------------------------------------------------------
    def thingstodo(self, window, entity): #liste des actions a faire
        self.move(window, entity)



class Enemy():

    def __init__(self,sprite, x,y, **kwargs): 
        mob_list = {  # Liste des différents types d'ennemis
            "common" :{ 
                "speed" : 0.3,
                "hp" : 0,
                "dmg" : 20,
                "range" : 200,
                "attack_speed" : 2000,
                "sprite" : 2,
            },
            "explode" : {
                "speed" : 0.3,
                "hp" : 0,
                "dmg" : 20,
                "range" : 200,
                "attack_speed" : 2000,
                "sprite" : 2,
            },
            "fast" : {
                "speed" : 0.2,
                "hp" : 0,
                "dmg" : 20,
                "range" : 200,
                "attack_speed" : 1000,
                "sprite" : 2,
            }  
        }
        self.x = x #Initialisation des paramètres
        self.y = y
        self.statut=["alive"]
        self.type = kwargs.get("type", "common")
        self.sprite_list = sprite
        self.hp = kwargs.get("hp", mob_list[self.type]["hp"])
        self.hp = kwargs.get("speed", mob_list[self.type]["hp"])
        self.hp = kwargs.get("dmg", mob_list[self.type]["hp"])
        self.range = mob_list[self.type]["range"]
        self.speed = mob_list[self.type]["speed"]
        self.attack_speed = mob_list[self.type]["attack_speed"]
        self.skin = self.sprite_list[mob_list[self.type]["sprite"]]
        self.skin = pygame.transform.scale(self.skin, (40,40))
        self.skin.set_colorkey((0,0,0))
        self.skin.set_alpha(255)
        self.ready_to_shoot = True
        self.last_shot = 0
        self.direction = 0

    def sprite(self) :
         return self.rot_center(self.skin, self.getAngle(self.direction+90))

    def rot_center(self,image, angle): # Dirige limage de l'ennemi vers le joueur.....En cours
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, 0-90-angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def thingstodo(self, window, entity): #liste des actions a faire
        self.move(window)
        self.shoot(window, entity)

    def shoot(self,window, entity): # Tire un projectile
        if abs(pygame.time.get_ticks() - self.last_shot) > self.attack_speed:
            self.ready_to_shoot = True
        if self.distance < self.range + 20 and self.ready_to_shoot == True:
            entity.append(Projectile(self.sprite_list, self, self.x-20, self.y-20, self.direction+90, "explode"))
            self.ready_to_shoot = False
            self.last_shot = pygame.time.get_ticks()
            
    
    def move(self, window): # Se deplace vers le joueur
        
        if player.pos[0]-self.x < 0 :
            self.direction = degrees(math.atan((player.pos[1]-self.y)/(player.pos[0]-self.x))) +90
        else:
            self.direction = 180 + degrees(math.atan((player.pos[1]-self.y)/(player.pos[0]-self.x))) +90
            
        self.distance = sqrt((player.pos[1]-self.y)**2+(player.pos[0]-self.x)**2)
        if self.distance > self.range:
            self.x = self.speed*cos(self.direction) + self.x
            self.y = self.speed*sin(self.direction) + self.y
            
        window.blit(self.skin, (self.x-20 ,self.y-20))

class Player():

    def __init__(self, window, entity_list):

        event.on("KEYUP", self.keyRelease) # Association des évenements
        event.on("KEYDOWN", self.keyPress)
        event.on("MOUSEBUTTONDOWN",self.shoot)
        event.on("MOUSEMOTION",self.mousemotion)

        self.ult = "dash"  #Initialisation des paramètres
        self.window = window
        self.ammo_sprite = pygame.image.load("../src/texture/blocapastoucher.png").convert()
        self.ammo_sprite = pygame.transform.scale(self.ammo_sprite, (20,20))
        self.ult_ready  = pygame.image.load("../src/texture/ult_ready.png").convert()
        self.ult_ready = pygame.transform.scale(self.ult_ready, (40,40))
        self.ult_ready.set_colorkey((0,0,0))
        self.ult_ready.set_alpha(255)

        self.entity_list = entity_list
        self.pos = [100,100]
        self.last_pos = self.pos
        self.skin  = pygame.image.load("../src/texture/sprite-0.png").convert()
        self.skin.set_colorkey((0,0,0))
        self.skin.set_alpha(255)
        self.skin = pygame.transform.scale(self.skin, (80,80))
        self.direction = [0,0]

        self.ammo = 5
        self.begin_dash = -50
        self.last_date = pygame.time.get_ticks()


    def sprite(self) :
         return self.rot_center(self.skin, self.getAngle(self.last_pos))

    def rot_center(self,image, angle):# Dirige limage du joueur vers la souris
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, 0-90-angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def getAngle(self,tpos): # Retourne l'angle du joueur
        pos = list(tpos)
        if self.pos[0]-pos[0] == 0 :
            pos[0] = pos[0] + 1
        elif self.pos[1]-pos[1] == 0 :
            pos[1] = pos[1] + 1
       
        if self.pos[0]-pos[0] < 0 : # Sert à éviter les divisions pas 0
            angle = degrees(math.atan((self.pos[1]-pos[1])/(self.pos[0]-pos[0])))
        else:
            angle = 180+degrees(math.atan((self.pos[1]-pos[1])/(self.pos[0]-pos[0])))
        return angle

    def mousemotion(self,tpos): # MAJ la l'angle du joueur
        main.blit(self.rot_center(self.skin, self.getAngle(tpos)) , (self.pos[0]-40, self.pos[1]-40) )
        self.last_pos = list(tpos)


    def shoot(self,tpos): # Tire un projectile

        self.entity_list.append(Projectile(sprite_list, self, self.pos[0], self.pos[1], self.getAngle(tpos), "player"))
        
    
    def keyPress(self,key): # Change la direction du joueur ET utilise l'attaque spéciale
        
        speed = 0.6
        if key == 119 and self.direction[1] == 0:# UP : 273 ou 119
            self.direction[1] = -speed
        if key == 115 and self.direction[1] == 0:# DOWN : 274 ou 115
            self.direction[1] = speed
        if key == 97 and self.direction[0] == 0:# LEFT : 276 ou 97
            self.direction[0] = -speed
        if key == 100 and self.direction[0] == 0:# RIGHT : 275 ou 100
            self.direction[0] = speed
        if key ==32:
            if self.ult == "splash":
                           if self.ammo == 5:
                                self.ammo = 0
                                self.entity_list.append(Projectile(sprite_list,self, self.pos[0], self.pos[1], self.getAngle(pygame.mouse.get_pos()), "explode"))
            if self.ult =="dash":
                if self.ammo > 0 and abs(pygame.time.get_ticks() - self.begin_dash) > 50:
                    self.dash()
                    self.ammo -= 1



    def keyRelease(self,key): # Change la direction du joueur
        #global direction
        speed = 0.6
        if key == 119 and self.direction[1] == -speed: # UP : 273 ou 119
            self.direction[1] = 0
        if key == 115 and self.direction[1] == speed: # DOWN : 274 ou 115
            self.direction[1] = 0
        if key == 97 and self.direction[0] == -speed: # LEFT : 276 ou 97
           self.direction[0] = 0
        if key == 100 and self.direction[0] == speed: # RIGHT : 275 ou 100
            self.direction[0] = 0

    def move(self): # Déplace le joueur
        self.pos[0] += self.direction[0]
        self.pos[1] += self.direction[1]
        if abs(pygame.time.get_ticks() - self.begin_dash)<50 :
            self.pos[0] = self.pos[0] + 15 * cos(self.dash_dir)
            self.pos[1] = self.pos[1] + 15 * sin(self.dash_dir)
        

    def reload(self): # Jauge de rechargement de l'attaque spéciale
        
        if(pygame.time.get_ticks() - self.last_date > 2000 and self.ammo < 5):
            self.ammo += 1
            self.last_date = pygame.time.get_ticks()
        

        if self.ammo == 5:
            self.window.blit(self.ult_ready, (100 ,10))
            self.last_date = pygame.time.get_ticks()
            for am in range(self.ammo-1):
                self.window.blit(self.ammo_sprite,(10+am*20, 20))
        else:
            for am in range(self.ammo):
                self.window.blit(self.ammo_sprite,(10+am*20, 20))


    def thingstodo(self): #liste des actions a faire
        self.move()
        self.reload()
        self.window.blit( self.sprite(), (self.pos[0]-40 , self.pos[1]-40))

    def dash(self): # Ruée
        self.begin_dash = pygame.time.get_ticks()
        self.dash_dir = radians(self.getAngle(self.last_pos)+360)

#------------------------Initialisation---------------------------------------------------------------------------------------

pygame.init()
main = pygame.display.set_mode((1000,800)) # ,pygame.FULLSCREEN
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h

directory_list = ["../src/texture/projectile_enemie.png","../src/texture/explode.png","../src/texture/bloc_all.png","../src/texture/projectile_joueur.png"]
sprite_list = []
for nbr_sprite in directory_list:
    sprite_list.append(pygame.image.load(nbr_sprite).convert())
for nbr_sprite in range (len(directory_list)):    
    sprite_list[nbr_sprite] = pygame.transform.scale(sprite_list[nbr_sprite], (20,20)) 


entity_list = [] #Entity(sprite, 200, 600, 270, "explode")

entity_list.append(Enemy(sprite_list,400,400))
player = Player(main, entity_list)
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------Boucle------------------------------------------------------------------------------------------

while True:
    event.run()


    main.fill((109,106,99)) # Efface le fond

    
    player.thingstodo()#Fait les action du joueur
    #main.blit(rot_center(caracter,getAngle(last_pos)),(player_pos[0]-40,player_pos[1]-40))
    for i in entity_list:
        i.thingstodo(main, entity_list)# Fait les actions des entités

        if "dead" in i.statut or i.x<0 or i.x>width or i.y<0 or i.y>height: # Retire les entités hors de l'écran 
            entity_list.remove(i)

##  
##        clicked_sprites = [s for s in sprites if s.rect.collidepoint(pos)]
      
    pygame.display.flip()  
