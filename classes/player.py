import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height=144, pos=(100, 0), lower_bound = 500):
        super().__init__()
        self.WIDTH = width
        self.HEIGHT = height
        self.ratio = self.HEIGHT / 144
        
        self.sprite_sheet = pygame.image.load("assets/player.png").convert_alpha()
        
        self.frame_width = 144
        self.frame_height = 144
        
        self.idle_frames = self.load_frames(0, 4)
        self.run_frames = self.load_frames(1, 6)
        self.jump_frames = {
            "crouch": self.load_frames(2, 2),
            "takeoff": self.load_frames(2, 1, 2),
            "ascend": self.load_frames(2, 2, 3),
            "peak": self.load_frames(3, 1, 0),
            "descend": self.load_frames(3, 2, 1),
            "land": self.load_frames(4, 2)
        }
        
        self.current_frame = 0
        self.image = self.idle_frames[self.current_frame]
        self.rect = self.image.get_rect()
        
        self.pos = pygame.math.Vector2(*pos)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        
        self.on_ground = False
        self.gravity = 1
        self.jump_strength = -15
        self.speed = 1
        self.friction = -0.2
        self.jump_phase = None
        self.direction = "right"
        self.lower_bound = lower_bound

    def load_frames(self, row, num_frames, start_col=0):
        frames = []
        for i in range(num_frames):
            x = (start_col + i) * self.frame_width
            y = row * self.frame_height
            frame = self.sprite_sheet.subsurface((x, y, self.frame_width, self.frame_height))
            frame = pygame.transform.scale(frame, (int(self.frame_width * self.ratio), self.HEIGHT))
            frames.append(frame)
        return frames

    def jump(self):
        if self.on_ground:
            self.vel.y = self.jump_strength
            self.on_ground = False
            self.jump_phase = "crouch"

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        
        self.acc = pygame.math.Vector2(0, self.gravity)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -self.speed
            self.animate("run")
            if self.direction != "left":
                self.direction = "left"
                self.image = pygame.transform.flip(self.image, True, False)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = self.speed
            self.animate("run")
            if self.direction != "right":
                self.direction = "right"
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.animate("idle")
        
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            self.jump()

    def update(self):
        self.handle_keys()
        
        self.acc.x += self.vel.x * self.friction
        
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        self.rect.midbottom = self.pos

        if self.pos.y >= self.lower_bound:
            self.pos.y = self.lower_bound
            self.vel.y = 0
            self.on_ground = True
            self.jump_phase = None
        else:
            self.update_jump_phase()
            self.on_ground = False

        if self.rect.left < -80:
            self.rect.left = -80
            self.pos.x = self.rect.midbottom[0]
            self.vel.x = 0
        elif self.rect.right > self.WIDTH + 80:
            self.rect.right = self.WIDTH + 80
            self.pos.x = self.rect.midbottom[0]
            self.vel.x = 0

    def update_jump_phase(self):
        if self.vel.y < -10:
            self.jump_phase = "ascend"
        elif -10 <= self.vel.y <= -1:
            self.jump_phase = "peak"
        elif self.vel.y > 1:
            self.jump_phase = "descend"
        elif self.vel.y == 0 and not self.on_ground:
            self.jump_phase = "land"
        
        if self.jump_phase:
            self.animate(self.jump_phase)

    def animate(self, action):
        if action == "idle":
            self.current_frame = (self.current_frame + 0.1) % len(self.idle_frames)
            frame = self.idle_frames[int(self.current_frame)]
        elif action == "run":
            self.current_frame = (self.current_frame + 0.2) % len(self.run_frames)
            frame = self.run_frames[int(self.current_frame)]
        elif action in self.jump_frames:
            frames = self.jump_frames[action]
            self.current_frame = (self.current_frame + 0.2) % len(frames)
            frame = frames[int(self.current_frame)]
        
        if self.direction == "left":
            self.image = pygame.transform.flip(frame, True, False)
        else:
            self.image = frame

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def move_down(self, pixels):
        self.pos.y += pixels
        self.rect.midbottom = self.pos

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1300, 600))
    player = Player(1300, height=72)  # Example with a different height
    player_group = pygame.sprite.Group(player)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player_group.update()

        screen.fill((30, 30, 30))
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()