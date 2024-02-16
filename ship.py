import pygame

class Ship:
 def __init__(self, ai_game):
  self.screen = ai_game.screen
  self.settings = ai_game.settings
  self.screen_rect = ai_game.screen.get_rect()
  
  # Load the ship's image
  self.image = pygame.image.load("assets/ship.bmp")
  self.rect = self.image.get_rect()
  
  # Start the game with the ship at the middle of the bottom of the screen
  self.rect.midbottom = self.screen_rect.midbottom
  
  # Store a float for the ship's horizontal position
  self.x = float(self.rect.x)
  
  # Movement flag. Start with a ship that's not moving
  self.moving_rirght = False
  self.moving_left = False
 
 def update(self):
  """Update ship's position"""
  if self.moving_rirght and self.rect.right < self.screen_rect.right:
   self.x += self.settings.ship_speed
  if self.moving_left and self.rect.left > 0:
   self.x -= self.settings.ship_speed
  
  self.rect.x = self.x

 def blitme(self):
  self.screen.blit(self.image, self.rect)