import pygame
import math

class Flask(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        
        self.sprite_sheet = pygame.image.load("assets/flasks.png").convert_alpha()
        
        self.frame_width = 128
        self.frame_height = 128
        
        self.type = color
        self.color = color

        row, col = self.offset()
        self.frames = self.load_frames(row, col)
        self.current_frame = 0
        self.animation_speed = 0.1
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.original_pos = pygame.math.Vector2(x, y)
        self.shake_angle = 0
        self.shake_direction = 0.25
        self.selected = False
        self.target_pos = pygame.math.Vector2(964, 220)
        

    def offset(self):
        if self.color == "clear":
            row, col = 3, 3
        elif self.color == "red":
            row, col = 3, 7
        elif self.color == "blue":
            row, col = 8, 3
        elif self.color == "green":
            row, col = 8, 7
        else:
            raise ValueError("Invalid color")
        return row, col

    def load_frames(self, row, col):
        frames = []
        for i in range(4):
            x = col * self.frame_width
            y = row * self.frame_height
            frame = self.sprite_sheet.subsurface((x, y, self.frame_width, self.frame_height))
            frame = pygame.transform.scale(frame, (self.frame_width, self.frame_height))
            frames.append(frame)
        return frames

    def animate(self):
        self.current_frame = (self.current_frame + self.animation_speed) % len(self.frames)
        self.image = self.frames[int(self.current_frame)]

    def update(self, mouse_pos):
        if self.color == "clear":
            return
        self.animate()
        if self.selected:
            self.rect.center = mouse_pos
            if self.color != "clear":
                self.rotate_towards_target()

    def rotate_towards_target(self):
        direction = self.target_pos - pygame.math.Vector2(self.rect.center)
        angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90
        self.image = pygame.transform.rotate(self.frames[int(self.current_frame)], angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def toggle_pause(self):
        self.selected = not self.selected
        if not self.selected:
            self.shake_angle = 0

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False
        self.shake_angle = 0
        self.rect.topleft = self.original_pos

    def set_color(self, color):
        self.color = color
        row, col = self.offset()
        self.frames = self.load_frames(row, col)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]

    def turn_clear_if_poured(self, empty_flask):
        if self.selected and self.rect.colliderect(empty_flask.rect):
            self.set_color("clear")

            self.frames = self.load_frames(3, 3)
            self.current_frame = 0
            self.image = self.frames[self.current_frame]

            self.deselect()

    def __del__(self):
        self.sprite_sheet = None
        self.frames = None