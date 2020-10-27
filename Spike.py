import pygame
import random


class Spike(pygame.sprite.Sprite):
    RED = (255, 0, 0)
    init_x = 1400
    init_y = 728

    base = 25

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.scoreUpdated = False
        self.image = image
        self.image.set_colorkey(Spike.RED)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = Spike.init_x
        self.rect.y = Spike.init_y
        self.base = Spike.base
        self.height = Spike.base
        self.y = Spike.init_y - self.height
        self.velocity = random.randint(-8, -6)
        self.color = (0, 0, 0)

    def update(self):
        self.rect.x += self.velocity
        self.mask = pygame.mask.from_surface(self.image)

    def setSpeed(self, speed):
        self.speed = speed
