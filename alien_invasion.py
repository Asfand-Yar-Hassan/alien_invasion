import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

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
  
  self.ship = Ship(self)
  self.bullets = pygame.sprite.Group()
  self.aliens = pygame.sprite.Group()
  
  self._create_fleet()
  
  
 def run_game(self):
  """Start the main loop for the game"""
  while True:
   self.check_events() 
   self.ship.update()
   self.update_bullets()
   self._update_aliens()
   self.update_screen()
   self.clock.tick(60)
  
 def check_events(self):
   # Watch for keyboard game and mouse events
   for event in pygame.event.get():
    if event == pygame.QUIT:
     sys.exit()
    
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
 
 def fire_bullet(self):
  """Create a new bullet and add it to the group"""
  if len(self.bullets) < self.settings.bullets_allowed:
   new_bullet = Bullet(self)
   self.bullets.add(new_bullet) 
   
 def update_bullets(self):
  self.bullets.update()
   # Get rid of bullets which have disappeared from the screen
  for bullet in self.bullets.copy():
    if bullet.rect.bottom <= 0:
     self.bullets.remove(bullet)
     
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
   # Make the screen visible
   pygame.display.flip()

if __name__ == "__main__":
  # Make a game instance, and run the game
  ai = AlienInvasion()
  ai.run_game()