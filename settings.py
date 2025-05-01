import pygame, os

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

        # Ensure files are found regardless of machine or file location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(script_dir, "images", "bg_image.jpg")

        # Set the background image.
        self.original_bg_img = pygame.image.load(img_path)
        self.bg_img = pygame.transform.smoothscale(
            self.original_bg_img, (self.screen_width, self.screen_height)
        )

        # Ship settings
        self.ship_speed = 6  # Obsolete because initialize_dynamic_settings overrides
        self.ship_limit = 2
        # TODO: Add a turbo speed when hold down CTRL + Direction

        # Bullet settings
        self.bullet_speed = 3.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (30, 30, 230)
        self.bullets_allowed = 15

        # Alien settings
        self.alien_speed = 1.5
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left
        # self.fleet_direction = 1

        # How quickly the game speeds up
        # TODO: Change the level system. Level should increase after
        #   a certain number of enemies are killed or a certain score is achieved.
        self.speedup_scale = 1.0

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Initialize settings that change throughout the game'''
        self.ship_speed = 5
        self.bullet_speed = 3
        self.alien_speed = 1.5

        # Score settings
        self.alien_points = 50

    def increase_speed(self):
        '''Increase speed settings'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

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
        
        