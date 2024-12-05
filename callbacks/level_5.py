import pygame
import random
import time
import json

from classes.image import Image
from classes.cursor import Cursor

def level_5(main_screen):
    clock = pygame.time.Clock()
    screen_width, screen_height = 1792 // 1.5, 1121 // 1.5
    main_screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Level 5 - Schnelles Tippen")

    cursor = Cursor()

    BACKGROUND_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)
    CORRECT_COLOR = (0, 255, 0)
    INCORRECT_COLOR = (255, 0, 0)
    BUTTON_COLOR = (100, 100, 250)
    BUTTON_HOVER_COLOR = (150, 150, 255)
    FONT = pygame.font.Font("assets/font.ttf", 40)
    x_font = pygame.font.Font("assets/font.ttf", 20)

    with open("./assets/words.json", "r") as file:
        words = json.load(file)["words"]

    current_word_index = 0
    typed_text = ""
    score = 0
    start_time = time.time()
    game_duration = 60

    word_sequence = [random.choice(words) for _ in range(300)]
    word_sequence = [word.split(" ")[0] for word in word_sequence]

    overlay_image = Image("assets/overlay_level_5.png", (screen_width, screen_height)).image

    running = True
    while running:
        main_screen.fill(BACKGROUND_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        main_screen.blit(overlay_image, (0, 0))

        ok_button = pygame.Rect(screen_width - 60, 20, 40, 40)

        if ok_button.collidepoint(mouse_pos):
            pygame.draw.rect(main_screen, BUTTON_HOVER_COLOR, ok_button)
            cursor.set_hand_cursor()
        else:
            pygame.draw.rect(main_screen, BUTTON_COLOR, ok_button)

        ok_text = x_font.render("X", True, TEXT_COLOR)
        ok_text_rect = ok_text.get_rect(center=ok_button.center)
        main_screen.blit(ok_text, ok_text_rect)

        elapsed_time = time.time() - start_time
        remaining_time = game_duration - int(elapsed_time)

        if remaining_time <= 0:
            running = False

        y_offset = screen_height // 1.39
        x_offset = screen_width // 4.5
        boundary_x = screen_width - screen_width // 5

        for i, word in enumerate(word_sequence[current_word_index:current_word_index + 10]):
            color = TEXT_COLOR
            if i == 0:
                for j, char in enumerate(word):
                    if x_offset >= boundary_x:
                        break
                    if j < len(typed_text):
                        char_color = CORRECT_COLOR if typed_text[j] == char else INCORRECT_COLOR
                    else:
                        char_color = TEXT_COLOR
                    char_surface = FONT.render(char, True, char_color)
                    main_screen.blit(char_surface, (x_offset, y_offset))
                    x_offset += char_surface.get_width()
                x_offset += 20
            else:
                word_surface = FONT.render(word, True, color)
                if x_offset + word_surface.get_width() >= boundary_x:
                    break
                main_screen.blit(word_surface, (x_offset, y_offset))
                x_offset += word_surface.get_width() + 20

        timer_surface = FONT.render(f"Verbleibende Zeit: {remaining_time}s", True, TEXT_COLOR)
        main_screen.blit(timer_surface, (screen_width - 900, screen_height // 2.55))

        score_surface = x_font.render(f"{score}/30", True, TEXT_COLOR)
        main_screen.blit(score_surface, (screen_width // 1.293, screen_height // 1.227))

        if ok_button.collidepoint(mouse_pos):
            cursor.set_hand_cursor()
        else:
            cursor.default()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]
                elif event.key == pygame.K_SPACE:
                    if typed_text.strip() == word_sequence[current_word_index]:
                        score += 1
                    current_word_index += 1
                    typed_text = ""
                    if current_word_index >= len(word_sequence):
                        running = False
                elif event.unicode.isalpha() or event.unicode.isspace():
                    typed_text += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button.collidepoint(mouse_pos):
                    running = False

        pygame.display.flip()
        clock.tick(60)

    main_screen.fill(BACKGROUND_COLOR)

    if score >= 30:
        with open("levels.json", "r") as file:
            levels_data = json.load(file)["levels"]

        levels_data[5]["unlocked"] = True
        levels_data[4]["completed"] = True

        with open("levels.json", "w") as file:
            json.dump({"levels": levels_data}, file)

        running = False

    pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    main_screen = pygame.display.set_mode((800, 400))
    level_5(main_screen)
    pygame.quit()