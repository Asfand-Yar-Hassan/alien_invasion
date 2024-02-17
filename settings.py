class Settings:
 """Class to store all settings for the game"""
 
 def __init__(self):
  """Initialize the game settings"""
  self.screen_width = 1200
  self.screen_height = 600
  self.bg_color = (230,230,230)
  # Ship settings
  self.ship_speed = 3.0
  self.ship_limit = 3
  # Bullet settings
  self.bullet_speed = 2.5
  self.bullet_width = 3
  self.bullet_height = 15
  self.bullet_color = (60, 60, 60)
  self.bullets_allowed = 3
  # Alien speed
  self.alien_speed = 1.0
  self.fleet_drop_speed = 10
  self.fleet_direction = 1