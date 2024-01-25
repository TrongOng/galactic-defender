import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    '''A class to manage bullets fired by aliens'''

    def __init__(self, ai_game, alien):
        '''Create a bullet object at the alien's position'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.alien_bullet_color

        # Create a bullet rect at the alien's position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midbottom = alien.rect.midbottom  # Ensure it starts from the center bottom of the alien

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        '''Move the bullet down the screen (from alien to player)'''
        # Update the decimal position of the bullet
        self.y += self.settings.alien_bullet_speed
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        '''Draw the bullet at the screen'''
        pygame.draw.rect(self.screen, self.color, self.rect)

