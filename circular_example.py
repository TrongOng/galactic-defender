import pygame
import math

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

# Ship class
class Ship:
    def __init__(self, start_x, direction):
        self.x = start_x
        self.y = HEIGHT // 2
        self.direction = direction
    
    def update(self):
        global angle
        if self.direction == "right":
            self.x += ship_speed
            if self.x >= WIDTH // 2:
                self.direction = "circular"
        elif self.direction == "left":
            self.x -= ship_speed
            if self.x <= WIDTH // 2:
                self.direction = "circular"
        elif self.direction == "circular":
            self.x = WIDTH // 2 + int(math.cos(math.radians(angle)) * (WIDTH // 4))
            self.y = HEIGHT // 2 + int(math.sin(math.radians(angle)) * (HEIGHT // 4))
            angle += ship_speed
            if angle >= 360:
                angle = 0

# Create ships
ships = [Ship(0, "right"), Ship(WIDTH, "left")]

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLACK)

    # Draw the ships
    for ship in ships:
        pygame.draw.circle(screen, WHITE, (ship.x, ship.y), ship_radius)
        ship.update()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
