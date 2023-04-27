import pygame
import random


# Constants
WIDTH = 400
HEIGHT = 600
FPS = 60
GRAVITY = 0.6
JUMP_VELOCITY = -10
PIPE_GAP = 150
PIPE_SPEED = -4
PIPE_DELAY = 1500
PIPE_MIN_HEIGHT = 50
PIPE_MAX_HEIGHT = 350
BACKGROUND_COLOR = (100, 200, 255)
GROUND_COLOR = (218, 95, 7)
BIRD_COLOR = (255, 255, 0)
PIPE_COLOR = (0, 200, 0)
FONT_COLOR = (255, 255, 255)
FONT_SIZE = 40


# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()


# Load resources
font = pygame.font.SysFont(None, FONT_SIZE)
jump_sound = pygame.mixer.Sound("jump.wav")


# Classes
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BIRD_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT // 2 - self.rect.height // 2
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = JUMP_VELOCITY
        jump_sound.play()


class PipePair(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((100, HEIGHT))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.bottom_height = random.randint(PIPE_MIN_HEIGHT, PIPE_MAX_HEIGHT)
        self.bottom_pipe = pygame.Surface((100, self.bottom_height))
        self.bottom_pipe.fill(PIPE_COLOR)
        self.top_pipe = pygame.Surface((100, HEIGHT - self.bottom_height - PIPE_GAP))
        self.top_pipe.fill(PIPE_COLOR)
        self.image.blit(self.bottom_pipe, (0, HEIGHT - self.bottom_height))
        self.image.blit(self.top_pipe, (0, 0))

    def update(self):
        self.rect.x += PIPE_SPEED


# Functions
def draw_text(text, x, y):
    text_surface = font.render(text, True, FONT_COLOR)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


# Create sprites
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()
bird = Bird()
all_sprites.add(bird)


# Game loop
running = True
game_over = False
score = 0
pipe_delay = PIPE_DELAY
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird.jump()

    # Update sprites
    all_sprites.update()
    pipe_delay -= clock.get_time()
    if pipe_delay <= 0 and not game_over:
        pipe_delay = PIPE_DELAY
        pipe_pair = PipePair(WIDTH)
        all_sprites.add(pipe_pair)
        pipes.add(pipe_pair)

    for pipe in pipes:
        if pipe.rect.right < 0:
            pipes.remove(pipe)
            all_sprites.remove(pipe)
            score += 1

        if pygame.sprite.collide_rect(bird, pipe):
            game_over = True

        if pipe.rect.left == bird.rect.centerx:
            score += 1

    if bird.rect.bottom >= HEIGHT or bird.rect.top <= 0:
        game_over = True

    # Draw screen
    screen.fill(BACKGROUND_COLOR)
    all_sprites.draw(screen)
    draw_text(str(score), WIDTH // 2, 10)
    if game_over:
        draw_text("Game Over", WIDTH // 2, HEIGHT // 2)
    pygame.draw.rect(screen, GROUND_COLOR, (0, HEIGHT - 50, WIDTH, 50))
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()