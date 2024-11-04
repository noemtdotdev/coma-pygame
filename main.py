import pygame
import json
import os

from classes.image import Image
from classes.button import Button
from classes.cursor import Cursor

pygame.init()

WIDTH, HEIGHT = 1300, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(Image('assets/icon.png', (32, 32)).image)

BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)

font_path = "assets/font.ttf"
font_size = 32
font = pygame.font.Font(font_path, font_size)

lock_image = Image('assets/lock.png', (40, 40)).image
cursor = Cursor()

def load_level_data():
    with open("levels.json", "r") as file:
        levels_data = json.load(file)
    return levels_data["levels"]

levels_data = load_level_data()
levels_file_path = "levels.json"
last_modified_time = os.path.getmtime(levels_file_path)

button_width, button_height = 230, 80
button_spacing = 20
buttons = []

for i in range(10):
    row = i // 5
    col = i % 5
    x = (WIDTH - (button_width * 5 + button_spacing * 4)) // 2 + col * (button_width + button_spacing)
    y = 200 + row * (button_height + button_spacing)
    unlocked = levels_data[i]["unlocked"]
    completed = levels_data[i]["completed"]
    button = Button(x, y, button_width, button_height, f"Level {i + 1}", unlocked, font, lock_image, screen, completed)
    buttons.append(button)

info_button = Button(
    WIDTH // 2 - 600 // 2,
    HEIGHT - 100,
    600,
    button_height,
    "Informationen",
    True,
    font,
    Image('assets/info.png', (40, 40)).image,
    screen,
    False,
    True
)
buttons.append(info_button)

running = True
clock = pygame.time.Clock()

while running:
    pygame.display.set_caption("Levelauswahl")

    screen.fill(BACKGROUND_COLOR)
    mouse_pos = pygame.mouse.get_pos()

    current_modified_time = os.path.getmtime(levels_file_path)
    if current_modified_time != last_modified_time:
        levels_data = load_level_data()
        last_modified_time = current_modified_time
        for i in range(10):
            if i < len(levels_data):
                buttons[i].unlocked = levels_data[i]["unlocked"]
                buttons[i].completed = levels_data[i]["completed"]

    text = font.render("Wähle ein Level aus", True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, 100))
    screen.blit(text, text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.is_hovered(mouse_pos):
                    button.handle_click()

    for button in buttons:
        button.draw(screen, mouse_pos)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()