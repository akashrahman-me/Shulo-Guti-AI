import pygame
import sys
import os
from classes.ShuloGutiEnv import ShuloGutiEnv

os.environ['SDL_VIDEO_WINDOW_POS'] = "50, 308"


class ShuloGuti (ShuloGutiEnv):
    def __init__(self):
        super().__init__()

        self.screen_w = 343
        self.screen_h = 500
        self.bg_color = (80, 80, 80)
        self.line_color = (200, 200, 200)
        self.circle_size = 10

        self.line_gap = 75
        self.line_start = 100
        self.space = 20

        self.protagonist_color = (0, 0, 255)
        self.antagonist_color = (255, 0, 0)

        pygame.display.init()
        pygame.font.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption('ShuloGuti Game')

    def draw_line(self, start_pos, end_pos, width=2):
        pygame.draw.line(self.screen, self.line_color, start_pos, end_pos, width)

    def draw_guti(self, position, color=None):
        if color is None:
            color = self.protagonist_color
        pygame.draw.circle(self.screen, color, position, self.circle_size)

   
    def position_to_index(self, position):
        x, y = position
        tolerance = 10  # Half of the circle size to create a bounding box
        
        grid = [(i, j) for j in range(5) for i in range(5)]
        
        # Check for indices 7 to 31
        for index in range(7, 32):
            i, j = grid[index - 7]
            expected_x = self.space + (self.circle_size / 3) + self.line_gap * i
            expected_y = self.line_start + (self.circle_size / 3) + self.line_gap * j
            if abs(x - expected_x) <= tolerance and abs(y - expected_y) <= tolerance:
                return index
        
        # Check for indices 1 to 3
        for i in range(3):
            expected_x = self.line_gap + self.space + (self.circle_size / 3) + self.line_gap * i
            expected_y = self.space + self.circle_size / 2
            if abs(x - expected_x) <= tolerance and abs(y - expected_y) <= tolerance:
                return i + 1

        # Check for indices 4 to 6
        for i in range(1, 4):
            expected_x = self.line_gap * 0.5 * i + self.space + (self.circle_size / 3) + self.line_gap
            expected_y = self.space + (self.circle_size / 10) + (self.line_gap / 2)
            if abs(x - expected_x) <= tolerance and abs(y - expected_y) <= tolerance:
                return i + 3

        # Check for indices 35 to 37
        for i in range(3):
            expected_x = self.line_gap + self.space + (self.circle_size / 3) + self.line_gap * i
            expected_y = self.space + (self.circle_size / 2) + self.line_gap * 6
            if abs(x - expected_x) <= tolerance and abs(y - expected_y) <= tolerance:
                return i + 35

        # Check for indices 32 to 34
        for i in range(1, 4):
            expected_x = self.line_gap * 0.5 * i + self.space + (self.circle_size / 3) + self.line_gap
            expected_y = self.space + (self.circle_size / 1) + (self.line_gap / 2) + self.line_gap * 5
            if abs(x - expected_x) <= tolerance and abs(y - expected_y) <= tolerance:
                return i + 31

        return None  # If no index matches the given position

    def index_to_position(self, index=1):
        grid = [(x, y) for y in range(5) for x in range(5)]
        for i in range(5 if (index >= 7) and (index <= 31) else 0):
            for j in range(5):
                if i == grid[index - 7][0] and j == grid[index - 7][1]:
                    return (
                        self.space + (self.circle_size / 3) + self.line_gap * i,
                        self.line_start + (self.circle_size / 3) + self.line_gap * j
                    )

        for i in range(index if index <= 3 else 0):
            if index == i + 1:
                return (
                    self.line_gap + self.space + (self.circle_size / 3) + self.line_gap * i,
                    self.space + self.circle_size / 2
                )

        for i in range(1, 4 if (index >= 4) and (index <= 6) else 0):
            if index + 1 == i + 4:
                return (
                    self.line_gap * 0.5 * i + self.space + (self.circle_size / 3) + self.line_gap,
                    self.space + (self.circle_size / 10) + (self.line_gap / 2)
                )

        for i in range(3 if (index >= 35) and (index <= 37) else 0):
            if index == i + 35:
                return (
                    self.line_gap + self.space + (self.circle_size / 3) + self.line_gap * i,
                    self.space + (self.circle_size / 2) + self.line_gap * 6
                )

        for i in range(1, 4 if (index >= 32) and (index <= 34) else 0):
            if index + 1 == i + 32:
                return (
                    self.line_gap * 0.5 * i + self.space + (self.circle_size / 3) + self.line_gap,
                    self.space + (self.circle_size / 1) + (self.line_gap / 2) + self.line_gap * 5
                )

    def is_guti_clicked(self, guti_pos, mouse_pos):
        distance = ((guti_pos[0] - mouse_pos[0]) ** 2 + (guti_pos[1] - mouse_pos[1]) ** 2) ** 0.5
        return distance <= self.circle_size

    def draw_text(self, text, position, font_size=20, color=(255, 255, 255)):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, position)
    
    def draw_straight_lines(self):
        for index, line in enumerate(self.straight_lines):
            start_pos = self.index_to_position(line[0])
            end_pos = self.index_to_position(line[-1])
            self.draw_line(start_pos, end_pos, 2 if index < 14 else 3)

    
    def move_fight(self, selected_guti_identifier):
        move_eligibilities = []
        fighted_gutis = []
        index = self.identifier_to_index(selected_guti_identifier)

        connected_lines = [line for line in self.straight_lines if index in line]
        for line in connected_lines:
            total_idx = len(line) - 1
            idx = line.index(index) # Focesed index in line

            fights = []
            if idx == total_idx - 1 or idx == total_idx:
                fights.append(line[idx - 2])
            elif idx == 0:
                fights.append(line[idx + 2])
            else:
                fights.append(line[idx - 2])
                try:
                    fights.append(line[idx + 2])
                except IndexError as e:
                    print(e)

            for fight in fights:
                if not self.index_to_identifier(fight): # Empty space for fight move
                    middle_guti = None
                    if idx > line.index(fight):
                        middle_guti = line[line.index(fight) + 1]
                    else:
                        middle_guti = line[line.index(fight) - 1]

                    if middle_guti is not None and \
                        self.index_to_identifier_based_ct(middle_guti):
                        move_eligibilities.append(fight)
                        fighted_gutis.append(middle_guti) 

            for x in move_eligibilities:
                pos = self.index_to_position(x)
                pygame.draw.circle(self.screen, (255, 255, 255), pos, 12, 2)

        return (move_eligibilities, fighted_gutis) # list of index

    def run(self):
        selected_guti_identifier = None
        is_game_over = False

        while True:
            # position, color, identifier, index
            gutis_assign = []
            for i, pleyar in enumerate(self.board):
                for identifier, index in pleyar:
                    gutis_assign.append((
                        self.protagonist_color if i == 0 else self.antagonist_color,
                        identifier,
                        index
                    ))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    # Selection of Guti
                    for color, identifier, index in gutis_assign:
                        eligiblity = None
                        if self.current_turn == 0:
                            eligiblity = any(item[0] == identifier for item in self.board[0])
                        else:
                            eligiblity = any(item[0] == identifier for item in self.board[1])

                        position = self.index_to_position(index)
                        if self.is_guti_clicked(position, mouse_pos) and eligiblity:
                            selected_guti_identifier = identifier

                    # Movement of Guti
                    if selected_guti_identifier is not None:
                        index = self.identifier_to_index(selected_guti_identifier)
                        move_index = self.position_to_index(mouse_pos)
                        eligible_places = self.move_eligiblity(selected_guti_identifier)
                        eligible_places = eligible_places['move_eligibilities_index']
                        fight_els, fighted_els = self.move_fight(selected_guti_identifier)

                        # Only movement
                        if move_index is not None and move_index in eligible_places:
                            self.replace_index_by_code(selected_guti_identifier, move_index)
                            self.current_turn = (self.current_turn + 1) % 2
                            selected_guti_identifier = None

                        # Move with fight
                        if move_index is not None and move_index in fight_els:
                            fidx = fight_els.index(move_index)
                            fdidx = fighted_els[fidx]
                            self.remove_cell_by_identifier(self.index_to_identifier(fdidx))
                            self.replace_index_by_code(selected_guti_identifier, move_index)
                            selected_guti_identifier = None

                            # Check if game over
                            if any(len(row) <= 3 for row in self.board):
                                is_game_over = self.current_turn
                            self.current_turn = (self.current_turn + 1) % 2

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


if __name__ == "__main__":
    game = ShuloGuti()
    game.run()
