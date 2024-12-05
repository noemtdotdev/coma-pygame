import pygame
from classes.image import Image
from classes.cursor import Cursor
import json

def level_1(main_screen):
    clock = pygame.time.Clock()
    screen_width, screen_height = (1792 // 1.5), (1016 // 1.5)
    
    main_screen = pygame.display.set_mode((screen_width, screen_height))
    screen_surface = pygame.Surface((screen_width, screen_height))
    
    pygame.display.set_caption("Level 1 - Labyrinth")

    font_path = "assets/font.ttf"
    font_size = 20
    font = pygame.font.Font(font_path, font_size)

    BUTTON_COLOR = (100, 100, 250)
    BUTTON_HOVER_COLOR = (150, 150, 255)
    BACKGROUND_COLOR = (30, 30, 30)

    cursor = Cursor()

    player_size = 10
    player_color = (0, 0, 0)
    player_rect = pygame.Rect(screen_width - 50, screen_height - 50, player_size, player_size)
    player_speed = 5

    portal_size = 20
    portal_color = (255, 0, 100)
    portal_rect = pygame.Rect(screen_width // 2.15, screen_height // 2.35, portal_size, portal_size)

    wall_thickness = 5

    def wall(length, horizontal, start):
        if horizontal:
            return pygame.Rect(*start, wall_thickness, length)
        return pygame.Rect(*start, length, wall_thickness)

    walls = [
        wall(screen_height, True, (0, 0)),
        wall(screen_width, False, (0, 0)),
        wall(screen_height, True, (screen_width - wall_thickness, 0)),
        wall(screen_width, False, (0, screen_height - wall_thickness)),
    ]

    overlay_image = Image("assets/overlay_level_1.png", (screen_width, screen_height)).image

    running = True
    while running:
        screen_surface.fill(BACKGROUND_COLOR)

        screen_surface.blit(overlay_image, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        pygame.draw.rect(screen_surface, player_color, player_rect)
        pygame.draw.rect(screen_surface, portal_color, portal_rect)
        
        for wall in walls:
            pygame.draw.rect(screen_surface, (0, 0, 0), wall)

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
            if player_rect.left < 0 or any(player_rect.colliderect(wall) for wall in walls):
                player_rect.x += player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed
            if player_rect.right > screen_width or any(player_rect.colliderect(wall) for wall in walls):
                player_rect.x -= player_speed
        if keys[pygame.K_UP]:
            player_rect.y -= player_speed
            if player_rect.top < 0 or any(player_rect.colliderect(wall) for wall in walls):
                player_rect.y += player_speed
        if keys[pygame.K_DOWN]:
            player_rect.y += player_speed
            if player_rect.bottom > screen_height or any(player_rect.colliderect(wall) for wall in walls):
                player_rect.y -= player_speed

        if player_rect.colliderect(portal_rect):
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