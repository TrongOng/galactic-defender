class Settings:
    '''Class to store all settings for Galactic Defender'''
    def __init__(self):
        '''Init the game's settings'''
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.FPS = 60 

        # Ship settings
        self.ship_limit = 3 # User Health

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 60, 60)
        self.bullets_allowed = 1.0

        # Alien shooting frequency (lower the faster)
        self.alien_shooting_frequency = 50
        self.alien_bullet_color = (255, 60, 60)

        # How quickly the game speed ups
        self.speedup_scale = 1.1

        # Game Speed Settings
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Initialize settings that change throughout the game'''
        self.ship_speed = 13.0
        self.bullet_speed = 15.0
        self.alien_bullet_speed = 7.0
        #self.alien_speed = 5

        # Scoring
        self.alien_points = 50




