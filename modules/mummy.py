import random

class Mummy:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.vision_range = 4

    def move(self, game_map):
        """
        Mueve la momia y devuelve su estado actual ('chase' o 'patrol').
        """
        player = game_map.player
        manhattan_distance = abs(self.row - player.row) + abs(self.col - player.col)

        if manhattan_distance <= self.vision_range:
            self._chase_player(game_map)
            return 'chase'
        else:
            self._move_randomly(game_map)
            return 'patrol'

    def _chase_player(self, game_map):
        player = game_map.player
        d_row = player.row - self.row
        d_col = player.col - self.col

        preferred_directions = []
        if d_row > 0: preferred_directions.append('DOWN')
        if d_row < 0: preferred_directions.append('UP')
        if d_col > 0: preferred_directions.append('RIGHT')
        if d_col < 0: preferred_directions.append('LEFT')

        random.shuffle(preferred_directions)

        for direction in preferred_directions:
            if self._can_move(direction, game_map):
                new_pos = self._get_new_pos_from_direction(direction)
                if game_map.is_valid_move(new_pos, entity_type='mummy'):
                    self._update_and_move(new_pos)
                    return

        self._move_randomly(game_map)

    def _move_randomly(self, game_map):
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        random.shuffle(directions)

        for direction in directions:
            if self._can_move(direction, game_map):
                new_pos = self._get_new_pos_from_direction(direction)
                if game_map.is_valid_move(new_pos, entity_type='mummy'):
                    self._update_and_move(new_pos)
                    break

    def _can_move(self, direction, game_map):
        """Comprueba si hay una pared en la dirección dada."""
        current_cell = game_map.list_cells[self.row][self.col]
        return not current_cell.walls[direction]

    def _get_new_pos_from_direction(self, direction):
        if direction == 'UP': return (self.row - 1, self.col)
        if direction == 'DOWN': return (self.row + 1, self.col)
        if direction == 'LEFT': return (self.row, self.col - 1)
        if direction == 'RIGHT': return (self.row, self.col + 1)
        return (self.row, self.col)

    def _update_and_move(self, new_pos):
        self.row, self.col = new_pos
