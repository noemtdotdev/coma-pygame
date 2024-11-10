import pygame
from classes.player import Player
from classes.portal import Portal
from classes.image import Image
from classes.cursor import Cursor
import json

def level_1(main_screen):
    clock = pygame.time.Clock()
    screen_width, screen_height = 1300, 600
    
    main_screen = pygame.display.set_mode((screen_width, screen_height))
    screen_surface = pygame.Surface((screen_width, screen_height))
    
    pygame.display.set_caption("Level 1 - Tutorial")

    font_path = "assets/font.ttf"
    font_size = 20
    font = pygame.font.Font(font_path, font_size)

    BUTTON_COLOR = (100, 100, 250)
    BUTTON_HOVER_COLOR = (150, 150, 255)
    BACKGROUND_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)

    player = Player(screen_width)
    portal = Portal()
    player_group = pygame.sprite.Group(player)
    portal_group = pygame.sprite.Group(portal)

    cursor = Cursor()

    running = True
    while running:
        screen_surface.fill(BACKGROUND_COLOR)

        player_group.update()
        portal_group.update()

        player_group.draw(screen_surface)
        portal_group.draw(screen_surface)

        mouse_pos = pygame.mouse.get_pos()
        ok_button = pygame.Rect(screen_width - 60, 20, 40, 40)

        if ok_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen_surface, BUTTON_HOVER_COLOR, ok_button)
            cursor.set_hand_cursor()
        else:
            pygame.draw.rect(screen_surface, BUTTON_COLOR, ok_button)

        overlay_image = Image("assets/overlay_level_1.png", (screen_width, screen_height)).image
        screen_surface.blit(overlay_image, (0, 0))

        ok_text = font.render("X", True, TEXT_COLOR)
        ok_text_rect = ok_text.get_rect(center=(ok_button.center[0], ok_button.center[1]-2))
        screen_surface.blit(ok_text, ok_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollideany(player, portal_group):
                    with open("levels.json", "r") as file:
                        levels_data = json.load(file)["levels"]

                    levels_data[1]["unlocked"] = True
                    levels_data[0]["completed"] = True

                    with open("levels.json", "w") as file:
                        json.dump({"levels": levels_data}, file)

                    running = False

                if ok_button.collidepoint(mouse_pos):
                    running = False

        if pygame.sprite.spritecollideany(player, portal_group):
            cursor.set_hand_cursor()
        elif not ok_button.collidepoint(mouse_pos):
            cursor.default()

        main_screen.blit(screen_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    main_screen = pygame.display.set_mode((1300, 600))
    level_1(main_screen)
    pygame.quit()