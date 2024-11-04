import pygame
from .callback import Callback
from .cursor import Cursor

class Button:
    def __init__(self, x, y, width, height, label, unlocked, font, lock_image, screen, completed, info_button=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.unlocked = unlocked
        self.font = font
        self.lock_image = lock_image
        self.shake_offset = 0
        self.shaking = False

        self.BUTTON_COLOR = (100, 100, 250)
        self.HOVER_COLOR = (150, 150, 255)
        self.LOCK_COLOR = (70, 70, 70)
        self.LOCK_HOVER_COLOR = (50, 50, 50)
        self.TEXT_COLOR = (255, 255, 255)
        self.completed = completed

        self.COMPLETED_COLOR = (175, 145, 70)
        self.COMPLETED_HOVER_COLOR = (222, 189, 104)

        self.main_screen = screen
        self.cursor = Cursor()
        self.info_button = info_button


    def draw(self, screen, mouse_pos):

        if self.rect.collidepoint(mouse_pos):
            self.cursor.set_hand_cursor()
        else:
            self.cursor.default()
        
        if self.unlocked and not self.completed:
            color = self.HOVER_COLOR if self.rect.collidepoint(mouse_pos) else self.BUTTON_COLOR
        elif self.completed:
            color = self.COMPLETED_HOVER_COLOR if self.rect.collidepoint(mouse_pos) else self.COMPLETED_COLOR
        else:
            color = self.LOCK_HOVER_COLOR if self.rect.collidepoint(mouse_pos) else self.LOCK_COLOR

        rect = self.rect.copy()
        if self.shaking:
            self.shake_offset = (self.shake_offset + 1) % 8 - 4
            rect.x += self.shake_offset
            if abs(self.shake_offset) < 1:
                self.shaking = False
                self.shake_offset = 0

        pygame.draw.rect(screen, color, rect)

        label_surface = self.font.render(self.label, True, self.TEXT_COLOR)
        label_rect = label_surface.get_rect(center=(rect.x + rect.width // 2, rect.y + rect.height // 2))

        if self.unlocked and not self.info_button:
            screen.blit(label_surface, label_rect)
        else:
            combined_width = label_surface.get_width() + self.lock_image.get_width() + 10
            label_rect.x = rect.x + (rect.width - combined_width) // 2
            lock_x = label_rect.right + 10

            screen.blit(label_surface, label_rect)
            screen.blit(self.lock_image, (lock_x + 3, label_rect.y - 5))

    def handle_click(self):
        if self.unlocked:
            Callback(self.label, self.main_screen)
            return True
        else:
            self.shaking = True
            return False

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
