import sys, pygame, random, time, os
from settings import Settings
from ship import Ship
from  bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    '''Overall class to manage game assets and behavior.'''

    def __init__(self):
        '''Initialize the game, and create game resources.'''
        pygame.init()
        pygame.mixer.init()
        
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption('Alien Invasion')

        # Create an instance to store game statistics,
        #   and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Create an alien at a random location in the screen
        self._create_alien()

        # Start Alien Invasion in an active state
        self.game_active = True

        # Start the game in an inactive state
        self.game_active = False

        # Make Play button
        self.play_button = Button(self, "Play")

        # Timer for alien spawning
        self.last_alien_spawn_time = time.time()
        self.alien_spawn_delay = random.uniform(1, 6)

        # Tracks amount of aliens
        self.offscreen_aliens = []

        # Ensure files are found regardless of machine or file location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sound_bullet_path = os.path.join(script_dir, 'sounds', 'bullet.wav')
        sound_explosion_path = os.path.join(script_dir, 'sounds', 'explosion.wav')
        bgm_path = os.path.join(script_dir, 'sounds', 'bg_music.wav')

        # Sound effects & music
        self.bullet_sound = pygame.mixer.Sound(sound_bullet_path)
        self.explosion_sound = pygame.mixer.Sound(sound_explosion_path)
        pygame.mixer.music.load(bgm_path)
        pygame.mixer.music.play(-1)
    
    def run_game(self):
        '''Start the main loop for the game.'''
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._delayed_alien_spawn()

            self._update_screen()    
            self.clock.tick(60)  # Set target framerate
    
    def _check_events(self):
        '''Respond to keypresses and mouse events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        '''Respond to keypresses'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_f:
            self.settings._toggle_fullscreen()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self, event):
        '''Respond to key releases'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _play_button_hover(self, mouse_pos):
        '''Enlarge Play button when the mouse hovers over it'''
        mouse_pos = pygame.mouse.get_pos()
        self.play_button.update(mouse_pos)
        self.play_button.draw_button()

    def _check_play_button(self, mouse_pos):
        '''Start a new game when the player clicks Play'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset game settings
            self.settings.initialize_dynamic_settings()

            # Reset game statistics
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            # self.sb.prep_ships()
            self.game_active = True

            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Restart spawning aliens and center the ship
            self._create_alien()
            self.ship.center_ship()

            # Hide mouse cursor
            pygame.mouse.set_visible(False)
                
    def _fire_bullet(self):
        '''Create a new bullet and add it to the bullets group'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.bullet_sound.play()

    def _update_bullets(self):
        '''Update position of bullets and get rid of old bullets'''
        # Update bullet postions
        self.bullets.update()

        # Get rid of bullets that have dissapeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()             

    def _check_bullet_alien_collisions(self):
        '''Respond to bullet-alien collision'''
        # Remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            self.explosion_sound.play()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_alien()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    #region SpawnRandomAliens
    def _delayed_alien_spawn(self):
        '''Creates new aliens at random intervals'''
        current_time = time.time()
        if current_time - self.last_alien_spawn_time > self.alien_spawn_delay:
            self._create_alien()

            # Reset timer and generate a new random delay
            self.last_alien_spawn_time = current_time
            self.alien_spawn_delay = random.uniform(1, 6)

    def _create_alien(self):
        '''Create an alien with random coordinates within screen bounds'''
        new_alien = Alien(self)

        # Spawn alien in a random x, y coordinate
        # But no lower than the middle of the screen
        new_alien.rect.x = random.randint(10, 1140)
        new_alien.rect.y = random.randint(0,400)  # It's always adding to 0 for some reason
        self.aliens.add(new_alien)
    #endregion
    
    def _update_aliens(self):
        '''Update collision status and show alien count offscreen'''
        
        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        # self._check_aliens_bottom()

        # Print aliens that go offscreen
        self._track_aliens()
    
    def _ship_hit(self):
        '''Respond to the ship being hit by an alien'''
        if self.stats.ships_left > 0:
            # Decrement ships_left and update scoreboard
            self.stats.ships_left -= 1
            # self.sb.prep_ships()

            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            # self._create_alien()
            self.ship.center_ship()

            # Pause
            time.sleep(1)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    #region OffscreenAliens
    def _remove_offscreen_aliens(self):
        '''Remove alien that go offscreen'''
        for alien in self.offscreen_aliens.copy():
            self.aliens.remove(alien)

        self.offscreen_aliens.clear()

    def _track_aliens(self):
        '''Keep track of the amount of aliens offscreen'''
        for alien in self.aliens.copy():
            if alien.rect.bottom >= self.settings.screen_height:
                if alien not in self.offscreen_aliens:
                    self.offscreen_aliens.append(alien)

        print(len(self.offscreen_aliens))  # Shows number of aliens that are offscreen

        self._remove_offscreen_aliens()  # Deletes the alien in the list
    
    #endregion

    '''Disconsider this for now'''
    # def _check_aliens_bottom(self):
    #     '''Check if any aliens have reached the bottom of the screen'''
    #     for alien in self.aliens.sprites():
    #         if alien.rect.bottom >= self.settings.screen_height:
    #             # Treat this the same as if the ship got hit
    #             self._ship_hit()
    #             break

    def _update_screen(self):
        '''Update images on the screen, and flip to the new screen'''
        self.screen.blit(self.settings.bg_img, (0, 0))
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw score information
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.game_active:
            mouse_pos = pygame.mouse.get_pos()
            self.play_button.update(mouse_pos)
            self.play_button.draw_button()

        self.aliens.update()
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
