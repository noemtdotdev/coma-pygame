import pygame

class Portal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.sprite_sheet = pygame.image.load("assets/portal.png").convert_alpha()
        
        self.frame_width = 32
        self.frame_height = 32
        
        self.frames = self.load_frames(0, 3)
        self.frames.extend(self.load_frames(1, 3))

        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        self.set_position(1100, 200)
        
        self.frame_rate = 0.125

    def load_frames(self, row, num_frames, start_col=0):
        frames = []
        for i in range(num_frames):
            x = (start_col + i) * self.frame_width
            y = row * self.frame_height
            frame = self.sprite_sheet.subsurface((x, y, self.frame_width, self.frame_height))
            frame = pygame.transform.scale(frame, (self.frame_width * 6, self.frame_height * 6))
            frames.append(frame)
        return frames

    def animate(self):
        self.current_frame = (self.current_frame + self.frame_rate) % len(self.frames)
        frame = self.frames[int(self.current_frame)]
        self.image = frame

    def update(self):
        self.animate()

    def set_position(self, x, y):
        self.rect.topleft = (x, y)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1300, 600))
    portal = Portal()
    portal_group = pygame.sprite.Group(portal)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                portal.set_position(x, y)

        portal_group.update()

        screen.fill((30, 30, 30))
        portal_group.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()