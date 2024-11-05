import pygame
from classes.image import Image
from classes.cursor import Cursor
from classes.flask import Flask
import json

def level_2(main_screen):
    clock = pygame.time.Clock()
    screen_width, screen_height = 1300, 600
    screen_surface = pygame.Surface((screen_width, screen_height))
    pygame.display.set_caption("Level 2 - Chemiezimmer")

    font_path = "assets/font.ttf"
    font_size = 20
    font = pygame.font.Font(font_path, font_size)

    BUTTON_COLOR = (100, 100, 250)
    BUTTON_HOVER_COLOR = (150, 150, 255)
    BACKGROUND_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)

    cursor = Cursor()

    red_flask = Flask("red", 300, 200)
    blue_flask = Flask("blue", 400, 202)
    green_flask = Flask("green", 500, 204)
    empty_flask = Flask("clear", 900, 210)

    flasks = [red_flask, blue_flask, green_flask, empty_flask]
    selected_flask = None

    running = True
    while running:
        screen_surface.fill(BACKGROUND_COLOR)

        mouse_pos = pygame.mouse.get_pos()
        ok_button = pygame.Rect(screen_width - 60, 20, 40, 40)

        if ok_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen_surface, BUTTON_HOVER_COLOR, ok_button)
            cursor.set_hand_cursor()
        else:
            pygame.draw.rect(screen_surface, BUTTON_COLOR, ok_button)

        overlay_image = Image("assets/overlay_level_2.png", (1300, 600)).image
        screen_surface.blit(overlay_image, (0, 0))

        ok_text = font.render("X", True, TEXT_COLOR)
        ok_text_rect = ok_text.get_rect(center=ok_button.center)
        screen_surface.blit(ok_text, ok_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button.collidepoint(mouse_pos):
                    running = False

                for flask in flasks:
                    if flask.rect.collidepoint(mouse_pos):

                        if flask != empty_flask and not selected_flask:
                            flask.toggle_pause()
                            
                            if flask.selected:
                                flask.select()
                                selected_flask = flask

                            else:
                                flask.deselect()
                                flask.rect.topleft = flask.original_pos
                                selected_flask = None

                            for other_flask in flasks:
                                if other_flask != flask:
                                    other_flask.selected = False
                                    other_flask.deselect()

                        elif selected_flask:

                            selected_flask.turn_clear_if_poured(empty_flask)
                            selected_flask = None


        flask_hovered = False
        for flask in flasks:
            flask.update(mouse_pos)
            screen_surface.blit(flask.image, flask.rect)
            if flask.rect.collidepoint(mouse_pos):
                flask_hovered = True

        if flask_hovered or ok_button.collidepoint(mouse_pos):
            cursor.set_hand_cursor()
        else:
            cursor.default()

        main_screen.blit(screen_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    main_screen = pygame.display.set_mode((1300, 600))
    level_2(main_screen)
    pygame.quit()