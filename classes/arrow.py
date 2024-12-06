import pygame

class Arrow(pygame.sprite.Sprite):
    def __init__(self, type, pos):
        super().__init__()

        self.type = type

        self.sprite_sheet = pygame.image.load("assets/arrows.png").convert_alpha()

        self.frame_width = 170
        self.frame_height = 170

        self.image = self.load_frame(type)

        self.image = pygame.transform.scale(self.image, (150, 150))

        self.rect = self.image.get_rect()
        self.set_position(*pos)


    def load_frame(self, type):
        x = 0
        y = 0
        if type == "up":
            x = 0
            y = 0
        elif type == "left":
            x = 170
            y = 0
        elif type == "down":
            x = 340
            y = 0
        elif type == "right":
            x = 510
            y = 0
        frame = self.sprite_sheet.subsurface((x, y, self.frame_width, self.frame_height))
        frame = pygame.transform.scale(frame, (self.frame_width * 2, self.frame_height * 2))
        return frame
    
    def set_position(self, x, y):
        self.rect.topleft = (x, y)

    def update(self):
        pass

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1300, 600))
    arrow = Arrow("down", (170, 170))
    arrow_group = pygame.sprite.Group(arrow)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                arrow.set_position(x, y)

        screen.fill((255, 255, 255))
        arrow_group.update()
        arrow_group.draw(screen)
        pygame.display.flip()
        clock.tick(60)