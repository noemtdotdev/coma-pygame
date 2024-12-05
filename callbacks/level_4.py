import pygame
import random
import time
from classes.image import Image
from classes.cursor import Cursor
from classes.item import Item
import json

def generate_equation():
    operators = ['+', '-', '*', '/']


    operator = random.choice(operators)

    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)

    if operator == '/':
        while True:
            if num1 % num2 == 0:
                break
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)

    equation = f"{num1} {operator} {num2}"
    answer = int(eval(equation))
    return equation, str(answer)

def level_4(main_screen):
    clock = pygame.time.Clock()
    screen_width, screen_height = 1121 // 1.121 // 2, 1792 // 1.121 // 2
    main_screen = pygame.display.set_mode((screen_width, screen_height))
    screen_surface = pygame.Surface((screen_width, screen_height))
    pygame.display.set_caption("Level 4 - Mathematik")

    font_path = "assets/font.ttf"
    font_size = 20
    font = pygame.font.Font(font_path, font_size)

    BUTTON_COLOR = (100, 100, 250)
    BUTTON_HOVER_COLOR = (150, 150, 255)
    BACKGROUND_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)

    cursor = Cursor()

    equation, correct_answer = generate_equation()
    user_input = ""
    start_time = time.time()
    time_limit = 5

    index = 0

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

        overlay_image = Image("assets/overlay_level_4.png", (screen_width, screen_height)).image
        screen_surface.blit(overlay_image, (0, 0))

        ok_text = font.render("X", True, TEXT_COLOR)
        ok_text_rect = ok_text.get_rect(center=ok_button.center)
        screen_surface.blit(ok_text, ok_text_rect)

        equation_text = font.render(f'{equation} = ', True, TEXT_COLOR)
        equation_rect = equation_text.get_rect(center=(screen_width // 2.5, screen_height // 3.6))
        screen_surface.blit(equation_text, equation_rect)

        input_text = font.render(user_input, True, TEXT_COLOR)
        input_rect = input_text.get_rect(center=(screen_width // 1.5, screen_height // 3.6))
        screen_surface.blit(input_text, input_rect)

        elapsed_time = time.time() - start_time
        remaining_time = max(0, time_limit - elapsed_time)
        timer_text = font.render(f"Verbleibende Zeit: {int(remaining_time)}s", True, TEXT_COLOR)
        timer_rect = timer_text.get_rect(center=(screen_width // 2, screen_height // 11))
        screen_surface.blit(timer_text, timer_rect)

        if remaining_time <= 0:
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button.collidepoint(mouse_pos):
                    running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input == correct_answer:
                        equation, correct_answer = generate_equation()
                        index += 1
                        user_input = ""
                        start_time = time.time()

                    else:
                        user_input = ""
                        
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        if ok_button.collidepoint(mouse_pos):
            cursor.set_hand_cursor()
        else:
            cursor.default()

        main_screen.blit(screen_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    if index >= 20:
        with open("levels.json", "r") as file:
            levels_data = json.load(file)["levels"]

        levels_data[4]["unlocked"] = True
        levels_data[3]["completed"] = True

        with open("levels.json", "w") as file:
            json.dump({"levels": levels_data}, file)

        running = False

if __name__ == "__main__":
    pygame.init()
    main_screen = pygame.display.set_mode((1300, 873))
    level_4(main_screen)
    pygame.quit()