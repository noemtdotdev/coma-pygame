import pygame
import random

def level_7(main_screen):
    clock = pygame.time.Clock()
    screen_width, screen_height = 1300, 600

    main_screen = pygame.display.set_mode((screen_width, screen_height))
    screen_surface = pygame.Surface((screen_width, screen_height))

    pygame.display.set_caption("Level 7 - Cafetaria")

    font_path = "assets/font.ttf"
    font_size = 20
    font = pygame.font.Font(font_path, font_size)

    BUTTON_COLOR = (100, 100, 250)
    BUTTON_HOVER_COLOR = (150, 150, 255)
    BACKGROUND_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)
    FOOD_COLOR = (255, 0, 0)

    player_size = 20
    player_color = (255, 255, 255)
    player_rect = pygame.Rect(screen_width // 2 - player_size // 2, screen_height // 2 - player_size // 2, player_size, player_size)
    player_speed = 5

    food_size = 10
    food_items = []

    def spawn_food():
        x = random.randint(0, screen_width - food_size)
        y = random.randint(0, screen_height - food_size)
        food_items.append(pygame.Rect(x, y, food_size, food_size))

    for _ in range(10):
        spawn_food()

    food_stack = []

    running = True
    while running:
        screen_surface.fill(BACKGROUND_COLOR)

        mouse_pos = pygame.mouse.get_pos()
        ok_button = pygame.Rect(screen_width - 60, 20, 40, 40)

        if ok_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen_surface, BUTTON_HOVER_COLOR, ok_button)
        else:
            pygame.draw.rect(screen_surface, BUTTON_COLOR, ok_button)

        ok_text = font.render("X", True, TEXT_COLOR)
        ok_text_rect = ok_text.get_rect(center=(ok_button.center[0], ok_button.center[1]-2))
        screen_surface.blit(ok_text, ok_text_rect)

        # Draw the player
        pygame.draw.rect(screen_surface, player_color, player_rect)

        # Draw the food items
        for food in food_items:
            pygame.draw.rect(screen_surface, FOOD_COLOR, food)

        # Draw the food stack
        for i, food in enumerate(food_stack):
            food_rect = pygame.Rect(player_rect.x, player_rect.y - (i + 1) * food_size, food_size, food_size)
            pygame.draw.rect(screen_surface, FOOD_COLOR, food_rect)

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

        # Check for collision with food items
        for food in food_items[:]:
            if player_rect.colliderect(food):
                food_items.remove(food)
                if len(food_stack) < 30:
                    food_stack.append(food)

        main_screen.blit(screen_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    main_screen = pygame.display.set_mode((1300, 600))
    level_7(main_screen)
    pygame.quit()