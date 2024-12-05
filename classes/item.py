import pygame
import os
import random

positive_keywords = ["popcorn", "sandwich"]

class Item(pygame.sprite.Sprite):
    def __init__(self, path=None, width=None, height=None, directory="assets/items"):
        super().__init__()
        if path is None:
            path = self._choose_random_image(directory)
        
        self.path = path

        self.image = pygame.image.load(os.path.join(directory, path))
        image_height = self.image.get_height()
        image_width = self.image.get_width()

        self.positive = False
        for keyword in positive_keywords:
            if keyword in path:
                self.positive = True
                break
        
        if width:
            ratio = image_height / image_width
            height = int(width * ratio)
            self.image = pygame.transform.scale(self.image, (width, height))
        elif height:
            ratio = image_width / image_height
            width = int(height * ratio)
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = self.image.convert_alpha()

        self.rect = self.image.get_rect()

    def _choose_random_image(self, directory):
        items = os.listdir(directory)
        return os.path.join(random.choice(items))
