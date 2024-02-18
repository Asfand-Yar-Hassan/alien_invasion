from asyncio import sleep
import sys
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button

class AlienInvasion:
 """Overall class to manage assets and behaviour"""
 def __init__(self):
  """Initializes the game, and create the game resources"""
  pygame.init()
  self.clock = pygame.time.Clock()
  self.settings = Settings()
  
  self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
  self.settings.screen_width = self.screen.get_rect().width
  self.settings.screen_height = self.screen.get_rect().height
  pygame.display.set_caption("Alien Invasion")
  
  self.stats = GameStats(self)
  
  self.ship = Ship(self)
  self.bullets = pygame.sprite.Group()
  self.aliens = pygame.sprite.Group()
  
  self._create_fleet()
  self.game_active = False
  
  self.play_button = Button(self, "Play")
  
  
 def run_game(self):
  """Start the main loop for the game"""
  while True:
   self.check_events()
   if self.game_active:
     self.ship.update()
     self._update_bullets()
     self._update_aliens()
   self.update_screen()
   self.clock.tick(60)
  
 def check_events(self):
   # Watch for keyboard game and mouse events
   for event in pygame.event.get():
    if event == pygame.QUIT:
     sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN:
      mouse_pos = pygame.mouse.get_pos()
      self._check_play_button(mouse_pos)
    elif event.type == pygame.KEYDOWN:
     self.check_key_down_events(event)
    elif event.type == pygame.KEYUP:
     self.check_key_up_events(event)
     
 
 def check_key_down_events(self, event):
  """Check for key pressing events"""
  if event.key == pygame.K_q:
   sys.exit()
  elif event.key == pygame.K_RIGHT:
      self.ship.moving_rirght = True
  elif event.key == pygame.K_LEFT:
      self.ship.moving_left = True
  elif event.key == pygame.K_SPACE:
   self.fire_bullet()
 
 def check_key_up_events(self, event):
  if event.key == pygame.K_RIGHT:
      self.ship.moving_rirght = False
  elif event.key == pygame.K_LEFT:
      self.ship.moving_left =False
  
 def _check_play_button(self, mouse_pos):
  button_clicked = self.play_button.rect.collidepoint(mouse_pos)
  if button_clicked and not self.game_active:
    self.settings.initialize_dynamic_settings()
    pygame.mouse.set_visible(False)
    self.game_active = True    
 
 def fire_bullet(self):
  """Create a new bullet and add it to the group"""
  if len(self.bullets) < self.settings.bullets_allowed:
   new_bullet = Bullet(self)
   self.bullets.add(new_bullet) 
   
 def _update_bullets(self):
  self.bullets.update()
   # Get rid of bullets which have disappeared from the screen
  for bullet in self.bullets.copy():
    if bullet.rect.bottom <= 0:
     self.bullets.remove(bullet)
  self._check_bullet_collisions()
    
 def _check_bullet_collisions(self):
    # Detect collisions, remove the alien and bullet
   pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
   # Create a new fleet if the existing fleet is destroyed
   if not self.aliens:
    self.bullets.empty()
    self._create_fleet()
    self.settings.increase_speed()
    
     
 def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height
 
 def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
   
 def _update_aliens(self):
   self._check_fleet_edges()
   self.aliens.update()
   self._check_ship_collision()
   self._check_aliens_bottom()
   
 def _check_ship_collision(self):
     if pygame.sprite.spritecollideany(self.ship, self.aliens):
       self._ship_hit()
      
 def _check_aliens_bottom(self):
   for alien in self.aliens.sprites():
     if alien.rect.bottom >= self.settings.screen_height:
       self._ship_hit()
       break     
       
 def _ship_hit(self):
   if self.stats.ships_left > 0:
    self.stats.ships_left -= 1
   
    # Get rid off bullets and aliens once the ship is hit
    self.bullets.empty()
    self.aliens.empty()
    # Create a new ship and center it
    self._create_fleet()
    self.ship.center_ship()
    sleep(0.5)
   else:
     self.game_active = False
     pygame.mouse.set_visible(True)
    
 def _check_fleet_edges(self):
   for alien in self.aliens.sprites():
     if alien.check_edges():
       self._change_fleet_direction()
       break
  
 def _change_fleet_direction(self):
   for alien in self.aliens.sprites():
     alien.rect.y += self.settings.fleet_drop_speed
   self.settings.fleet_direction *= -1
  
 def update_screen(self):
   # Redraw the screen during each iteration through the loop
   self.screen.fill(self.settings.bg_color)
   
   for bullet in self.bullets.sprites():
    bullet.draw_bullet()
   
   self.ship.blitme()
   self.aliens.draw(self.screen)
   
   if not self.game_active:
     self.play_button.draw_button()
   
   # Make the screen visible
   pygame.display.flip()

if __name__ == "__main__":
  # Make a game instance, and run the game
  ai = AlienInvasion()
  ai.run_game()