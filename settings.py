import pygame

class Settings:
    '''A class to store all settings for Alien Invasion.'''

    def __init__(self):
        '''Initialize the game settings.'''
        # Set screen size
        self.screen_width = 1200
        self.screen_height = 800

        # Set the background image.
        original_bg_img = pygame.image.load("images/background_img_alien_inv.png")
        self.bg_img = pygame.transform.smoothscale(
            original_bg_img, (self.screen_width, self.screen_height)
        )