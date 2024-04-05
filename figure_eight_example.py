import pygame
import sys

class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))  # Green color for the sprite
        self.rect = self.image.get_rect()
        self.rect.center = (150, 150)  # Starting position of the sprite
        self.speed = 2
        self.waypoints = [(400, 400), (400, 200), (200, 200), (200, 400)]  # Waypoints for square movement
        self.current_waypoint = 0  # Index of the current waypoint

    def update(self):
        # Get the current waypoint
        target_x, target_y = self.waypoints[self.current_waypoint]

        # Move towards the current waypoint
        if self.rect.x < target_x:
            self.rect.x += self.speed
        elif self.rect.x > target_x:
            self.rect.x -= self.speed

        if self.rect.y < target_y:
            self.rect.y += self.speed
        elif self.rect.y > target_y:
            self.rect.y -= self.speed

        # Check if the sprite has reached the current waypoint
        if self.rect.x == target_x and self.rect.y == target_y:
            # Move to the next waypoint
            self.current_waypoint = (self.current_waypoint + 1) % len(self.waypoints)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()

    sprite = Sprite()
    all_sprites = pygame.sprite.Group(sprite)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        all_sprites.update()

        screen.fill((0, 0, 0))  # Fill the screen with black color
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)  # Cap the frame rate at 60 FPS

if __name__ == "__main__":
    main()

