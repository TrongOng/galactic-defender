import pygame
import sys
import math
import random

class Settings:
    def __init__(self):
        '''Init the game's settings'''
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.FPS = 60 

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
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def second_level(self, sprite):
        if sprite.direction == "right":
            waypoints = [(0.7, 0.15), (0.3, 0.15), (0.3, 0.5), (0.7, 0.5)]
        else:
            waypoints = [(0.3, 0.15), (0.7, 0.15), (0.7, 0.5), (0.3, 0.5)]

        target_x = waypoints[sprite.current_waypoint][0] * self.screen_width
        target_y = waypoints[sprite.current_waypoint][1] * self.screen_height

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
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()  # Create a group to hold all sprites

    # Create multiple instances of Sprite and add them to the group
    spawn_interval = 50  # Adjust this value to set the distance between each spawned sprite
    sprite = Sprite(screen)
    sprite_width = sprite.rect.width
    max_sprites_horizontal = (settings.screen_width - spawn_interval) // (sprite_width + spawn_interval)
    for i in range(max_sprites_horizontal):
        sprite = Sprite(screen)
        sprite.rect.x = (i + 1) * (sprite_width + spawn_interval)
        all_sprites.add(sprite)


    movement = Movement(settings.screen_width, settings.screen_height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        all_sprites.update(movement)

        screen.fill((0, 0, 0))  # Fill the screen with black color
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(settings.FPS)  # Cap the frame rate at 60 FPS

if __name__ == "__main__":
    main()



