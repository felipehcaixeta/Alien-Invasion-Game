import pygame, os
from pygame.sprite import Sprite

class Alien(Sprite):
    '''A class to represent a single alien in the fleet'''

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Ensure files are found regardless of machine or file location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(script_dir, "images", "aliennn.bmp")

        # Load the alien image and set its rect attribute
        self.alien_width = 60
        self.alien_height = 70
        self.image = pygame.image.load(img_path)
        self.alien = pygame.transform.smoothscale(
            self.image, (self.alien_width, self.alien_height)
        )
        self.image = self.alien
        self.rect = self.image.get_rect()
        # print(f'Alien rect dimensions: {self.rect.width} x {self.rect.height}')
        
        # Store the alien's exact vertical position
        self.y = float(self.rect.y)

    def check_edges(self):
        '''Return True if alien is at edge of screen'''
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    #region AlienMovement
    def update(self):
        '''Move the alien straight down the screen'''
        self.y += self.settings.alien_speed
        self.rect.y = self.y
    #endregion
   

        