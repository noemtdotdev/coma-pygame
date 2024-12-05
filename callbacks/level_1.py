import pygame
from classes.image import Image
from classes.cursor import Cursor
import json

def level_1(main_screen):
    clock = pygame.time.Clock()
    screen_width, screen_height = 1792 // 1.5, 1121 // 1.5
    
    main_screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Level 1 - Labyrinth")

    font_path = "assets/font.ttf"
    font_size = 20
    font = pygame.font.Font(font_path, font_size)

    BUTTON_COLOR = (100, 100, 250)
    BUTTON_HOVER_COLOR = (150, 150, 255)
    BACKGROUND_COLOR = (30, 30, 30)

    cursor = Cursor()

    player_size = 10
    player_color = (255, 255, 255)
    player_rect = pygame.Rect(1260, 560, player_size, player_size)
    player_speed = 5

    portal_size = 20
    portal_color = (0, 255, 0)
    portal_rect = pygame.Rect(350, screen_height // 2 - 30, portal_size, portal_size)

    overlay_image = Image("assets/overlay_level_1.png", (screen_width, screen_height)).image

    running = True
    while running:
        screen_surface = pygame.Surface((screen_width, screen_height))
        screen_surface.fill(BACKGROUND_COLOR)
        screen_surface.blit(overlay_image, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        pygame.draw.rect(screen_surface, player_color, player_rect)
        pygame.draw.rect(screen_surface, portal_color, portal_rect)

        ok_button = pygame.Rect(screen_width - 60, 20, 40, 40)

        if ok_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen_surface, BUTTON_HOVER_COLOR, ok_button)
            cursor.set_hand_cursor()
        else:
            pygame.draw.rect(screen_surface, BUTTON_COLOR, ok_button)

        ok_text = font.render("X", True, (255, 255, 255))
        ok_text_rect = ok_text.get_rect(center=ok_button.center)
        screen_surface.blit(ok_text, ok_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.colliderect(portal_rect):
                    with open("levels.json", "r") as file:
                        levels_data = json.load(file)["levels"]

                    levels_data[1]["unlocked"] = True
                    levels_data[0]["completed"] = True

                    with open("levels.json", "w") as file:
                        json.dump({"levels": levels_data}, file)

                    running = False

                if ok_button.collidepoint(mouse_pos):
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed

        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed

        if keys[pygame.K_UP]:
            player_rect.y -= player_speed

        if keys[pygame.K_DOWN]:
            player_rect.y += player_speed

        if player_rect.colliderect(portal_rect) or not screen_surface.get_rect().contains(player_rect):
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