import pygame

class Ship():
    '''Class to manage the ship'''

    def __init__(self, ai_game):
        '''Initialize the ship and set its starting position'''
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.ship_width = 60
        self.ship_height = 100
        space_ship = pygame.image.load("images/ship.png")
        self.ship = pygame.transform.smoothscale(
            space_ship, (self.ship_width, self.ship_height)
        )
        self.rect = self.ship.get_rect()

        # Start each new ship at the bottom center of screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the ship's exact horizontal position
        self.x = float(self.rect.x)

        # Movement flag; start with a ship that's not moving
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        '''Update the ship's position based on the movement flag'''
        if self.moving_right:
            self.x += self.settings.ship_speed
        if self.moving_left:
            self.x -= self.settings.ship_speed
        
        # Update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        '''Draw the ship at its current position'''
        self.screen.blit(self.ship, self.rect)