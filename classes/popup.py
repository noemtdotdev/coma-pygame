import pygame

class Popup:
    def __init__(self, text, width, height):
        self.text = text
        self.width = width
        self.height = height
        self.font_path = "assets/font.ttf"
        self.font_size = 20
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.background_color = (50, 50, 50)
        self.text_color = (255, 255, 255)
        self.button_color = (200, 0, 0)
        self.button_hover_color = (255, 0, 0)
        self.button_text_color = (255, 255, 255)
        self.visible = True

    def draw(self, screen):
        if not self.visible:
            return

        popup_rect = pygame.Rect((screen.get_width() - self.width) // 2, (screen.get_height() - self.height) // 2, self.width, self.height)
        pygame.draw.rect(screen, self.background_color, popup_rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=popup_rect.center)
        screen.blit(text_surface, text_rect)

        close_button_rect = pygame.Rect(popup_rect.right - 30, popup_rect.top + 10, 20, 20)
        mouse_pos = pygame.mouse.get_pos()
        if close_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.button_hover_color, close_button_rect)
        else:
            pygame.draw.rect(screen, self.button_color, close_button_rect)

        close_text_surface = self.font.render("X", True, self.button_text_color)
        close_text_rect = close_text_surface.get_rect(center=close_button_rect.center)
        screen.blit(close_text_surface, close_text_rect)

        self.close_button_rect = close_button_rect

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_button_rect.collidepoint(event.pos):
                self.visible = False

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    popup = Popup("This is a popup!", 300, 200)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            popup.handle_event(event)

        screen.fill((30, 30, 30))
        popup.draw(screen)
        pygame.display.flip()

    pygame.quit()