import pygame
import random
import sys

# Game configuration
WIDTH, HEIGHT = 400, 600
FPS = 60
BUCKET_WIDTH = 60
BUCKET_HEIGHT = 20
STAR_SIZE = 20
STAR_DROP_INTERVAL = 1000  # milliseconds
MAX_LIVES = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
STAR_COLOR = (255, 255, 0)
BUCKET_COLOR = (0, 150, 255)
TEXT_COLOR = (255, 255, 255)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bucket Star Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Sound effects (replace with custom sounds if desired)
catch_sound = pygame.mixer.Sound(pygame.mixer.Sound(file="s.mp3"))
miss_sound = pygame.mixer.Sound(pygame.mixer.Sound(file="s.mp3"))

def draw_text(text, x, y, color=TEXT_COLOR):
    rendered = font.render(text, True, color)
    screen.blit(rendered, (x, y))

def game_loop():
    bucket_x = WIDTH // 2 - BUCKET_WIDTH // 2
    bucket_y = HEIGHT - BUCKET_HEIGHT - 10
    score = 0
    lives = MAX_LIVES
    stars = []
    star_timer = pygame.time.get_ticks()
    speed = 3

    running = True
    while running:
        screen.fill(BLACK)

        # Handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            bucket_x -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            bucket_x += 5

        bucket_x = max(0, min(WIDTH - BUCKET_WIDTH, bucket_x))

        # Add new star
        if pygame.time.get_ticks() - star_timer > STAR_DROP_INTERVAL:
            stars.append([random.randint(0, WIDTH - STAR_SIZE), 0])
            star_timer = pygame.time.get_ticks()

        # Move stars
        for star in stars[:]:
            star[1] += speed
            star_rect = pygame.Rect(star[0], star[1], STAR_SIZE, STAR_SIZE)
            bucket_rect = pygame.Rect(bucket_x, bucket_y, BUCKET_WIDTH, BUCKET_HEIGHT)
            if star_rect.colliderect(bucket_rect):
                stars.remove(star)
                score += 1
                print("Catch!")
                pygame.mixer.Sound.play(catch_sound)
            elif star[1] > HEIGHT:
                stars.remove(star)
                lives -= 1
                print("Miss!")
                pygame.mixer.Sound.play(miss_sound)

        # Increase difficulty
        if score > 0 and score % 10 == 0:
            speed = 4 + score // 10

        # Draw bucket
        pygame.draw.rect(screen, BUCKET_COLOR, (bucket_x, bucket_y, BUCKET_WIDTH, BUCKET_HEIGHT))

        # Draw stars
        for star in stars:
            pygame.draw.rect(screen, STAR_COLOR, (*star, STAR_SIZE, STAR_SIZE))

        # Draw score and lives
        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Lives: {lives}", WIDTH - 110, 10)

        pygame.display.flip()
        clock.tick(FPS)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if lives <= 0:
            break

    return score

def game_over_screen(score):
    screen.fill(BLACK)
    draw_text("Game Over!", WIDTH // 2 - 80, HEIGHT // 2 - 60, RED)
    draw_text(f"Final Score: {score}", WIDTH // 2 - 90, HEIGHT // 2 - 20)
    draw_text("Press R to Restart or Q to Quit", WIDTH // 2 - 160, HEIGHT // 2 + 30)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Main loop
while True:
    final_score = game_loop()
    game_over_screen(final_score)
