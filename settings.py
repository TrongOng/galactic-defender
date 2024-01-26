class Settings:
    '''Class to store all settings for Alien Invasion'''

    def __init__(self):
        '''Init the game's settings'''
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.FPS = 60 

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 60, 60)
        self.bullets_allowed = 1.0

        # Alien Settings
        self.alien_speed = 0.5
        self.fleet_drop_speed = 10
        self.fleet_direction = 1 # Fleet_direction of 1 represents right; -1 represents left

        # Alien shooting frequency
        self.alien_shooting_frequency = 100 
        self.alien_bullet_color = (255, 60, 60)

        # Game Speed Settings
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Initialize settings that change throughout the game'''
        self.ship_speed = 10.0
        self.bullet_speed = 3.0 * 5
        self.alien_bullet_speed = 7.0
        self.alien_speed = 1 * 5

        # Scoring
        self.alien_points = 50



