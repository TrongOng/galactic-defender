import pygame
from pygame.sprite import Sprite
from entities.particle import Particle

class Ship(Sprite):
    '''Class to manage the ship'''

    def __init__(self, ai_game):
        '''initialize the ship and set its starting position'''
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/gd_ship.bmp')
        self.original_image = self.image  # Store the original image for resizing

        # Resize the ship initially
        initial_size = (self.image.get_width() // 8, self.image.get_height() // 8)
        self.image = pygame.transform.scale(self.original_image, initial_size)
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= 20  # Move the ship 20 pixels up

        # Store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Move flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # Ensure the ship remains centered at the bottom after resizing
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def update(self):
        '''Update the ship's position based on the movement flag'''
        # Update the ship's x value, not the rect
        # if ship rect value is less than the screen rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        # if ship rect is greater than screen location on left
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # if ship rect is greater than 0
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        # if ship rect is less than screen rect
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        
        #Update rect object from self.x
        self.rect.x = self.x
        self.rect.y = self.y

    def resize(self, new_size):
        '''Resize the ship image and update its rect'''
        self.image = pygame.transform.scale(self.original_image, new_size)
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def blitme(self):
        '''Draw the ship at its current location'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        '''Center the ship on the screen'''
        # self.rect.midbottom = self.screen_rect.midbottom
        # self.rect.y -= 20  # Move the ship 10 pixels up
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= 20  # Move the ship 20 pixels up
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def explode_particles(self, all_particles):
        '''Create particles for explosion effect'''
        for _ in range(10):  # Adjust the number of particles as needed
            particle = Particle(self.rect.centerx, self.rect.centery)
            all_particles.add(particle) 


