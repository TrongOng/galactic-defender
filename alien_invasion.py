import sys, pygame, math, random
from time import sleep
from enum import Enum

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien_bullet import AlienBullet
from alien import Alien
from stars import Star, create_star_field
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from particle import Particle

class Keys(Enum):
    RIGHT = pygame.K_RIGHT
    LEFT = pygame.K_LEFT
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    QUIT = pygame.K_q
    SPACE = pygame.K_SPACE

class AlienInvasion:
    '''Overall class to manage game assets and behavior'''
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        # Display Window
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.clock = pygame.time.Clock()

        # Create an instance to store game statitics
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Create a group for stars using the create_star_field function
        self.stars = create_star_field(self, 800)  # Adjust the number of stars as needed

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        # Create a group for alien bullets
        self.alien_bullets = pygame.sprite.Group()
        self.spacebar_pressed = False  # Flag to check if the spacebar is pressed
        self.aliens = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()


        self._create_fleet()

        # Play button
        self.play_button = Button(self, "Play")

    '''Start the main loop for the game'''
    def run_game(self):
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self.particles.update()
                self._update_bullets()
                self._update_aliens()
                self._update_alien_bullets()

            self._update_screen()
            self.clock.tick(60) 

    '''Respond to keypresses and mouse events'''
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    '''Start a new game when the player clicks play'''
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            print("prep_level called. Current level:", self.stats.level)
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

    '''Respond to keypresses'''
    def _check_keydown_events(self, event):
        if event.key == Keys.RIGHT.value:
            self.ship.moving_right = True
        elif event.key == Keys.LEFT.value:
            self.ship.moving_left = True
        elif event.key == Keys.UP.value:
            self.ship.moving_up = True
        elif event.key == Keys.DOWN.value:
            self.ship.moving_down = True
        elif event.key == Keys.QUIT.value:
            sys.exit()
        elif event.key == Keys.SPACE.value:
            self.spacebar_pressed = True  # Set the flag to true
    
    '''Respond to key releases'''
    def _check_keyup_events(self, event):
        if event.key == Keys.RIGHT.value:
            self.ship.moving_right = False
        elif event.key == Keys.LEFT.value:
            self.ship.moving_left = False
        elif event.key == Keys.UP.value:
            self.ship.moving_up = False
        elif event.key == Keys.DOWN.value:
            self.ship.moving_down = False
        elif event.key == Keys.SPACE.value:
            self.spacebar_pressed = False  # Set the flag to false when spacebar is released

    '''Create a new bullet and add it to the bullets group'''
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            new_bullet.rect.midtop = self.ship.rect.midtop  # Set bullet starting position
            self.bullets.add(new_bullet)

    '''Update position of bullets and get rid of old bullets'''
    def _update_bullets(self):
        if self.spacebar_pressed:
            self._fire_bullet()

        self.bullets.update()
        self.alien_bullets.update()

        # Get rid of bullets that have disappeared
        self._remove_offscreen_bullets(self.bullets)
        
        # Get rid of alien bullets that have disappeared
        self._remove_offscreen_bullets(self.alien_bullets)
        
        self._check_bullet_alien_collision()
        self._check_alien_bullet_collision()

    '''Remove bullets from the group that have disappeared off the screen'''
    def _remove_offscreen_bullets(self, bullets_group):
        screen_rect = self.screen.get_rect()
        
        for bullet in bullets_group.sprites():
            if bullet.rect.bottom <= 0 or bullet.rect.top >= screen_rect.height:
                bullets_group.remove(bullet)
    
    '''Respond to bullet-alien collisions'''
    def _check_bullet_alien_collision(self):
        # Remove any bullets and aliens that have collided
        collision = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # Add score points when hit only once
        if collision:
            for aliens in collision.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # Call explode_particles method for each hit alien
        for hit_aliens in collision.values():
            for alien in hit_aliens:
                alien.explode_particles(self.particles)

        # repopulating the fleet
        if not self.aliens:
            # Destroy existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            print("prep_level called. Current level:", self.stats.level)
            self.sb.prep_level()

    '''Respond to alien_bullet-ship collision'''
    def _check_alien_bullet_collision(self):
        # Using a sprite group for the player ship
        ship_collision = pygame.sprite.spritecollideany(self.ship, self.alien_bullets)

        if ship_collision:
            # Call explode_particles method for bullet hit ship
            self.ship.explode_particles(self.particles)
            self._ship_hit()
    
    '''Create the fleet of aliens'''
    def _create_fleet(self):
        # Make an alien
        alien = Alien(self)
        alien_width = alien.rect.width
        # Determine how many aliens fit in a row (x)
        available_space_x = self.settings.screen_width - (2 * alien_width)
        # Determine space bwtween aliens (one alien width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Create the first row of aliens
        print("Before alien creation loop. Level:", self.stats.level)
        for alien_number in range(number_aliens_x):
            if alien_number < self.stats.level:
                # Create an alien and place it in the row
                alien = Alien(self)
                alien.x = alien_width + 2 * alien_width * alien_number
                alien.rect.x = alien.x
                self.aliens.add(alien)           
        print("After alien creation loop. Number of aliens created:", len(self.aliens))

    '''Check if the fleet is at an edge, Update the positions of all aliens in the fleet'''
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        # Randomly make an alien shoot a bullet
        if random.randint(1, self.settings.alien_shooting_frequency) == 1:
            self._alien_shoot_bullet()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()
    
    '''Make a random alien shoot a bullet'''
    def _alien_shoot_bullet(self):
        if self.aliens.sprites():
            random_alien = random.choice(self.aliens.sprites())
            new_bullet = AlienBullet(self, random_alien)
            self.alien_bullets.add(new_bullet)

    '''Update position of alien bullets and get rid of old bullets'''
    def _update_alien_bullets(self):
        self.alien_bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)

        # ... (any additional logic you need for alien bullets)
    
    '''Respond appropriately if any aliens have reached an edge'''
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    '''Drop the entire fleet and change the fleet's direction'''
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    '''Respond to the ship being hit by an alien'''
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            # Decrement ships_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.2)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

            # Reset game statistics only if no ships are left
            self.stats.reset_stats()
            self.sb.prep_score()

    '''Check if any aliens have reached the bottom of the screen'''
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break

    '''Update images on the screen, and flip to the new screen'''
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw alien bullets
        for alien_bullet in self.alien_bullets.sprites():
            alien_bullet.draw_bullet()

        # Draw aliens
        self.aliens.draw(self.screen)

        # Draw stars on the screen
        self.stars.draw(self.screen)

        # Draw particle on hit 
        self.particles.draw(self.screen)

        # Draw the score information
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
