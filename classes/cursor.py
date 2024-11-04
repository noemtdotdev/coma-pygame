import pygame

class Cursor:
    def __init__(self):
        self.state = "none"
        self.default()

    def set_hand_cursor(self):
        if self.state == "hand":
            return
        pointer = pygame.image.load('assets/pointer.cur').convert_alpha()
        pointer = pygame.transform.scale(pointer, (32, 32))

        cursor_data = pygame.cursors.Cursor((0, 0), pointer)
        pygame.mouse.set_cursor(cursor_data)
        self.state = "hand"

    def default(self):
        if self.state == "default":
            return
        regular = pygame.image.load('assets/regular.cur').convert_alpha()
        regular = pygame.transform.scale(regular, (32, 32))

        cursor_data = pygame.cursors.Cursor((0, 0), regular)
        pygame.mouse.set_cursor(cursor_data)
        self.state = "default"