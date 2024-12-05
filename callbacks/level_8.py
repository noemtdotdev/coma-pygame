import pygame
import random
from classes.image import Image

def level_8(main_screen):
    clock = pygame.time.Clock()
    screen_width, screen_height = 1792 // 1.5, 1121 // 1.5

    main_screen = pygame.display.set_mode((screen_width, screen_height))
    screen_surface = pygame.Surface((screen_width, screen_height))

    pygame.display.set_caption("Level 8 - Puzzle")

    font_path = "assets/font.ttf"
    font_size = 20
    font = pygame.font.Font(font_path, font_size)

    BUTTON_COLOR = (100, 100, 250)
    BUTTON_HOVER_COLOR = (150, 150, 255)
    BACKGROUND_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)
    BLOCK_COLOR = (255, 0, 0)
    GOAL_COLOR = (0, 255, 0)

    player_size = 20
    player_color = (255, 255, 255)
    player_rect = pygame.Rect(screen_width // 2 - player_size // 2, screen_height // 2 - player_size // 2, player_size, player_size)
    player_speed = 5

    block_size = 40
    blocks = [
        pygame.Rect(200, 200, block_size, block_size),
        pygame.Rect(300, 200, block_size, block_size),
        pygame.Rect(400, 200, block_size, block_size)
    ]

    goals = [
        pygame.Rect(200, 400, block_size, block_size),
        pygame.Rect(300, 400, block_size, block_size),
        pygame.Rect(400, 400, block_size, block_size)
    ]

    def reset_level():
        nonlocal player_rect, blocks
        player_rect = pygame.Rect(screen_width // 2 - player_size // 2, screen_height // 2 - player_size // 2, player_size, player_size)
        blocks = [
            pygame.Rect(200, 200, block_size, block_size),
            pygame.Rect(300, 200, block_size, block_size),
            pygame.Rect(400, 200, block_size, block_size)
        ]

    reset_level()

    overlay_image = Image("assets/overlay_level_8.png", (screen_width, screen_height)).image


    running = True
    while running:
        screen_surface.fill(BACKGROUND_COLOR)
        screen_surface.blit(overlay_image, (0, 0))


        mouse_pos = pygame.mouse.get_pos()
        restart_button = pygame.Rect(screen_width - 160, 20, 140, 40)

        if restart_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen_surface, BUTTON_HOVER_COLOR, restart_button)
        else:
            pygame.draw.rect(screen_surface, BUTTON_COLOR, restart_button)

        restart_text = font.render("Restart Puzzle", True, TEXT_COLOR)
        restart_text_rect = restart_text.get_rect(center=(restart_button.center[0], restart_button.center[1]-2))
        screen_surface.blit(restart_text, restart_text_rect)

        pygame.draw.rect(screen_surface, player_color, player_rect)

        for block in blocks:
            pygame.draw.rect(screen_surface, BLOCK_COLOR, block)

        for goal in goals:
            pygame.draw.rect(screen_surface, GOAL_COLOR, goal)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(mouse_pos):
                    reset_level()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
            for block in blocks:
                if player_rect.colliderect(block):
                    block.x -= player_speed
                    if block.colliderect(player_rect) or any(block.colliderect(other_block) for other_block in blocks if other_block != block):
                        block.x += player_speed
                    player_rect.x += player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < screen_width:
            player_rect.x += player_speed
            for block in blocks:
                if player_rect.colliderect(block):
                    block.x += player_speed
                    if block.colliderect(player_rect) or any(block.colliderect(other_block) for other_block in blocks if other_block != block):
                        block.x -= player_speed
                    player_rect.x -= player_speed
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed
            for block in blocks:
                if player_rect.colliderect(block):
                    block.y -= player_speed
                    if block.colliderect(player_rect) or any(block.colliderect(other_block) for other_block in blocks if other_block != block):
                        block.y += player_speed
                    player_rect.y += player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < screen_height:
            player_rect.y += player_speed
            for block in blocks:
                if player_rect.colliderect(block):
                    block.y += player_speed
                    if block.colliderect(player_rect) or any(block.colliderect(other_block) for other_block in blocks if other_block != block):
                        block.y -= player_speed
                    player_rect.y -= player_speed

        if all(any(block.colliderect(goal) for goal in goals) for block in blocks):
            print("Puzzle Solved!")
            running = False

        main_screen.blit(screen_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    main_screen = pygame.display.set_mode((1300, 600))
    level_8(main_screen)
    pygame.quit()