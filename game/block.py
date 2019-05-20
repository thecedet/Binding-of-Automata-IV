import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y,color, collision=True, event=False, passing=False, breakable=False):
        if collision: self.groups = game.walls, game.allSprites
        if event: self.groups = game.event, game.allSprites
        if passing: self.groups = game.passing

        self.breakable = breakable 


        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((self.game.scale, self.game.scale))
        self.image.fill( tuple(color) )
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x = x * self.game.scale
        self.rect.y = y * self.game.scale

    def event(self):
        Block(self.game, 30, 15, (255,255,255), passing=True)
