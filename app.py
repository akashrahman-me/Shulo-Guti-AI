import pygame
import sys
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "50, 308"


class GameEnv:
    def __init__(self):
        self.straight_lines = [
            # Horizontal
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9, 10, 11],
            [12, 13, 14, 15, 16],
            [17, 18, 19, 20, 21],
            [22, 23, 24, 25, 26],
            [27, 28, 29, 30, 31],
            [32, 33, 34],
            [35, 36, 37],

            # Vertical
            [7, 12, 17, 22, 27],
            [8, 13, 18, 23, 28],
            [2, 5, 9, 14, 19, 24, 29, 29, 33, 36],
            [10, 15, 20, 25, 30],
            [11, 16, 21, 26, 31],

            # Diagonal
            [1, 4, 9, 15, 21],
            [7, 13, 19, 25, 31],
            [17, 23, 29, 34, 37],
            [3, 6, 9, 13, 17],
            [11, 15, 19, 23, 27],
            [21, 25, 29, 32, 35],
        ]

        self.board = [
            [['d47', 1], ['RvO', 2], ['fHD', 3], ['qOY', 4], ['AET', 5], ['tDy', 6], ['hiF', 7], ['rZs', 8], ['kM1', 9], ['AOQ', 10], ['P3U', 11], ['ZMP', 12], ['jCA', 13], ['Kdr', 14], ['qsl', 15], ["pG1", 16]],
            [['PPA', 22], ['wau', 23], ['QHH', 24], ['MG6', 25], ['qme', 26], ['JX7', 27], ['pkz', 28], ['COl', 29], ['ae6', 30], ['m1i', 31], ['CzZ', 32], ['ZIk', 33], ['26o', 34], ['yq7', 35], ['aLN', 36], ['MS2', 37]]
        ]

        self.current_turn = 0  # protagonist (0) or antagonist (1)

    def index_to_identifier(self, index):
        for row in self.board:
            for cell in row:
                if cell[1] == index:
                    return cell[0]
        return False

    def remove_cell_by_identifier(self, identifier):
        for row in self.board:
            for cell in row:
                if cell[0] == identifier:
                    row.remove(cell)
                    return self.board
        return self.board

    def identifier_to_index(self, key):
        for sublist in self.board:
            for pair in sublist:
                if pair[0] == key:
                    return pair[1]
        return False

    def index_to_identifier_based_ct(self, index):
        ct = (self.current_turn + 1) % 2
        for cell in self.board[ct]:
            if cell[1] == index:
                return cell[0]
        return False

    def replace_index_by_code(self, code, new_index):
        for sublist in self.board:
            for item in sublist:
                if item[0] == code:
                    item[1] = new_index
                    return self.board
        return self.board

    def index_to_straight_lines_points(self, index):
        return [line for line in self.straight_lines if index in line]

    def move_eligibility(self, selected_guti_identifier):
        move_eligibilities = []
        index = self.identifier_to_index(selected_guti_identifier)
        connected_lines = [line for line in self.straight_lines if index in line]
        for line in connected_lines:
            total_idx = len(line) - 1
            idx = line.index(index)

            neighbors = []
            if idx == total_idx:
                neighbors.append(line[idx - 1])
            elif idx == 0:
                neighbors.append(line[idx + 1])
            else:
                neighbors.extend([line[idx - 1], line[idx + 1]])

            for neighbor in neighbors:
                if not self.index_to_identifier(neighbor):
                    move_eligibilities.append(neighbor)
        return move_eligibilities

    def move_fight(self, selected_guti_identifier):
        move_eligibilities = []
        fighted_gutis = []
        index = self.identifier_to_index(selected_guti_identifier)

        connected_lines = [line for line in self.straight_lines if index in line]
        for line in connected_lines:
            total_idx = len(line) - 1
            idx = line.index(index)

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
                if not self.index_to_identifier(fight):
                    middle_guti = None
                    if idx > line.index(fight):
                        middle_guti = line[line.index(fight) + 1]
                    else:
                        middle_guti = line[line.index(fight) - 1]

                    if middle_guti is not None and \
                            self.index_to_identifier_based_ct(middle_guti):
                        move_eligibilities.append(fight)
                        fighted_gutis.append(middle_guti)

        return move_eligibilities, fighted_gutis


class ShuloGutiUI:
    def __init__(self, game_env):
        self.game_env = game_env
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
            expected_y = self.screen_h - self.space
            if abs(x - expected_x) <= tolerance and abs(y - expected_y) <= tolerance:
                return i + 35

        return None

    def mainloop(self):
        selected_guti = None
        while True:
            self.screen.fill(self.bg_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    selected_index = self.position_to_index(mouse_pos)
                    if selected_guti:
                        eligible_moves = self.game_env.move_eligibility(selected_guti)
                        move_eligibilities, fighted_gutis = self.game_env.move_fight(selected_guti)
                        if selected_index in eligible_moves:
                            self.game_env.replace_index_by_code(selected_guti, selected_index)
                            selected_guti = None
                            self.game_env.current_turn = (self.game_env.current_turn + 1) % 2
                        elif selected_index in move_eligibilities:
                            self.game_env.replace_index_by_code(selected_guti, selected_index)
                            selected_guti = None
                            self.game_env.current_turn = (self.game_env.current_turn + 1) % 2
                            for fighted_guti in fighted_gutis:
                                self.game_env.remove_cell_by_identifier(fighted_guti)
                        else:
                            selected_guti = None
                    else:
                        selected_guti = self.game_env.index_to_identifier(selected_index)

            for y in range(5):
                for x in range(5):
                    start_pos = (self.space + self.line_gap * x, self.line_start + self.line_gap * y)
                    end_pos = (self.space + self.line_gap * x, self.line_start + self.line_gap * (y + 1))
                    self.draw_line(start_pos, end_pos)
                    end_pos = (self.space + self.line_gap * (x + 1), self.line_start + self.line_gap * y)
                    self.draw_line(start_pos, end_pos)

            for cell in self.game_env.board[0]:
                index = cell[1]
                i = (index - 1) % 5
                j = (index - 1) // 5
                pos = (self.space + self.line_gap * i, self.line_start + self.line_gap * j)
                self.draw_guti(pos)

            for cell in self.game_env.board[1]:
                index = cell[1]
                i = (index - 1) % 5
                j = (index - 1) // 5
                pos = (self.space + self.line_gap * i, self.line_start + self.line_gap * j)
                self.draw_guti(pos, self.antagonist_color)

            pygame.display.flip()


if __name__ == '__main__':
    game_env = GameEnv()
    shulo_guti_ui = ShuloGutiUI(game_env)
    shulo_guti_ui.mainloop()
