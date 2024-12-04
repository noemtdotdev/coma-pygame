import pygame
import random
import json

from classes.cursor import Cursor

def level_6(main_screen):
    clock = pygame.time.Clock()
    screen_width, screen_height = 1300, 600

    main_screen = pygame.display.set_mode((screen_width, screen_height))
    screen_surface = pygame.Surface((screen_width, screen_height))

    pygame.display.set_caption("Level 6 - Völkerball")

    font_path = "assets/font.ttf"
    font_size = 20
    font = pygame.font.Font(font_path, font_size)

    BUTTON_COLOR = (100, 100, 250)
    BUTTON_HOVER_COLOR = (150, 150, 255)
    BACKGROUND_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)

    cursor = Cursor()

    player_size = 20
    player_color = (255, 255, 255)
    player_rect = pygame.Rect(screen_width // 2 - player_size // 2, screen_height - player_size - 10, player_size, player_size)
    player_speed = 5

    dodgeball_size = 20
    dodgeball_color = (255, 0, 0)
    dodgeballs = []

    def spawn_dodgeball():
        x = random.randint(0, screen_width - dodgeball_size)
        y = -dodgeball_size
        dodgeballs.append(pygame.Rect(x, y, dodgeball_size, dodgeball_size))

    spawn_dodgeball()

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

        ok_text = font.render("X", True, TEXT_COLOR)
        ok_text_rect = ok_text.get_rect(center=(ok_button.center[0], ok_button.center[1]-2))
        screen_surface.blit(ok_text, ok_text_rect)

        # Draw the player
        pygame.draw.rect(screen_surface, player_color, player_rect)

        # Draw and update dodgeballs
        for dodgeball in dodgeballs:
            pygame.draw.rect(screen_surface, dodgeball_color, dodgeball)
            dodgeball.y += 5
            if dodgeball.colliderect(player_rect):
                running = False  # End the game if the player is hit
            if dodgeball.y > screen_height:
                dodgeballs.remove(dodgeball)

        # Spawn new dodgeballs
        if random.randint(1, 20) == 1:
            spawn_dodgeball()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button.collidepoint(mouse_pos):
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < screen_width:
            player_rect.x += player_speed
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < screen_height:
            player_rect.y += player_speed

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
    level_6(main_screen)
    pygame.quit()