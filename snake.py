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

      pg.display.init()
      pg.font.init()
      pg.mixer.init()

      self.screen = pg.display.set_mode((self.screen_w, self.screen_h))
      pg.display.set_caption("Snake Game")

   
   def mainloop(self):
      while True:
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_UP:
                  

         self.screen.fill(self.bg_color)

         # Draw straight lines
         self.draw_straight_lines()

         # Draw Guti
         for color, identifier, index in gutis_assign:
            position = self.index_to_position(index)
            self.draw_guti(position, color)

            if selected_guti_identifier == identifier:
              # self.move_eligiblity(selected_guti_identifier)
              self.move_fight(selected_guti_identifier)

         # Display scores
         for index, pleyar in enumerate(self.board):
            score = 16 - len(pleyar)
            pos = (self.space, self.space + self.line_gap / 2) if index == 1 else\
               (self.screen_w - self.space - 56, self.screen_h - self.space - 10 - (self.line_gap / 2))
            self.draw_text(f"Score: {score}", pos)

         if is_game_over:
            pygame.draw.circle(self.screen, self.protagonist_color if is_game_over == 0 else self.antagonist_color, (self.screen_w / 2, self.screen_h / 2), 100)
            font = pygame.font.Font(None, 24)
            text_surface = font.render("Game Over", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen_w / 2, self.screen_h / 2))
            self.screen.blit(text_surface,text_rect)

         pygame.display.flip()