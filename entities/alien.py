import pygame
from pygame.sprite import Sprite
from entities.particle import Particle
from settings.settings import Settings
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
    
    def update(self, *args, **kwargs):
        '''Move the alien to the right or left'''
        print("Current Position:", (self.rect.x, self.rect.y))
        AlienMovement().first_level(self)
        print("Current Position:", (self.rect.x, self.rect.y))
        # print("Current position:", (self.rect.x, self.rect.y))
        # AlienMovement().second_level(self)
        # print("New position:", (self.rect.x, self.rect.y))
        # (x,y) (590, 150)
        

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

        # Check edges and reverse direction if alien reaches the edge
        if alien.rect.right >= alien.screen.get_width() or alien.rect.left <= 0:
            alien.settings.fleet_direction *= -1

    @staticmethod
    def second_level(alien):
        start_x = alien.rect.x
        start_y = alien.rect.y
        print("(x,y)", (start_x, start_y))
        current_waypoint = 0  # Initialize with the index of the first waypoint
        waypoints = [(start_x, start_y), (400, start_y), (400, 400), (start_x, 400), (start_x, start_y)]

        # Get the current waypoint
        target_x, target_y = waypoints[current_waypoint]

        # Move towards the current waypoint
        if alien.rect.x < target_x:
            alien.rect.x += alien.settings.alien_speed
        elif alien.rect.x > target_x:
            alien.rect.x -= alien.settings.alien_speed

        if alien.rect.y < target_y:
            alien.rect.y += alien.settings.alien_speed
        elif alien.rect.y > target_y:
            alien.rect.y -= alien.settings.alien_speed

        # Check if the alien has reached the current waypoint
        if alien.rect.x == target_x and alien.rect.y == target_y:
            # Move to the next waypoint
            current_waypoint = (current_waypoint + 1) % len(waypoints)


class AlienLevel:
    def first_level(self, ai_game, alien_group, number_aliens_x, alien_width, stats):
        # Create the first row of aliens
        print("Before alien creation loop. Level:", stats.level)
        for alien_number in range(number_aliens_x):
            if alien_number < stats.level:
                # Create an alien and place it in the row
                alien = Alien(ai_game)
                alien.x = alien_width + 2 * alien_width * alien_number
                alien.rect.x = alien.x
                alien_group.add(alien)           
        print("After alien creation loop. Number of aliens created:", len(alien_group))

    def second_level(self, ai_game, alien_group):
        alien = Alien(ai_game)
        alien_group.add(alien)



        





