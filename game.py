import pygame
import random
import sys

# Game configuration
WIDTH, HEIGHT = 400, 600
FPS = 60
BUCKET_WIDTH = 60
BUCKET_HEIGHT = 25
ITEM_SIZE = 25
ITEM_DROP_INTERVAL = 900  # milliseconds
MAX_LIVES = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUCKET_COLOR = (30, 144, 255)
RIM_COLOR = (135, 206, 250)
TEXT_COLOR = (255, 255, 255)
RED = (255, 0, 0)

# Falling item colors
ITEM_COLORS = [
    (255, 215, 0),   # Gold
    (255, 69, 0),    # OrangeRed
    (0, 255, 127),   # Spring Green
    (138, 43, 226),  # BlueViolet
    (255, 105, 180)  # Hot Pink
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bucket Star Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Load or use dummy sounds
try:
    catch_sound = pygame.mixer.Sound("s.mp3")
    miss_sound = pygame.mixer.Sound("s.mp3")
except:
    catch_sound = miss_sound = None

def draw_text(text, x, y, color=TEXT_COLOR):
    rendered = font.render(text, True, color)
    screen.blit(rendered, (x, y))

def draw_bucket(x, y):
    # Rim
    pygame.draw.rect(screen, RIM_COLOR, (x, y, BUCKET_WIDTH, BUCKET_HEIGHT // 4))
    # Body
    pygame.draw.rect(screen, BUCKET_COLOR, (x + 5, y + BUCKET_HEIGHT // 4, BUCKET_WIDTH - 10, BUCKET_HEIGHT))

def draw_falling_item(x, y, color):
    pygame.draw.ellipse(screen, color, (x, y, ITEM_SIZE, ITEM_SIZE))

def game_loop():
    bucket_x = WIDTH // 2 - BUCKET_WIDTH // 2
    bucket_y = HEIGHT - BUCKET_HEIGHT - 10
    score = 0
    lives = MAX_LIVES
    items = []
    item_timer = pygame.time.get_ticks()
    speed = 3

    running = True
    while running:
        screen.fill(BLACK)

        # Handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            bucket_x -= 6
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            bucket_x += 6

        bucket_x = max(0, min(WIDTH - BUCKET_WIDTH, bucket_x))

        # Add new item
        if pygame.time.get_ticks() - item_timer > ITEM_DROP_INTERVAL:
            item_x = random.randint(0, WIDTH - ITEM_SIZE)
            color = random.choice(ITEM_COLORS)
            items.append([item_x, 0, color])
            item_timer = pygame.time.get_ticks()

        # Move items
        for item in items[:]:
            item[1] += speed
            item_rect = pygame.Rect(item[0], item[1], ITEM_SIZE, ITEM_SIZE)
            bucket_rect = pygame.Rect(bucket_x, bucket_y, BUCKET_WIDTH, BUCKET_HEIGHT)

            if item_rect.colliderect(bucket_rect):
                items.remove(item)
                score += 1
                print("Catch!")
                if catch_sound:
                    catch_sound.play()
            elif item[1] > HEIGHT:
                items.remove(item)
                lives -= 1
                print("Miss!")
                if miss_sound:
                    miss_sound.play()

        # Increase difficulty
        if score > 0 and score % 10 == 0:
            speed = 3 + score // 5

        # Draw bucket
        draw_bucket(bucket_x, bucket_y)

        # Draw items
        for item in items:
            draw_falling_item(item[0], item[1], item[2])

        # Draw score and lives
        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Lives: {lives}", WIDTH - 120, 10)

        pygame.display.flip()
        clock.tick(FPS)

        # Handle events
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
