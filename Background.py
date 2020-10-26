import pygame


class Background():
    def __init__(self, image):
        self.image = image
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("AI")

    def update(self):
        self.screen.blit(self.image, self.rect)
