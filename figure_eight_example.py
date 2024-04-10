import pygame
import sys, math, random

class Sprite(pygame.sprite.Sprite):
    def __init__(self, screen, spawn_random=False):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))  # Green color for the sprite
        self.rect = self.image.get_rect()
        self.screen = screen
        if spawn_random:
            self.rect.x = random.choice([self.rect.width, self.screen.get_width() - self.rect.width])
            if self.rect.x == self.rect.width:
                self.rect.y = self.rect.height + 100
                self.direction = "left"
            else:
                self.rect.y = self.rect.height + 100
                self.direction = "right"

        else:
            self.rect.x = self.rect.width
            self.rect.y = self.rect.height + 100
            self.direction = "left"

        self.current_waypoint = 0  # Index of the current waypoint

    def update(self, movement):
        movement.second_level(self)

class Movement:
    def second_level(self, sprite):
        #if sprite.rect.x == sprite.screen.get_width() - sprite.rect.width:
        if sprite.direction == "right":
            waypoints = [(1400, 200), (500, 200), (500, 600), (1400, 600)]
        else:
            waypoints = [(500, 200), (1400, 200), (1400, 600), (500, 600)]

        target_x, target_y = waypoints[sprite.current_waypoint]

        dx = target_x - sprite.rect.x
        dy = target_y - sprite.rect.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        speed = 5

        if distance > speed:
            ratio = speed / distance
            sprite.rect.x += dx * ratio
            sprite.rect.y += dy * ratio
        else:
            sprite.rect.x = target_x
            sprite.rect.y = target_y
            sprite.current_waypoint = (sprite.current_waypoint + 1) % len(waypoints)

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    sprite = Sprite(screen, spawn_random=True)
    all_sprites = pygame.sprite.Group(sprite)
    movement = Movement()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        all_sprites.update(movement)

        screen.fill((0, 0, 0))  # Fill the screen with black color
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)  # Cap the frame rate at 60 FPS

if __name__ == "__main__":
    main()



