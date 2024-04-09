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

        # Start each new alien near the top left of the screen
        #self.rect.x = random.randint(0, self.screen.get_width() - self.rect.width)\
        #self.rect.y = 150
        # self.rect.x = self.rect.width
        # self.rect.y = self.rect.height + 100 #y = 161
        # Start each new alien near the top left of the screen
        if spawn_random:
            self.rect.x = random.choice([self.rect.width, self.screen.get_width() - self.rect.width])
            self.rect.y = self.rect.height + 100
        else:
            self.rect.x = self.rect.width
            self.rect.y = self.rect.height + 100
        
        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

        self.current_waypoints = 0
        print("Screen size:", (self.screen.get_width(), self.screen.get_height()))

    
    def update(self, *args, **kwargs):
        '''Move the alien to the right or left'''
        # print("Current Position:", (self.rect.x, self.rect.y))
        # AlienMovement().first_level(self)
        # print("Current Position:", (self.rect.x, self.rect.y))
        AlienMovement().second_level(self)
        # (x,y) (590, 150)
        

    def explode_particles(self, all_particles):
        '''Create particles for explosion effect'''
        for _ in range(10):  # Adjust the number of particles as needed
            particle = Particle(self.rect.centerx, self.rect.centery)
            all_particles.add(particle) 

class AlienMovement:
    '''Handles alien movement logic'''
    square_waypoints_left = [(500, 200), (1400, 200), (1400, 600), (500, 600)]
    square_waypoints_right = [(1400, 200), (500, 200), (500, 600), (1400, 600)]

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
        # Get the target position from the alien's current waypoints
        if alien.rect.x == alien.screen.get_width() - alien.rect.width:
            waypoints = AlienMovement.square_waypoints_right
        else:
            waypoints = AlienMovement.square_waypoints_left
        

        # Get the target position from the alien's current waypoints
        target_x, target_y = waypoints[alien.current_waypoints]

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

        # Debugging output
        print("Alien Position:", (alien.rect.x, alien.rect.y))
        print("Target Position:", (target_x, target_y))
        


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
        print("After alien creation loop. Number of aliens created:", len(alien_group))

    def second_level(self, ai_game, alien_group, spawn_random=True):
        alien = Alien(ai_game, spawn_random=True)
        alien_group.add(alien)



        





