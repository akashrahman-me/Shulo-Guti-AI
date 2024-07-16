import pygame as pg
import sys
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "50, 308"

class SnakeGame:
   def __init__(self):

      self.screen_w = 400
      self.screen_h = 400
      self.food_size = 20
      self.food_color = (255, 0, 0)
      self.snake_color = (0, 255, 0)

      self.direction = "RIGHT"
      self.snake_length = 5
      self.snake_speed = 10

      pg.display.init()
      pg.font.init()
      pg.mixer.init()

      self.screen = pg.display.set_mode((self.screen_w, self.screen_h))
      pg.display.set_caption("Snake Game")

   
   def run(self):
      while True:
         for event in pg.event.get():
            if event.type == pg.QUIT:
               pg.quit()
               sys.exit()
            if event.type == pg.KEYDOWN:
               if event.key == pg.K_UP:
                  print("Key up is press")
               if event.key == pg.K_DOWN:
                  print("Key down is press")
               if event.key == pg.K_LEFT:
                  print("Key left is press")
               if event.key == pg.K_RIGHT:
                  print("Key right is press")

         self.screen.fill((0, 0, 0))

         # Draw Snake
         for i in range(self.snake_length):
            pg.draw.rect(self.screen, self.snake_color, (i * self.food_size, 0, self.food_size, self.food_size))
            
         pg.display.flip()

game = SnakeGame()
game.run()