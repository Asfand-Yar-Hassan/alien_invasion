import sys
import pygame

class AlienInvasion:
 """Overall class to manage assets and behaviour"""
 def __init__(self):
  """Initializes the game, and create the game resources"""
  pygame.init()
  self.clock = pygame.time.Clock()
  
  self.screen = pygame.display.set_mode((1200, 800))
  pygame.display.set_caption("Alien Invasion")
  
  # Set the background color
  self.bg_color = (230, 230, 230)
  
 def run_game(self):
  """Start the main loop for the game"""
  while True:
   # Watch for keyboard game and mouse events
   for event in pygame.event.get():
    if event == pygame.QUIT:
     sys.exit()
    
    # Redraw the screen during each iteration through the loop
    self.screen.fill(self.bg_color)
    
   # Make the screen visible
   pygame.display.flip()
   self.clock.tick(60)

if __name__ == "__main__":
  # Make a game instance, and run the game
  ai = AlienInvasion()
  ai.run_game()