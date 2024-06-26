import pygame.font
from pygame.sprite import Group

from entities.ship import Ship

class Scoreboard:
    '''A class to report scoring information'''

    def __init__(self, ai_game):
        '''Initialize scorekeeping attributes'''
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font ssettings for scoring information
        self.text_color = (0, 255, 0, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

        self.update_level = True

    def prep_score(self):
        '''Turn the score into a rendered image'''
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)

        # Create a Surface with per-pixel alpha
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        self.score_image.set_colorkey(self.settings.bg_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 40
        self.score_rect.top = 40
    
    def prep_high_score(self):
        '''Turn the high score into a rendered image'''
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)

        # Create a Surface with per-pixel alpha
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        self.high_score_image.set_colorkey(self.settings.bg_color)

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        '''Check to see if there's a new high score'''
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
    
    def prep_level(self):
        '''Turn the level into a rendered image'''
        level_str = str(self.stats.level)

        # Create a Surface with per-pixel alpha
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
        self.level_image.set_colorkey(self.settings.bg_color)

        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        '''Show how many ships are left'''
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 40 + ship_number * ship.rect.width
            ship.rect.y = 40
            self.ships.add(ship)

    def show_score(self):
        '''Draw score to the screen'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        
        # Check if the level needs to be updated
        if self.update_level:
            self.prep_level()  # Call prep_level to update the level
            self.screen.blit(self.level_image, self.level_rect)
            self.update_level = False  # Set the flag to False after updating
        else:
            # If the level doesn't need to be updated, just blit the existing level image
            self.screen.blit(self.level_image, self.level_rect)

        # Health Bar Indicator
        self.ships.draw(self.screen) 
