import pygame.font

class Button:
    '''A class to build buttons for the game'''

    def __init__(self, ai_game, msg):
        '''Initialize button attributes'''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.original_width, self.original_height = 210, 75
        self.hover_width, self.hover_height = 220, 85
        self.width, self.height = self.original_width, self.original_height
        self.button_color = (55, 20, 70)  # Dark Purple
        self.text_color = (255, 115, 0)  # Orange
        self.font = pygame.font.SysFont('comicsansms', 42)  # Font style and size
        self.radius = 10

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once
        self._prep_msg(msg)

    def update(self, mouse_pos):
        '''Update button color when hover'''

        if self.rect.collidepoint(mouse_pos):
            self.width, self.height = self.hover_width, self.hover_height
        else:
            self.width, self.height = self.original_width, self.original_height

        old_center = self.rect.center
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = old_center
        self.msg_img_rect = self.rect.center

    def _prep_msg(self, msg):
        '''Turn msg into a rendered image and center text on the button'''
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        '''Draw button with rounded edges'''
        pygame.draw.rect(
            self.screen,
            self.button_color,
            self.rect,
            border_radius = self.radius
        )
        # self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
