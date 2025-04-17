import pygame

class Settings:
    '''A class to store all settings for Alien Invasion.'''

    def __init__(self):
        '''Initialize the game settings.'''
        # Set screen size
        self.default_screen_width = 1200
        self.default_screen_height = 800
        self.screen_width = self.default_screen_width
        self.screen_height = self.default_screen_height
        self.fullscreen = False  # Keep track of fullscreen mode

        # Set the background image.
        self.original_bg_img = pygame.image.load("images/background_img_alien_inv.png")
        self.bg_img = pygame.transform.smoothscale(
            self.original_bg_img, (self.screen_width, self.screen_height)
        )

        # Ship settings
        self.ship_speed = 2

    def _toggle_fullscreen(self):
        '''Toggle between fullscreen and windowed mode'''
        if self.fullscreen:
            self.screen = pygame.display.set_mode(
            (self.default_screen_width, self.default_screen_height)
        )
            self.screen_width = self.default_screen_width
            self.screen_height = self.default_screen_height
            self.fullscreen = False
        else:
            # Set fullscreen
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.screen_width = self.screen.get_rect().width
            self.screen_height = self.screen.get_rect().height
            self.fullscreen = True

        self.bg_img = pygame.transform.smoothscale(
            self.original_bg_img, (self.screen_width, self.screen_height)
        )
        
        