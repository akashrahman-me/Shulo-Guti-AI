class ShuloGutiEnv:
   def __init__(self):
      # Initial board setup for protagonist (0) and antagonist (1)
      self.board = [
          [['d47', 1], ['RvO', 2], ['fHD', 3], ['qOY', 4], ['AET', 5], ['tDy', 6], ['hiF', 7], ['rZs', 8], ['kM1', 9], ['AOQ', 10], ['P3U', 11], ['ZMP', 12], ['jCA', 13], ['Kdr', 14], ['qsl', 15], ["pG1", 16]],
          [['PPA', 22], ['wau', 23], ['QHH', 24], ['MG6', 25], ['qme', 26], ['JX7', 27], ['pkz', 28], ['COl', 29], ['ae6', 30], ['m1i', 31], ['CzZ', 32], ['ZIk', 33], ['26o', 34], ['yq7', 35], ['aLN', 36], ['MS2', 37]]
      ]

      self.current_turn = 0

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
   
   def index_to_stright_lines_points(self, index):
      return [line for line in self.straight_lines if index in line]

   
   def move_eligiblity(self, selected_guti_identifier):
      move_eligibilities = []
      index = self.identifier_to_index(selected_guti_identifier)
      position = self.index_to_position(index)

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

         #  for x in move_eligibilities:
         #      pos = self.index_to_position(x)
         #      pygame.draw.circle(self.screen, (255, 255, 255), pos, 12, 2)

      return {
         "move_eligibilities_index": move_eligibilities,
         "selected_index": index
      }

   def step(self, action):
      # action = [index, index]
      pass