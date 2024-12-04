import pygame

class Lives(pygame.sprite.Sprite):
    def __init__(self, lives=3, pos=(1100, 200)):
        super().__init__()

        self.lives = lives
        self.sprite_sheet = pygame.image.load("assets/hearts.png").convert_alpha()
        self.frame_width = 17
        self.frame_height = 16

        self.heart_full = self.load_frames(0, 1)[0]
        self.heart_used = self.load_frames(4, 1)[0]

        self.image = pygame.Surface((self.frame_width * 3 * 6, self.frame_height * 6), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        self.set_position(*pos)
        self.update()
    
    def load_frames(self, row, num_frames, start_col=0):
        frames = []
        for i in range(num_frames):
            x = (start_col + i) * self.frame_width
            y = row * self.frame_height
            frame = self.sprite_sheet.subsurface((x, y, self.frame_width, self.frame_height))
            frame = pygame.transform.scale(frame, (self.frame_width * 4, self.frame_height * 4))
            frames.append(frame)
        return frames

    def update(self):
        self.image.fill((0, 0, 0, 0))
        for i in range(3):
            if i < self.lives:
                self.image.blit(self.heart_full, (i * self.frame_width * 4, 0))
            else:
                self.image.blit(self.heart_used, (i * self.frame_width * 4, 0))

    def decrement_lives(self):
        if self.lives > 0:
            self.lives -= 1

    def increment_lives(self):
        if self.lives < 3:
            self.lives += 1

    def set_position(self, x, y):
        self.rect.topleft = (x, y)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1300, 600))
    pygame.display.set_caption("Lives Example")

    lives = Lives()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(lives)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    lives.decrement_lives()
                elif event.key == pygame.K_UP:
                    lives.increment_lives()

        lives.update()

        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
