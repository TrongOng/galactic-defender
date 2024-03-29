import pygame
from pygame.sprite import Sprite
from particle import Particle
import random

class Alien(Sprite):
    '''A class to represent a single alien in the fleet'''
    def __init__(self, ai_game):
        '''Initialize the alien and sets it starting position'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and get its rect
        self.image = pygame.image.load('images/alien.bmp')
        self.original_image = self.image  # Store the original image for resizing

        # Resize the alien initially
        initial_size = (self.image.get_width() // 16, self.image.get_height() // 16)
        self.image = pygame.transform.scale(self.original_image, initial_size)
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = random.randint(0, self.screen.get_width() - self.rect.width)
        self.rect.y =  150 #self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)
    
    def check_edges(self):
        '''Return True if alien is at edge of screen'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    
    def update(self):
        '''Move the alien to the right or left'''
        # self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        # self.rect.x = self.x
        AlienMovement().first_level(self)

    def explode_particles(self, all_particles):
        '''Create particles for explosion effect'''
        for _ in range(10):  # Adjust the number of particles as needed
            particle = Particle(self.rect.centerx, self.rect.centery)
            all_particles.add(particle) 

class AlienMovement:
    '''Handles alien movement logic'''
    @staticmethod
    def first_level(alien):
        '''Move the alien to the right or left'''
        alien.x += (alien.settings.alien_speed * alien.settings.fleet_direction)
        alien.rect.x = alien.x




