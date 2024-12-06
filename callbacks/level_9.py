import pygame
import random
from classes.image import Image
import json

def level_9(main_screen):
    pygame.init()
    clock = pygame.time.Clock()
    screen_width, screen_height = 1792 // 1.5, 1121 // 1.5
    main_screen = pygame.display.set_mode((screen_width, screen_height))
    screen_surface = pygame.Surface((screen_width, screen_height))
    pygame.display.set_caption("Level 9 - Memory")

    font_path = "assets/font.ttf"
    font_size = 20
    try:
        font = pygame.font.Font(font_path, font_size)
    except FileNotFoundError:
        font = pygame.font.SysFont(None, font_size)

    BUTTON_COLOR = (100, 100, 250)
    BUTTON_HOVER_COLOR = (150, 150, 255)
    BACKGROUND_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)
    CARD_BACK_COLOR = (6, 65, 26)
    CARD_FRONT_COLOR = (6, 96, 26)

    card_size = 100
    card_margin = 10
    rows, cols = 6, 6
    words = [
        "Zelle", 
        "DNA", 
        "Gen", 
        "Klon", 
        "Enzym", 
        "RNA", 
        "Virus", 
        "Bakterium", 
        "Chromosom", 
        "Protein", 
        "Krebs", 
        "Säuger", 
        "Blut", 
        "Hormon", 
        "Zucker", 
        "Mutter", 
        "Nerv", 
        "Mark"
    ]
    card_values = words * 2
    random.shuffle(card_values)

    x_offset = (screen_width - (cols * card_size + (cols - 1) * card_margin)) // 2
    y_offset = (screen_height - (rows * card_size + (rows - 1) * card_margin)) // 2
    
    cards = []
    for row in range(rows):
        for col in range(cols):
            x = col * (card_size + card_margin) + card_margin + x_offset
            y = row * (card_size + card_margin) + card_margin + y_offset
            card_rect = pygame.Rect(x, y, card_size, card_size)
            card_value = card_values.pop()
            cards.append({"rect": card_rect, "value": card_value, "flipped": False, "matched": False})

    flipped_cards = []
    matched_pairs = 0
    game_phase = "waiting_for_input"
    phase_start_time = 0
    flip_delay = 1000

    overlay_image = Image("assets/overlay_level_9.png", (screen_width, screen_height)).image

    running = True
    while running:
        screen_surface.fill(BACKGROUND_COLOR)
        screen_surface.blit(overlay_image, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        exit_button = pygame.Rect(screen_width - 60, 20, 40, 40)
        if exit_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen_surface, BUTTON_HOVER_COLOR, exit_button)
        else:
            pygame.draw.rect(screen_surface, BUTTON_COLOR, exit_button)

        exit_text = font.render("X", True, TEXT_COLOR)
        exit_text_rect = exit_text.get_rect(center=exit_button.center)
        screen_surface.blit(exit_text, exit_text_rect)

        for card in cards:
            if card["flipped"] or card["matched"]:
                pygame.draw.rect(screen_surface, CARD_FRONT_COLOR, card["rect"])
                value_text = font.render(card["value"], True, TEXT_COLOR)
                value_text_rect = value_text.get_rect(center=card["rect"].center)
                screen_surface.blit(value_text, value_text_rect)
            else:
                pygame.draw.rect(screen_surface, CARD_BACK_COLOR, card["rect"])

        if game_phase == "game_over":
            with open("levels.json", "r") as file:
                levels_data = json.load(file)["levels"]

            levels_data[9]["unlocked"] = True
            levels_data[8]["completed"] = True

            with open("levels.json", "w") as file:
                json.dump({"levels": levels_data}, file)

            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and game_phase == "waiting_for_input":
                if exit_button.collidepoint(mouse_pos):
                    running = False
                else:
                    for card in cards:
                        if card["rect"].collidepoint(mouse_pos) and not card["flipped"] and not card["matched"]:
                            card["flipped"] = True
                            flipped_cards.append(card)
                            if len(flipped_cards) == 2:
                                game_phase = "checking_match"
                                phase_start_time = pygame.time.get_ticks()
                            break

        if game_phase == "checking_match":
            if pygame.time.get_ticks() - phase_start_time > flip_delay:
                if flipped_cards[0]["value"] == flipped_cards[1]["value"]:
                    flipped_cards[0]["matched"] = True
                    flipped_cards[1]["matched"] = True
                    matched_pairs += 1
                else:
                    flipped_cards[0]["flipped"] = False
                    flipped_cards[1]["flipped"] = False
                flipped_cards = []
                game_phase = "waiting_for_input"

        if matched_pairs == (rows * cols) // 2:
            game_phase = "game_over"

        main_screen.blit(screen_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    main_screen = pygame.display.set_mode((800, 600))
    level_9(main_screen)
    pygame.quit()
