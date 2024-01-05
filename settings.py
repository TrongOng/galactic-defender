class Settings:
    '''Class to store all settings for Alien Invasion'''

    def __init__(self):
        '''Init the game's settings'''
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed = 0.7