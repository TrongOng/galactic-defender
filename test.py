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
        self.alien_speed = 5
        self.fleet_direction = 1
        self.current_waypoints = 0

        # Load the alien image and get its rect
        self.image = pygame.image.load('images/alien.bmp')
        self.original_image = self.image  # Store the original image for resizing

        # Resize the alien initially
        initial_size = (self.image.get_width() // 16, self.image.get_height() // 16)
        self.image = pygame.transform.scale(self.original_image, initial_size)
        self.rect = self.image.get_rect()

        # # Alien Coordination
        if spawn_random:
            '''Spawn the alien randomly on the screen'''
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
        self.y = float(self.rect.y)

    def update(self, *args, **kwargs):
        '''Move the alien to the right or left'''
        AlienMovement(self.screen.get_width(), self.screen.get_height()).second_level(self)
        #AlienMovement(self.screen.get_width(), self.screen.get_height()).first_level(self)

        # Update the rect based on the new positions
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        

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

    def first_level(self, alien):
        alien.x += (alien.alien_speed * alien.fleet_direction)
        alien.rect.x = alien.x

        # Check edges and reverse direction if alien reaches the edge
        if alien.rect.right >= alien.screen.get_width() or alien.rect.left <= 0:
            alien.fleet_direction *= -1


    def second_level(self, alien):
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
    def first_level(self, ai_game, alien_group, ship_height, stats):
        # Create a single alien object to get its dimensions
        alien = Alien(ai_game)
        alien_width, alien_height = alien.rect.size

        # Calculate max aliens horizontal for the first level
        available_space_x_first_level = ai_game.settings.screen_width - (2 * alien_width)
        number_aliens_x_first_level = available_space_x_first_level // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen
        available_space_y_first_level = ai_game.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = min(2, available_space_y_first_level // (2 * alien_height))

        if stats.level == 1:
            for alien_number in range(number_aliens_x_first_level):
                # Create a new alien object in each iteration
                alien = Alien(ai_game)
                alien.x = alien_width + 2 * alien_width * alien_number
                alien.y = alien.rect.height + 100
                alien_group.add(alien)
        elif stats.level == 2:
            for row_number in range(number_rows):
                for alien_number in range(number_aliens_x_first_level):
                    # Create a new alien object in each iteration
                    alien = Alien(ai_game)
                    alien.x = alien_width + 2 * alien_width * alien_number
                    alien.y = (alien.rect.height + 2 * alien.rect.height * row_number) + 100
                    alien_group.add(alien)

    def second_level(self, ai_game, alien_group, alien_width, max_aliens_second_level):
        # Create a single instance of Alien to determine the side of spawning
        alien = Alien(ai_game, spawn_random=True)

        # Determine the side of spawning
        side = alien.direction
        print("Spawn side in second level:", side)

        # Calculate the gap between aliens
        available_space_x = ai_game.settings.screen_width - 2 * alien_width
        gap = available_space_x / (max_aliens_second_level + 1)

        # Calculate the starting x position based on the chosen side and gap
        if side == "left":
            start_x = gap
        else:
            start_x = ai_game.settings.screen_width - gap - alien_width

        # Spawn all aliens on the chosen side
        for i in range(max_aliens_second_level):
            # Create a new instance of Alien for each alien
            new_alien = Alien(ai_game)

            # Set the position of the new alien based on the calculated start_x and gap
            new_alien.x = start_x + (i + 1) * gap
            new_alien.y = new_alien.rect.height + 100
            
            alien_group.add(new_alien)


    # def second_level(self, ai_game, alien_group, alien_width, max_aliens_second_level):
    #     # Calculate the available space for aliens
    #     available_space_x = ai_game.settings.screen_width - 2 * alien_width

    #     # Calculate the gap between each alien's spawn position
    #     gap = available_space_x / (max_aliens_second_level + 1)

    #     # Calculate the starting x position based on the chosen side and gap
    #     start_x = ai_game.settings.screen_width - gap - alien_width

    #     # Spawn all aliens on the chosen side
    #     for i in range(max_aliens_second_level):
    #         alien = Alien(ai_game, spawn_random=True)
    #         alien.x = start_x + (i + 1) * gap  # Adding 1 to i to start from the first gap
    #         alien.y = alien.rect.height + 100
    #         alien_group.add(alien)