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
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 3.0
        self.bullet_width = 4
        self.bullet_height = 15
        self.bullet_color = (30, 30, 170)
        self.bullets_allowed = 15

        # Alien settings
        self.alien_speed = 1.5
        self.fleet_drop_speed = 20
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

    def _toggle_fullscreen(self):
        '''Toggle between fullscreen and windowed mode'''
        # TODO: This is still buggy. Need to fix the ships' position while in fullscreen.
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
        
        