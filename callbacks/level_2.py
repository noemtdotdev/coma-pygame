import pygame
from classes.image import Image
from classes.cursor import Cursor
from classes.arrow import Arrow
from classes.lives import Lives
import random
import json

def level_2(main_screen):
    clock = pygame.time.Clock()
    screen_width, screen_height = 1792 // 1.5, 1121 // 1.5

    main_screen = pygame.display.set_mode((screen_width, screen_height))
    screen_surface = pygame.Surface((screen_width, screen_height))

    pygame.display.set_caption("Level 2 - Musik")

    font_path = "assets/font.ttf"
    font_size = 20
    font = pygame.font.Font(font_path, font_size)

    BUTTON_COLOR = (100, 100, 250)
    BUTTON_HOVER_COLOR = (150, 150, 255)
    BACKGROUND_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)

    pos_arrow_left = (359, 39)
    pos_arrow_top = (517, 44)
    pos_arrow_bottom = (517, 44)
    pos_arrow_right = (684, 37)

    ymin_top_arrow = 383
    ymin_other_arrows = 536

    arrows = []
    score = 0

    lives = Lives(3, pos=(screen_width - 17*12, screen_height - 16*4))

    cursor = Cursor()
    overlay_image = Image("assets/overlay_level_2.png", (screen_width, screen_height)).image

    running = True
    while running:
        screen_surface.fill(BACKGROUND_COLOR)
        screen_surface.blit(overlay_image, (0, 0))

        screen_surface.blit(lives.image, lives.rect)

        mouse_pos = pygame.mouse.get_pos()
        ok_button = pygame.Rect(screen_width - 60, 20, 40, 40)

        if ok_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen_surface, BUTTON_HOVER_COLOR, ok_button)
            cursor.set_hand_cursor()
        else:
            pygame.draw.rect(screen_surface, BUTTON_COLOR, ok_button)

        ok_text = font.render("X", True, TEXT_COLOR)
        ok_text_rect = ok_text.get_rect(center=ok_button.center)
        screen_surface.blit(ok_text, ok_text_rect)

        if len(arrows) < 4 and random.randint(1, 40) == 1:
            direction = random.choice(["left", "up", "down", "right"])
            if direction == "left":
                arrow = Arrow(direction, pos_arrow_left)
            elif direction == "up":
                arrow = Arrow(direction, pos_arrow_top)
            elif direction == "down":
                arrow = Arrow(direction, pos_arrow_bottom)
            elif direction == "right":
                arrow = Arrow(direction, pos_arrow_right)
            arrows.append(arrow)

        for arrow in arrows:
            arrow.update()
            arrow.rect.y += 6
            screen_surface.blit(arrow.image, arrow.rect)

        arrows_to_remove = []
        keys = pygame.key.get_pressed()

        for arrow in arrows:
            if arrow.type != "up":
                if arrow.rect.top > ymin_other_arrows - 100:
                    if (arrow.type == "left" and keys[pygame.K_LEFT]) or \
                       (arrow.type == "down" and keys[pygame.K_DOWN]) or \
                       (arrow.type == "right" and keys[pygame.K_RIGHT]):
                        score += 1
                        arrows_to_remove.append(arrow)
            else:
                if arrow.rect.top > ymin_top_arrow - 100:
                    if keys[pygame.K_UP]:
                        score += 1
                        arrows_to_remove.append(arrow)

        for arrow in arrows:
            if (arrow.type == "up" and arrow.rect.top > ymin_top_arrow) or \
               (arrow.type != "up" and arrow.rect.top > ymin_other_arrows):
                lives.decrement_lives()
                arrows.remove(arrow)

        for arrow in arrows_to_remove:
            if not arrow in arrows:
                continue
            arrows.remove(arrow)

        lives.update()

        if lives.lives <= 0:
            running = False

        elif score >= 60:
            with open("levels.json", "r") as file:
                levels_data = json.load(file)["levels"]

            levels_data[2]["unlocked"] = True
            levels_data[1]["completed"] = True

            with open("levels.json", "w") as file:
                json.dump({"levels": levels_data}, file)

            running = False

        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen_surface.blit(score_text, (20, 20))

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
    level_2(main_screen)
    pygame.quit()