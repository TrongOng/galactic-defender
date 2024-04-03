import pygame
import sys

class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))  # Green color for the sprite
        self.rect = self.image.get_rect()
        self.rect.center = (300, 300)  # Starting position of the sprite
        self.speed = 2
        self.direction = 'right'

    def update(self):
        # Move the sprite in the specified direction
        if self.direction == 'right':
            self.rect.x += self.speed
            if self.rect.right >= 400:  # If the sprite reaches half of the screen width
                self.rect.right = 400
                self.direction = 'down'
        elif self.direction == 'down':
            self.rect.y += self.speed
            if self.rect.bottom >= 400:  # If the sprite reaches half of the screen height
                self.rect.bottom = 400
                self.direction = 'left'
        elif self.direction == 'left':
            self.rect.x -= self.speed
            if self.rect.left <= 150:  # If the sprite reaches half of the screen width
                self.rect.left = 150
                self.direction = 'up'
        elif self.direction == 'up':
            self.rect.y -= self.speed
            if self.rect.top <= 150:  # If the sprite reaches half of the screen height
                self.rect.top = 150
                self.direction = 'right'

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
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

