import pygame
from pygame.sprite import Sprite
from entities.particle import Particle
from settings.settings import Settings
import random, math

class Alien(Sprite):
    '''A class to represent a single alien in the fleet'''
    def __init__(self, ai_game, spawn_random=False):
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

        # Alien Coordination
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
        
        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

        self.current_waypoints = 0
    
    def update(self, *args, **kwargs):
        '''Move the alien to the right or left'''
        # print("Current Position:", (self.rect.x, self.rect.y))
        # AlienMovement().first_level(self)
        # print("Current Position:", (self.rect.x, self.rect.y))
        AlienMovement(self.screen.get_width(), self.screen.get_height()).second_level(self)
        # (x,y) (590, 150)
        

    def explode_particles(self, all_particles):
        '''Create particles for explosion effect'''
        for _ in range(10):  # Adjust the number of particles as needed
            particle = Particle(self.rect.centerx, self.rect.centery)
            all_particles.add(particle) 

class AlienMovement:
    '''Handles alien movement logic'''
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def first_level(alien):
        '''Move the alien to the right or left'''
        alien.x += (alien.settings.alien_speed * alien.settings.fleet_direction)
        alien.rect.x = alien.x

        # Check edges and reverse direction if alien reaches the edge
        if alien.rect.right >= alien.screen.get_width() or alien.rect.left <= 0:
            alien.settings.fleet_direction *= -1

    def second_level(self, alien):
        # Get the target position from the alien's current waypoints
        #if alien.rect.x == alien.screen.get_width() - alien.rect.width:
        if alien.direction == "right":
            waypoints = [(0.7, 0.15), (0.3, 0.15), (0.3, 0.5), (0.7, 0.5)]
        else:
            waypoints = [(0.3, 0.15), (0.7, 0.15), (0.7, 0.5), (0.3, 0.5)]
        

        # Get the target position from the alien's current waypoints
        target_x = waypoints[alien.current_waypoints][0] * self.screen_width
        target_y = waypoints[alien.current_waypoints][1] * self.screen_height

        # Calculate the difference between the current position and the target position
        dx = target_x - alien.rect.x
        dy = target_y - alien.rect.y

        # Calculate the distance between the current position and the target position
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Define the speed of movement
        speed = 5

        # Move towards the current waypoint using linear interpolation
        if distance > speed:
            # Calculate the ratio of movement based on the speed and distance
            ratio = speed / distance
            alien.rect.x += dx * ratio
            alien.rect.y += dy * ratio
        else:
            # If the distance is less than the speed, set the alien's position to the target position
            alien.rect.x = target_x
            alien.rect.y = target_y

            # Move to the next waypoint
            alien.current_waypoints = (alien.current_waypoints + 1) % len(waypoints)

class AlienLevel:
    def first_level(self, ai_game, alien_group, number_aliens_x, alien_width, stats):
        # Create the first row of aliens
        for alien_number in range(number_aliens_x):
            if alien_number < stats.level:
                # Create an alien and place it in the row
                alien = Alien(ai_game)
                alien.x = alien_width + 2 * alien_width * alien_number
                alien.rect.x = alien.x
                alien_group.add(alien)           

    def second_level(self, ai_game, alien_group, alien_width, max_aliens_second_level, spawn_interval):
        for i in range(max_aliens_second_level):
            if i % 2 == 0:  # Alternate between left and right spawns
                alien = Alien(ai_game, spawn_random=True)
            else:
                alien = Alien(ai_game, spawn_random=True)  # Pass False to spawn at the other side
            alien.rect.x = (i + 1) * (alien_width + spawn_interval) + i * alien_width
            alien_group.add(alien)









        





