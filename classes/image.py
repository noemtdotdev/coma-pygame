import pygame

class Image(pygame.sprite.Sprite):
    def __init__(self, path, size):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, size)
