import pygame
import random
import json
from classes.image import Image
from classes.cursor import Cursor

def load_questions(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return list(data["physik"].items())

def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""
    
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] > max_width:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    lines.append(current_line)
    return lines

def level_10(main_screen):
    clock = pygame.time.Clock()
    screen_width, screen_height = 1792 // 1.5, 1121 // 1.5

    main_screen = pygame.display.set_mode((screen_width, screen_height))
    screen_surface = pygame.Surface((screen_width, screen_height))

    pygame.display.set_caption("Level 10 - Physik Quiz")

    font_path = "assets/font.ttf"
    font_size = 20
    font = pygame.font.Font(font_path, font_size)

    BACKGROUND_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)
    CORRECT_COLOR = (0, 200, 0)
    WRONG_COLOR = (200, 0, 0)
    BUTTON_COLOR = (100, 100, 250)
    BUTTON_HOVER_COLOR = (150, 150, 255)

    overlay_image = Image("assets/overlay_level_10.png", (screen_width, screen_height)).image

    questions = load_questions("assets/questions.json")
    random.shuffle(questions)
    selected_questions = questions[:6]

    question_index = 0
    correct_answers = 0
    feedback = None

    max_question_width = screen_width - 200
    answer_box_width = screen_width // 4
    answer_box_height = screen_height // 1.7
    answer_area_top = screen_height // 4 + 30

    cursor = Cursor()

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

        ok_text = font.render("X", True, TEXT_COLOR)
        ok_text_rect = ok_text.get_rect(center=(ok_button.center[0], ok_button.center[1] - 2))
        screen_surface.blit(ok_text, ok_text_rect)

        if question_index < len(selected_questions):
            question, answers = selected_questions[question_index]

            question_lines = wrap_text(question, font, max_question_width)
            for i, line in enumerate(question_lines):
                question_text = font.render(line, True, TEXT_COLOR)
                question_rect = question_text.get_rect(center=(screen_width // 1.88, 85 - i * 5 + i * 30))
                screen_surface.blit(question_text, question_rect)

            buttons = []
            num_answers = len([key for key in answers if key != "correct"])
            answer_spacing = (screen_width - num_answers * answer_box_width) // (num_answers + 1)

            for i, (key, answer) in enumerate(answers.items()):
                if key == "correct":
                    continue

                button_x = answer_spacing + i * (answer_box_width + answer_spacing)
                button_y = answer_area_top
                button_rect = pygame.Rect(button_x, button_y, answer_box_width, answer_box_height)
                buttons.append((button_rect, key))

                answer_lines = wrap_text(f"{key}: {answer}", font, answer_box_width - 20)
                for j, line in enumerate(answer_lines):
                    answer_text = font.render(line, True, TEXT_COLOR)
                    answer_rect = answer_text.get_rect(center=(button_rect.centerx, button_rect.height // 2 + button_y + j * 30 - j * 10))
                    screen_surface.blit(answer_text, answer_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not feedback:
                    if ok_button.collidepoint(event.pos):
                        running = False

                    for button_rect, key in buttons:
                        if button_rect.collidepoint(event.pos):
                            if key == answers["correct"]:
                                feedback = "Richtig!"
                                correct_answers += 1
                            else:
                                feedback = f"Falsch! Die richtige Antwort war: {answers[answers['correct']]}"
                            break

            if feedback:
                feedback_text = font.render(feedback, True, CORRECT_COLOR if feedback.startswith("Richtig") else WRONG_COLOR)
                feedback_rect = feedback_text.get_rect(center=(screen_width // 2, screen_height - 50))
                screen_surface.blit(feedback_text, feedback_rect)

                pygame.display.flip()
                pygame.time.wait(1500)
                feedback = None
                question_index += 1

            cursor_over_button = any(button_rect.collidepoint(mouse_pos) for button_rect, _ in buttons) or ok_button.collidepoint(mouse_pos)
            if cursor_over_button:
                cursor.set_hand_cursor()
            else:
                cursor.default()

        else:
            running = False

        main_screen.blit(screen_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    screen_surface.fill(BACKGROUND_COLOR)
    result_text = f"Du hast {correct_answers} von {len(selected_questions)} Fragen richtig beantwortet."
    if correct_answers >= 5:
        result_text += " Du hast gewonnen!"
        result_color = CORRECT_COLOR
        with open("levels.json", "r") as file:
            levels_data = json.load(file)["levels"]
            
        levels_data[9]["completed"] = True

        with open("levels.json", "w") as file:
            json.dump({"levels": levels_data}, file)

        running = False

    else:
        result_text += " Du hast verloren!"
        result_color = WRONG_COLOR

    result_surface = font.render(result_text, True, result_color)
    result_rect = result_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen_surface.blit(result_surface, result_rect)

    main_screen.blit(screen_surface, (0, 0))
    pygame.display.flip()
    pygame.time.wait(1500)

if __name__ == "__main__":
    pygame.init()
    try:
        main_screen = pygame.display.set_mode((1300, 600))
        level_10(main_screen)
    finally:
        pygame.quit()