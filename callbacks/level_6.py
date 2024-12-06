import pygame
from pygame_texteditor import TextEditor
import json

from classes.cursor import Cursor

class ConsoleWindow:
    def __init__(self, x, y, width, height, font, font_size, text_color, bg_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(font, font_size)
        self.text_color = text_color
        self.bg_color = bg_color
        self.lines = []

    def set_output(self, output_list):
        self.lines = []
        for line in output_list:
            self.lines.extend(self.wrap_text(line))

    def wrap_text(self, text):

        if not type(text) == str:
            text = str(text)

        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] < self.rect.width - 10:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        return lines

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        y_offset = 0
        for line in self.lines:
            text_surface = self.font.render(line, True, self.text_color)
            screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5 + y_offset))
            y_offset += text_surface.get_height()

def level_6(main_screen):
    pygame.init()

    clock = pygame.time.Clock()
    screen_width, screen_height = 1792 // 1.5, 1121 // 1.5
    main_screen = pygame.display.set_mode((screen_width, screen_height))
    screen_surface = pygame.Surface((screen_width, screen_height))

    pygame.display.set_caption("Level 6 - Informatik")

    font_path = "assets/font.ttf"
    font_size = 20
    font = pygame.font.Font(font_path, font_size)

    BUTTON_COLOR = (100, 100, 250)
    BUTTON_HOVER_COLOR = (150, 150, 255)
    BACKGROUND_COLOR = (19, 20, 17)
    TEXT_COLOR = (255, 255, 255)

    tasks = [
        "Erzeuge den output 'Hallo Welt!'",
        "Erzeuge den output ['1', '2', '3', ..., '50']",
        "Erzeuge die Summe der Zahlen 1 bis 100",
        "Generiere die ersten 10 Fibonacci-Zahlen",
        "Erstelle eine Liste der Quadratzahlen von 1 bis 10",
        "Zähle die Vokale im String 'Hallo, Welt!'",
        "Finde die größte Zahl in der Liste [3, 15, 8, 20, 7]",
        "Prüfe, ob 'racecar' ein Palindrom ist",
    ]

    solutions = [
        "Hallo Welt!",
        list(str(i) for i in range(1, 51)),
        sum(range(1, 101)),
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34],
        [1, 4, 9, 16, 25, 36, 49, 64, 81, 100],
        3,
        20,
        True,
    ]

    task = 0

    te = TextEditor(
        offset_x=100, offset_y=50, editor_width=screen_width - 200, editor_height=screen_height - 300, screen=screen_surface, syntax_highlighting_python=True
    )

    te.set_text_from_string("# Schreibe hier deinen Python-Code hinein!")

    console_width = screen_width - 300 - 140
    console = ConsoleWindow(120, screen_height - 230, console_width, 150, font_path, font_size, TEXT_COLOR, (50, 50, 50))
    ok_button = pygame.Rect(screen_width - 60, 20, 40, 40)
    run_button = pygame.Rect(screen_width - 300, screen_height - 230, 120, 40)

    cursor = Cursor()

    running = True
    while running:
        screen_surface.fill(BACKGROUND_COLOR)

        pygame_events = pygame.event.get()
        pressed_keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        te.display_editor(pygame_events, pressed_keys, *mouse_pos, mouse_pressed)

        if ok_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen_surface, BUTTON_HOVER_COLOR, ok_button)
        else:
            pygame.draw.rect(screen_surface, BUTTON_COLOR, ok_button)

        if run_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen_surface, BUTTON_HOVER_COLOR, run_button)
        else:
            pygame.draw.rect(screen_surface, BUTTON_COLOR, run_button)

        ok_text = font.render("X", True, TEXT_COLOR)
        ok_text_rect = ok_text.get_rect(center=(ok_button.center[0], ok_button.center[1]-2))
        screen_surface.blit(ok_text, ok_text_rect)

        run_text = font.render("Ausführen", True, TEXT_COLOR)
        run_text_rect = run_text.get_rect(center=(run_button.center[0], run_button.center[1]-2))
        screen_surface.blit(run_text, run_text_rect)

        if task >= len(tasks):
            with open("levels.json", "r") as file:
                levels_data = json.load(file)["levels"]

            levels_data[6]["unlocked"] = True
            levels_data[5]["completed"] = True

            with open("levels.json", "w") as file:
                json.dump({"levels": levels_data}, file)

            running = False

        task_text = font.render(tasks[task], True, TEXT_COLOR)
        task_text_rect = task_text.get_rect(center=(screen_width // 2, 20))
        screen_surface.blit(task_text, task_text_rect)

        for event in pygame_events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button.collidepoint(mouse_pos):
                    running = False
                elif run_button.collidepoint(mouse_pos):
                    content = te.get_text_as_string()
                    output = run_code(content)
                    console.set_output(output)
                    if type(output) == list:
                        if len(output) == 0:
                            continue
                        if output[0] == solutions[task]:
                            task += 1

        console.draw(screen_surface)
        main_screen.blit(screen_surface, (0, 0))

        if ok_button.collidepoint(mouse_pos) or run_button.collidepoint(mouse_pos):
            cursor.set_hand_cursor()
        else:
            cursor.default()
        
        pygame.display.flip()
        clock.tick(60)

def run_code(code: str):
    output = []
    print = output.append
    try:
        exec(code, globals(), locals())
        return output
    
    except Exception as e:
        return [str(e)]
    

if __name__ == "__main__":
    level_6(None)
    pygame.quit()