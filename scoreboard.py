import pygame.font

class Scoreboard:
    '''A class to report score information'''

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for score information
        self.text_color = (255, 165, 0)
        self.font = pygame.font.SysFont(None, 40)

        # Prepare the initial score image
        self.prep_score()

    def prep_score(self):
        '''Turn the score into a rendered image'''
        rounded_score = round(self.stats.score, -1)
        score_str = f'{rounded_score:,}'
        self.score_image = self.font.render(
            score_str,
            True,
            self.text_color,
            # self.settings.bg_img
        )

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        '''Draw score to the screen'''
        self.screen.blit(self.score_image, self.score_rect)


        
    