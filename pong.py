# pong.py

import pygame
import random

# --- Constants ---
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Paddle dimensions
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
PADDLE_SPEED = 7

# Ball dimensions
BALL_SIZE = 15
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# --- Initialize Pygame ---
pygame.init()

# --- Create the Screen ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# --- Create Game Objects ---
# Paddles are Rectangles: (x, y, width, height)
player_paddle = pygame.Rect(SCREEN_WIDTH - PADDLE_WIDTH - 20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball is also a Rectangle
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Ball speed
ball_speed_x = BALL_SPEED_X * random.choice((-1, 1))
ball_speed_y = BALL_SPEED_Y * random.choice((-1, 1))

# Score
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 50) # Default font, size 50

# --- Game Functions ---
def handle_paddle_movement():
    """Moves the player's paddle based on key presses."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle.top > 0:
        player_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player_paddle.bottom < SCREEN_HEIGHT:
        player_paddle.y += PADDLE_SPEED

def handle_ball_movement():
    """Moves the ball and handles collisions."""
    global ball_speed_x, ball_speed_y, player_score, opponent_score

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top and bottom walls
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1

    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed_x *= -1

    # Scoring
    if ball.left <= 0:
        player_score += 1
        reset_ball()
    if ball.right >= SCREEN_WIDTH:
        opponent_score += 1
        reset_ball()

def reset_ball():
    """Resets the ball to the center with a random direction."""
    global ball_speed_x, ball_speed_y
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball_speed_x *= random.choice((-1, 1))
    ball_speed_y *= random.choice((-1, 1))

def draw_objects():
    """Draws all game objects on the screen."""
    # Fill the background with black
    screen.fill(BLACK)

    # Draw the paddles and the ball
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Draw the middle line
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    # Draw the score
    player_text = font.render(str(player_score), True, WHITE)
    screen.blit(player_text, (SCREEN_WIDTH // 2 + 20, 20))
    
    opponent_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(opponent_text, (SCREEN_WIDTH // 2 - 40, 20))

# --- The Main Game Loop ---
running = True
clock = pygame.time.Clock() # Clock for controlling frame rate

while running:
    # 1. Handle Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_paddle_movement()

    # 2. Update Game State
    handle_ball_movement()

    # Simple AI for the opponent
    if opponent_paddle.centery < ball.centery:
        opponent_paddle.y += PADDLE_SPEED - 3 # Make it slightly slower
    if opponent_paddle.centery > ball.centery:
        opponent_paddle.y -= PADDLE_SPEED - 3

    # 3. Draw Everything
    draw_objects()

    # Update the full display
    pygame.display.flip()

    # Control the frame rate (60 FPS)
    clock.tick(60)

# --- Quit Pygame ---
pygame.quit()