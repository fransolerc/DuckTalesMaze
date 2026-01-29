class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.score = 0

    def move(self, direction, game_map):
        """
        Mueve al jugador si no hay una pared y el movimiento es válido.
        """
        current_cell = game_map.list_cells[self.row][self.col]

        # Comprobar si hay una pared en la dirección del movimiento
        if current_cell.walls[direction]:
            return False

        if direction == 'UP':
            new_pos = (self.row - 1, self.col)
        elif direction == 'DOWN':
            new_pos = (self.row + 1, self.col)
        elif direction == 'LEFT':
            new_pos = (self.row, self.col - 1)
        elif direction == 'RIGHT':
            new_pos = (self.row, self.col + 1)
        else:
            return False

        if game_map.is_valid_move(new_pos, entity_type='player'):
            self.row, self.col = new_pos
            return True
        return False

    def add_score(self, points):
        self.score += points

    def get_score(self):
        return self.score
