import pygame
import random
import os
import json

from classes.cursor import Cursor
from classes.image import Image

class PuzzlePiece(pygame.sprite.Sprite):
    def __init__(self, image_path, position, is_movable=True):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (self.original_image.get_width() // 3, self.original_image.get_height() // 3))
        self.rect = self.image.get_rect(topleft=position)
        self.is_movable = is_movable
        self.filename = os.path.basename(image_path)

    def update(self, pos, offset):
        if self.is_movable:
            self.rect.topleft = (pos[0] - offset[0], pos[1] - offset[1])

class TargetRect:
    def __init__(self, center):
        self.rect = pygame.Rect(center[0] - 15, center[1] - 15, 30, 30)

def load_puzzle_pieces(folder_path, prefix):
    pieces = []
    for filename in os.listdir(folder_path):
        if filename.startswith(prefix) and filename.endswith(".png"):
            pieces.append(os.path.join(folder_path, filename))
    return pieces

def level_8(main_screen):
    clock = pygame.time.Clock()
    screen_width, screen_height = int(1792 // 1.5), int(1121 // 1.5)
    # danke python // ist dafür da integer zu erzeugen ABER: ES BLEIBT NE FLOAT????

    main_screen = pygame.display.set_mode((screen_width, screen_height))
    screen_surface = pygame.Surface((screen_width, screen_height))

    pygame.display.set_caption("Level 8 - Kunst")

    font_path = "assets/font.ttf"
    font_size = 20
    font = pygame.font.Font(font_path, font_size)

    BUTTON_COLOR = (100, 100, 250)
    BUTTON_HOVER_COLOR = (150, 150, 255)
    BACKGROUND_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)

    cursor = Cursor()
    overlay_image = Image("assets/overlay_level_8.png", (screen_width, screen_height)).image

    puzzle_2_pieces = load_puzzle_pieces("assets/puzzles", "puzzle_2_")
    puzzle_1_pieces = load_puzzle_pieces("assets/puzzles", "puzzle_1_")
    puzzle_sprites = pygame.sprite.Group()

    target_rects = {
        "puzzle_2_1.png": TargetRect((746, 621)),
        "puzzle_2_2.png": TargetRect((617, 545)),
        "puzzle_2_3.png": TargetRect((700, 500)),
        "puzzle_2_4.png": TargetRect((583, 487)),
        "puzzle_2_5.png": TargetRect((626, 680)),
        "puzzle_2_6.png": TargetRect((702, 616)),
        "puzzle_2_7.png": TargetRect((609, 607)),

        "puzzle_1_1.png": TargetRect((94, 306)),
        "puzzle_1_2.png": TargetRect((202, 326)),
        "puzzle_1_3.png": TargetRect((294, 339)),
        "puzzle_1_4.png": TargetRect((400, 320)),
        "puzzle_1_5.png": TargetRect((400, 378)),
        "puzzle_1_6.png": TargetRect((94, 367)),
        "puzzle_1_7.png": TargetRect((146, 382)),
        "puzzle_1_8.png": TargetRect((105, 432)),
        "puzzle_1_9.png": TargetRect((73, 521)),
        "puzzle_1_10.png": TargetRect((132, 502)),
        "puzzle_1_11.png": TargetRect((226, 411)),
        "puzzle_1_12.png": TargetRect((218, 500)),
        "puzzle_1_13.png": TargetRect((415, 480)),
        "puzzle_1_14.png": TargetRect((316, 405)),
        "puzzle_1_15.png": TargetRect((337, 510)),
        "puzzle_1_16.png": TargetRect((317, 474)),
    }

    for i, piece_path in enumerate(puzzle_2_pieces):
        if i == 4:
            position = (screen_width // 2 - 50, screen_height - 100)
            piece = PuzzlePiece(piece_path, position, is_movable=False)
        else:
            position = (random.randint(0, screen_width - 100), random.randint(0, screen_height - 100))
            piece = PuzzlePiece(piece_path, position)
        puzzle_sprites.add(piece)

    for piece_path in puzzle_1_pieces:
        if "puzzle_1_8" in piece_path:
            position = (50, screen_height // 2)
            piece = PuzzlePiece(piece_path, position, is_movable=False)
        else:
            position = (random.randint(screen_width // 2, screen_width - 100), random.randint(0, screen_height // 2))
            piece = PuzzlePiece(piece_path, position)
        puzzle_sprites.add(piece)

    dragging_piece = None
    offset = (0, 0)

    running = True
    while running:
        screen_surface.fill(BACKGROUND_COLOR)
        screen_surface.blit(overlay_image, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        ok_button = pygame.Rect(screen_width - 60, 20, 40, 40)

        if ok_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen_surface, BUTTON_HOVER_COLOR, ok_button)
            cursor.set_hand_cursor()
        else:
            pygame.draw.rect(screen_surface, BUTTON_COLOR, ok_button)

        ok_text = font.render("X", True, TEXT_COLOR)
        ok_text_rect = ok_text.get_rect(center=(ok_button.center[0], ok_button.center[1]-2))
        screen_surface.blit(ok_text, ok_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button.collidepoint(mouse_pos):
                    running = False
                elif event.button == 1:
                    for piece in puzzle_sprites:
                        if piece.rect.collidepoint(mouse_pos) and piece.is_movable:
                            dragging_piece = piece
                            offset = (mouse_pos[0] - piece.rect.x, mouse_pos[1] - piece.rect.y)
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_piece = None

        if dragging_piece:
            dragging_piece.update(mouse_pos, offset)

        puzzle_sprites.draw(screen_surface)

        all_correct = True
        for piece in puzzle_sprites:
            piece_name = piece.filename
            if piece_name in target_rects:
                if not target_rects[piece_name].rect.collidepoint(piece.rect.center):
                    all_correct = False
                    break

        if all_correct:
            with open("levels.json", "r") as file:
                levels_data = json.load(file)["levels"]

            levels_data[8]["unlocked"] = True
            levels_data[7]["completed"] = True

            with open("levels.json", "w") as file:
                json.dump({"levels": levels_data}, file)

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
    level_8(main_screen)
    pygame.quit()