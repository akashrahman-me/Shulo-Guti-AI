import pygame as pg
import sys
import os

# Something went wrong here.

os.environ['SDL_VIDEO_WINDOW_POS'] = "50, 308"

class SnakeGame:
   def __init__(self):

      self.screen_w = 400
      self.screen_h = 400
      self.food_size = 20
      self.food_color = (255, 0, 0)
      self.snake_color = (0, 255, 0)

      pg.display.init()
      pg.font.init()
      pg.mixer.init()

      self.screen = pg.display.set_mode((self.screen_w, self.screen_h))
      pg.display.set_caption("Snake Game")

   
   def mainloop(self):
      while True: