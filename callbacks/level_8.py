import pygame
import random
import json

from classes.cursor import Cursor
from classes.image import Image

def level_8(main_screen):
    clock = pygame.time.Clock()
    screen_width, screen_height = 1792 // 1.5, 1121 // 1.5

    main_screen = pygame.display.set_mode((screen_width, screen_height))
    screen_surface = pygame.Surface((screen_width, screen_height))

    pygame.display.set_caption("Level 8 - Kunst")

    font_path = "assets/font.ttf"
    font_size = 20
    font = pygame.font.Font(font_path, font_size)

    BUTTON_COLOR = (100, 100, 250)
    BUTTON_HOVER_COLOR = (150, 150, 255)
    BACKGROUND_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)

    cursor = Cursor()
    overlay_image = Image("assets/overlay_level_8.png", (screen_width, screen_height)).image


    running = True
    while running:
        screen_surface.fill(BACKGROUND_COLOR)
        screen_surface.blit(overlay_image, (0, 0))


        mouse_pos = pygame.mouse.get_pos()
        ok_button = pygame.Rect(screen_width - 60, 20, 40, 40)

        if ok_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen_surface, BUTTON_HOVER_COLOR, ok_button)
            cursor.set_hand_cursor()
        else:
            pygame.draw.rect(screen_surface, BUTTON_COLOR, ok_button)

        ok_text = font.render("X", True, TEXT_COLOR)
        ok_text_rect = ok_text.get_rect(center=(ok_button.center[0], ok_button.center[1]-2))
        screen_surface.blit(ok_text, ok_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button.collidepoint(mouse_pos):
                    running = False

        if ok_button.collidepoint(mouse_pos):
            cursor.set_hand_cursor()
        else:
            cursor.default()

        main_screen.blit(screen_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    main_screen = pygame.display.set_mode((1300, 600))
    level_8(main_screen)
    pygame.quit()