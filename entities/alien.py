import pygame
from pygame.sprite import Sprite
from entities.particle import Particle
from settings.settings import Settings
import random, math

class Alien(Sprite):
    '''A class to represent a single alien in the fleet'''
    def __init__(self, ai_game):
        '''Initialize the alien and sets it starting position'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.alien_speed = 5
        self.fleet_direction = 1
        self.current_waypoints = 0
        self.direction = ""

        # Load the alien image and get its rect
        self.image = pygame.image.load('images/alien.bmp')
        self.original_image = self.image  # Store the original image for resizing

        # Resize the alien initially
        initial_size = (self.image.get_width() // 16, self.image.get_height() // 16)
        self.image = pygame.transform.scale(self.original_image, initial_size)
        self.rect = self.image.get_rect()

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self, *args, **kwargs):
        '''Move the alien to the right or left'''
        AlienMovement(self.screen.get_width(), self.screen.get_height()).sqaure_pattern(self)
        #AlienMovement(self.screen.get_width(), self.screen.get_height()).linear_pattern(self)

        # Update the rect based on the new positions
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        

    def explode_particles(self, all_particles):
        '''Create particles for explosion effect'''
        for i in range(10):  # Adjust the number of particles as needed
            particle = Particle(self.rect.centerx, self.rect.centery)
            all_particles.add(particle) 

class AlienMovement:
    '''Handles alien movement logic'''
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def linear_pattern(self, alien):
        alien.x += (alien.alien_speed * alien.fleet_direction)
        alien.rect.x = alien.x

        # Check edges and reverse direction if alien reaches the edge
        if alien.rect.right >= alien.screen.get_width() or alien.rect.left <= 0:
            alien.fleet_direction *= -1

    def sqaure_pattern(self, alien):
        def lerp(start, end, t):
            return start + (end - start) * t
        
        if alien.direction == "right":
            waypoints = [(0.7, 0.15), (0.3, 0.15), (0.3, 0.5), (0.7, 0.5)]
        else:
            waypoints = [(0.3, 0.15), (0.7, 0.15), (0.7, 0.5), (0.3, 0.5)]

        target_x = waypoints[alien.current_waypoints][0] * self.screen_width
        target_y = waypoints[alien.current_waypoints][1] * self.screen_height

        dx = target_x - alien.x
        dy = target_y - alien.y

        distance = math.sqrt(dx ** 2 + dy ** 2)
        speed = 5

        if distance > 0:
            # Calculate a consistent interpolation factor for both dx and dy
            t = min(speed / distance, 1)  # Ensure t doesn't exceed 1
            alien.x = lerp(alien.x, target_x, t)
            alien.y = lerp(alien.y, target_y, t)

        if distance < 1:  # If close to target, move to the next waypoint
            alien.current_waypoints = (alien.current_waypoints + 1) % len(waypoints)

class AlienLevel:
    def __init__(self) -> None:
        pass
    
    def spawn_alien(self, ai_game, spawn_random=False):
        '''Spawn a new alien'''
        alien = Alien(ai_game)
        if spawn_random:
            '''Spawn the alien randomly on the screen'''
            alien.rect.x = random.choice([alien.rect.width, ai_game.settings.screen_width - alien.rect.width])
            print("Alien rect.x:", alien.rect.x)
            if alien.rect.x == alien.rect.width:
                alien.rect.y = alien.rect.height + 100
                alien.direction = "left"
            else:
                alien.rect.y = alien.rect.height + 100
                alien.direction = "right"   
        else:
            alien.rect.x = alien.rect.width
            alien.rect.y = alien.rect.height + 100
            alien.direction = "left"

        alien.x = float(alien.rect.x)
        alien.y = float(alien.rect.y)

        return alien

    def first_level(self, ai_game, alien_group):
        # Create a single alien object to get its dimensions
        alien = self.spawn_alien(ai_game)
        alien_width, alien_height = alien.rect.size

        # Calculate max aliens horizontal for the first level
        available_space_x_first_level = ai_game.settings.screen_width - (2 * alien_width)
        number_aliens_x_first_level = available_space_x_first_level // (2 * alien_width)

        for alien_number in range(number_aliens_x_first_level):
            # Create a new alien object in each iteration
            alien = self.spawn_alien(ai_game)
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.y = alien.rect.height + 100
            alien_group.add(alien)

    def second_level(self, ai_game, alien_group, ship_height):
        # Create a single alien object to get its dimensions
        alien = self.spawn_alien(ai_game)
        alien_width, alien_height = alien.rect.size

        # Calculate max aliens horizontal for the first level
        available_space_x_first_level = ai_game.settings.screen_width - (2 * alien_width)
        number_aliens_x_first_level = available_space_x_first_level // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen
        available_space_y_first_level = ai_game.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = min(2, available_space_y_first_level // (2 * alien_height))

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x_first_level):
                # Create a new alien object in each iteration
                alien = self.spawn_alien(ai_game)
                alien.x = alien_width + 2 * alien_width * alien_number
                alien.y = (alien.rect.height + 2 * alien.rect.height * row_number) + 100
                alien_group.add(alien)

    def third_level(self, ai_game, alien_group):
        # Create a single instance of Alien to determine the side of spawning
        first_alien = self.spawn_alien(ai_game, spawn_random=True)
        first_alien_direction = first_alien.direction # Store the direction of the first alien

        # Initiate Variables
        spawn_interval = 100
        alien_width, alien_height = first_alien.rect.size

        # Calculate the available space for aliens
        available_space_x = ai_game.settings.screen_width - 2 * alien_width

        # Calculate max aliens horizontal for the second level
        available_space_x_second_level = ai_game.settings.screen_width - spawn_interval
        max_aliens_second_level = available_space_x_second_level // (alien_width + spawn_interval)

        # Calculate the gap between each alien's spawn position
        gap = available_space_x / (max_aliens_second_level + 1)

        # Calculate the starting x position based on the chosen side and gap
        if first_alien_direction == "left":
            start_x = gap
        else:
            start_x = ai_game.settings.screen_width - gap - alien_width

        for i in range(max_aliens_second_level):
            # Create a new instance of Alien for each alien in the loop
            alien = self.spawn_alien(ai_game, spawn_random=False)  # Ensure spawn is not random
            alien.direction = first_alien_direction # Set the direction of the current alien to that of the first alien

            # Calculate the position of the current alien
            alien.x = start_x + (i * gap) if first_alien.direction == "right" else start_x - (i * gap)
            alien.y = alien.rect.height + 100
            alien_group.add(alien)










        





