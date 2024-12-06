import pygame
import random
import json

from classes.cursor import Cursor
from classes.item import Item
from classes.lives import Lives
from classes.image import Image
from classes.player import Player

import os

def level_7(main_screen):
    clock = pygame.time.Clock()
    screen_width, screen_height = 600, 800

    main_screen = pygame.display.set_mode((screen_width, screen_height))
    screen_surface = pygame.Surface((screen_width, screen_height))

    pygame.display.set_caption("Level 7 - Cafeteria")

    font_path = "assets/font.ttf"
    font_size = 20
    font = pygame.font.Font(font_path, font_size)

    BUTTON_COLOR = (100, 100, 250)
    BUTTON_HOVER_COLOR = (150, 150, 255)
    BACKGROUND_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)

    success_count = 0

    health_bar = Lives(3, (screen_width - 17*12, screen_height - 16*4))
    lives_sprites = pygame.sprite.Group()
    lives_sprites.add(health_bar)

    last_hurt_counter = 0

    cursor = Cursor()

    player = Player(width=screen_width, height=130, pos=(0, 0), lower_bound=screen_height-(130/144*16) - 10)
    player_group = pygame.sprite.Group()
    player_group.add(player)

    items = []
    item_pool = []

    def preload_items():
        for path in os.listdir("assets/items"):
            item = Item(path=path, width=80)
            if item.image.get_height() > 80:
                item.__init__(item.path, height=80)
            item_pool.append(item)

    def spawn_item():
        if item_pool:
            item = random.choice(item_pool)
            
            new_item = Item(path=item.path, width=80)
            if new_item.image.get_height() > 80:
                new_item.__init__(new_item.path, height=80)

            new_item.rect.x = random.randint(0, screen_width - 80)
            new_item.rect.y = -new_item.rect.height
            items.append(new_item)

    preload_items()
    spawn_item()

    ok_text = font.render("X", True, TEXT_COLOR)
    overlay_image = Image("assets/overlay_level_7.png", (screen_width, screen_height)).image

    running = True
    while running:
        screen_surface.fill(BACKGROUND_COLOR)
        screen_surface.blit(overlay_image, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        ok_button = pygame.Rect(screen_width - 60, 20, 40, 40)

        pygame.draw.rect(
            screen_surface,
            BUTTON_HOVER_COLOR if ok_button.collidepoint(mouse_pos) else BUTTON_COLOR,
            ok_button
        )

        player_group.update()
        player_group.draw(screen_surface)

        ok_text_rect = ok_text.get_rect(center=(ok_button.center[0], ok_button.center[1] - 2))
        screen_surface.blit(ok_text, ok_text_rect)

        screen_surface.blit(player.image, player.rect)

        pygame.draw.rect(screen_surface, (0, 0, 0), pygame.Rect(0, screen_height-4*16, screen_width, 4*16))

        lives_sprites.update()
        lives_sprites.draw(screen_surface)

        items_to_remove = []
        for item in items:
            screen_surface.blit(item.image, item.rect)
            item.rect.y += 5

            if item.rect.colliderect(player.rect):
                overlap_rect = item.rect.clip(player.rect)
                overlap_area = overlap_rect.width * overlap_rect.height
                item_area = item.rect.width * item.rect.height

                if overlap_area >= 0.6 * item_area:
                    items_to_remove.append(item)

                    if not item.positive:
                        current_hp = health_bar.lives
                        health_bar.decrement_lives()

                        last_hurt_counter = success_count

                        if current_hp <= 1:
                            running = False

                    else:
                        success_count += 1
                        if success_count - last_hurt_counter >= 10:
                            health_bar.increment_lives()
                            last_hurt_counter -= 5

            elif item.rect.y > screen_height:
                items_to_remove.append(item)

        for item in items_to_remove:
            items.remove(item)

        if random.randint(1, 30) == 1 and len(items) < 10:
            spawn_item()

        if success_count >= 30:
            with open("levels.json", "r") as file:
                levels_data = json.load(file)["levels"]

            levels_data[7]["unlocked"] = True
            levels_data[6]["completed"] = True

            with open("levels.json", "w") as file:
                json.dump({"levels": levels_data}, file)

            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and ok_button.collidepoint(mouse_pos):
                running = False

        cursor.set_hand_cursor() if ok_button.collidepoint(mouse_pos) else cursor.default()

        main_screen.blit(screen_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    main_screen = pygame.display.set_mode((1300, 600))
    level_7(main_screen)
    pygame.quit()