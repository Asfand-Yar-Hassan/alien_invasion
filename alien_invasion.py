import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet

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
  
  
 def run_game(self):
  """Start the main loop for the game"""
  while True:
   self.check_events() 
   self.ship.update()
   self.update_bullets()
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
 
 def update_screen(self):
   # Redraw the screen during each iteration through the loop
   self.screen.fill(self.settings.bg_color)
   
   for bullet in self.bullets.sprites():
    bullet.draw_bullet()
   
   self.ship.blitme()
    
   # Make the screen visible
   pygame.display.flip()

if __name__ == "__main__":
  # Make a game instance, and run the game
  ai = AlienInvasion()
  ai.run_game()