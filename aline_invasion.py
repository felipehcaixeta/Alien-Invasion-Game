import sys, pygame

class AlienInvasion:
    '''Overall class to manage game assets and behavior.'''

    def __init__(self):
        '''Initialize the game, and create game resources.'''
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Alien Invasion')

        # Set the background image.
        original_bg_img = pygame.image.load("images/background_img_alien_inv.png")
        self.bg_img = pygame.transform.smoothscale(
            original_bg_img, (self.screen_width, self.screen_height)
        )

    
    def run_game(self):
        '''Start the main loop for the game.'''
        while True:
            # Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            # Redraw the screen during each pass through the loop.
            # self.screen.fill([230, 230, 230])
            self.screen.blit(self.bg_img, (0, 0))

            # Make the most recently drawn screen visible.
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
