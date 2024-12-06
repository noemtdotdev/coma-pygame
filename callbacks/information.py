import pygame
from count_lines import count_lines
from classes.cursor import Cursor


def render_text_with_underline(surface, text, font, color, x, y):
    words = text.split(' ')
    offset_x = x
    for word in words:
        if word.startswith('__') and word.endswith('__'):
            word = word[2:-2]
            word_surface = font.render(word, True, color)
            word_rect = word_surface.get_rect(topleft=(offset_x, y))
            surface.blit(word_surface, word_rect)
            underline_rect = pygame.Rect(word_rect.left, word_rect.bottom, word_rect.width, 1)
            pygame.draw.rect(surface, color, underline_rect)
        else:
            word_surface = font.render(word, True, color)
            word_rect = word_surface.get_rect(topleft=(offset_x, y))
            surface.blit(word_surface, word_rect)
        offset_x += word_rect.width + font.size(' ')[0]

def show_information(main_screen):

    clock = pygame.time.Clock()
    info_width, info_height = 1300, 600
    info_surface = pygame.Surface((info_width, info_height))
    pygame.display.set_caption("Informationen über das Spiel")
    cursor = Cursor()

    BACKGROUND_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)
    BUTTON_COLOR = (100, 100, 250)
    BUTTON_HOVER_COLOR = (150, 150, 255)

    font_path = "assets/font.ttf"
    font_size = 32
    font = pygame.font.Font(font_path, font_size)
    small_font = pygame.font.Font(font_path, 20)

    lines, files = count_lines()

    running = True
    while running:
        info_surface.fill(BACKGROUND_COLOR)

        text = font.render('Computermathematik 12/1 Klausur - "Projekt"', True, TEXT_COLOR)
        text_rect = text.get_rect(center=(info_width // 2, 50))
        info_surface.blit(text, text_rect)

        texts = [
            "Entwickelt mit PyGame von Dennis.",
            "Konzepte wurden von Shani erstellt.",
            f"Das Projekt beinhaltet {files} Python-Dateien mit insgesamt __{lines}__ Zeilen Code.",
            "Mit der Programmierung am Projekt wurde am __04.11.2024__ begonnen.",
            "Beendet wurde das Spiel am __06.11.2024__",
            "",
            "com.noemt.dev | com.dennis.beer"
        ]

        y_offset = 100
        for text in texts:
            render_text_with_underline(info_surface, text, small_font, TEXT_COLOR, 50, y_offset)
            y_offset += 30

        mouse_pos = pygame.mouse.get_pos()
        ok_button = pygame.Rect(info_width // 2 - 200 // 2, info_height - 100, 200, 80)
        if ok_button.collidepoint(mouse_pos):
            pygame.draw.rect(info_surface, BUTTON_HOVER_COLOR, ok_button)
            cursor.set_hand_cursor()
        else:
            pygame.draw.rect(info_surface, BUTTON_COLOR, ok_button)
            cursor.default()

        ok_text = font.render("Okay", True, TEXT_COLOR)
        ok_text_rect = ok_text.get_rect(center=(ok_button.center[0], ok_button.center[1]-2))
        info_surface.blit(ok_text, ok_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button.collidepoint(mouse_pos):
                    running = False

        main_screen.blit(info_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    main_screen = pygame.display.set_mode((1300, 600))
    show_information(main_screen)
    pygame.quit()
