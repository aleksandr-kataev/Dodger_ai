import pygame
import random


class Barrel(pygame.sprite.Sprite):
    BLACK = (0, 0, 0)
    init_x = 1400
    init_y = 728

    base = 25

    def __init__(self, images):
        pygame.sprite.Sprite.__init__(self)
        self.scoreUpdated = False
        if random.random() < 0.5:
            self.image = images[0]
        else:
            self.image = images[1]
        self.image.set_colorkey(Barrel.BLACK)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = Barrel.init_x
        self.rect.y = Barrel.init_y
        self.base = Barrel.base
        self.height = Barrel.base
        self.y = Barrel.init_y - self.height
        self.velocity = random.randint(-8, -6)
        self.color = (0, 0, 0)

    def update(self):
        self.rect.x += self.velocity
        self.mask = pygame.mask.from_surface(self.image)

    def setSpeed(self, speed):
        self.speed = speed
