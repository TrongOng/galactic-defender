import pygame
import math
from alien import Alien

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circular Movement")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ship properties
ship_radius = 25
ship_speed = 2
angle = 0

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLACK)

    # Draw the ship
    ship_x = WIDTH // 2 + int(math.cos(math.radians(angle)) * (WIDTH // 4))
    ship_y = HEIGHT // 2 + int(math.sin(math.radians(angle)) * (HEIGHT // 4))
    pygame.draw.circle(screen, WHITE, (ship_x, ship_y), ship_radius)

    # Update angle for circular movement
    angle += ship_speed
    if angle >= 360:
        angle = 0

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
