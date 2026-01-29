import pygame
import random
from modules.cell import Cell
from modules.player import Player
from modules.mummy import Mummy
from modules.config import SIZE_CELL, COLOR_VISITED, COLOR_TREASURE, COLOR_MUMMY, COLOR_PLAYER, COLOR_BLACK, MARGIN, COLOR_SLIME, COLOR_PASSAGE


class GameMap:
    def __init__(self):
        self.list_cells = self.load_map()
        self.player = None
        self.mummy = None
        self.treasure_pos = None
        self.holes = []
        self.setup_map()
        self.create_walls(density=0.2)

    @staticmethod
    def load_map():
        return [[Cell(row, col) for col in range(8)] for row in range(8)]

    def create_walls(self, density):
        for r in range(8):
            for c in range(8):
                if c < 7 and random.random() < density:
                    self.list_cells[r][c].walls['RIGHT'] = True
                    self.list_cells[r][c+1].walls['LEFT'] = True
                if r < 7 and random.random() < density:
                    self.list_cells[r][c].walls['DOWN'] = True
                    self.list_cells[r+1][c].walls['UP'] = True

    def setup_map(self):
        for _ in range(3):
            self._place_hole()
        self._place_treasure()
        self._place_player()
        self._place_mummy()
        for _ in range(5):
            self._place_reward(50)

    def _get_random_free_cell(self, avoid_slime=False):
        free_cells = self.get_free_cells(avoid_slime=avoid_slime)
        return random.choice(free_cells) if free_cells else None

    def _place_slime_around(self, row, col):
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < 8 and 0 <= c < 8 and not self.list_cells[r][c].is_hole:
                    self.list_cells[r][c].has_slime = True

    def _place_hole(self):
        pos = self._get_random_free_cell(avoid_slime=False)
        if pos:
            row, col = pos
            self.list_cells[row][col].is_hole = True
            self.holes.append(pos)
            self._place_slime_around(row, col)

    def _place_treasure(self):
        pos = self._get_random_free_cell(avoid_slime=True)
        if pos:
            self.list_cells[pos[0]][pos[1]].has_treasure = True
            self.treasure_pos = pos

    def _place_mummy(self):
        if not self.player:
            return

        min_distance = 4
        free_cells = self.get_free_cells(avoid_slime=True)

        far_cells = [
            cell for cell in free_cells
            if abs(cell[0] - self.player.row) + abs(cell[1] - self.player.col) >= min_distance
        ]

        pos = random.choice(far_cells) if far_cells else self._get_random_free_cell(avoid_slime=True)

        if pos:
            self.mummy = Mummy(pos[0], pos[1])

    def _place_reward(self, value):
        pos = self._get_random_free_cell(avoid_slime=True)
        if pos:
            self.list_cells[pos[0]][pos[1]].reward_points = value

    def _place_player(self):
        pos = self._get_random_free_cell(avoid_slime=True)
        if pos:
            self.player = Player(pos[0], pos[1])

    def get_free_cells(self, avoid_slime=False):
        occupied_pos = set(self.holes)
        if self.treasure_pos: occupied_pos.add(self.treasure_pos)
        if self.mummy: occupied_pos.add((self.mummy.row, self.mummy.col))
        if self.player: occupied_pos.add((self.player.row, self.player.col))

        free_cells = []
        for r in range(8):
            for c in range(8):
                if (r, c) in occupied_pos:
                    continue
                if avoid_slime and self.list_cells[r][c].has_slime:
                    continue
                free_cells.append((r, c))
        return free_cells

    def _get_cell_color(self, cell, r, c):
        if self.player and (r, c) == (self.player.row, self.player.col):
            return COLOR_PLAYER
        if self.mummy and (r, c) == (self.mummy.row, self.mummy.col):
            return COLOR_MUMMY
        if cell.has_treasure:
            return COLOR_TREASURE
        if cell.has_slime and cell.visited:
            return COLOR_SLIME
        if cell.visited:
            return COLOR_VISITED
        return (50, 50, 50)

    def _draw_passages(self, screen, cell, x, y):
        if not cell.walls['RIGHT']:
            pygame.draw.circle(screen, COLOR_PASSAGE, (x + SIZE_CELL, y + SIZE_CELL / 2), 4)
        if not cell.walls['DOWN']:
            pygame.draw.circle(screen, COLOR_PASSAGE, (x + SIZE_CELL / 2, y + SIZE_CELL), 4)
        if not cell.walls['LEFT']:
            pygame.draw.circle(screen, COLOR_PASSAGE, (x, y + SIZE_CELL / 2), 4)
        if not cell.walls['UP']:
            pygame.draw.circle(screen, COLOR_PASSAGE, (x + SIZE_CELL / 2, y), 4)

    def draw_map(self, screen):
        for row_idx, row in enumerate(self.list_cells):
            for col_idx, cell in enumerate(row):
                if self.player and (row_idx, col_idx) == (self.player.row, self.player.col):
                    cell.visit()

                color = self._get_cell_color(cell, row_idx, col_idx)
                x = MARGIN + col_idx * SIZE_CELL
                y = MARGIN + row_idx * SIZE_CELL

                pygame.draw.rect(screen, color, pygame.Rect(x, y, SIZE_CELL, SIZE_CELL))
                pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect(x, y, SIZE_CELL, SIZE_CELL), 10)
                self._draw_passages(screen, cell, x, y)

    def move_player(self, direction):
        if self.player.move(direction, self):
            new_pos = (self.player.row, self.player.col)
            points = self.list_cells[new_pos[0]][new_pos[1]].visit()
            if points > 0:
                self.player.add_score(points)

    def move_mummy(self):
        if self.mummy:
            return self.mummy.move(self)
        return 'patrol'

    def is_valid_move(self, pos, entity_type='player'):
        row, col = pos
        if not (0 <= row < 8 and 0 <= col < 8):
            return False
        if entity_type == 'mummy' and self.list_cells[row][col].is_hole:
            return False
        return True

    def check_victory(self):
        return (self.player.row, self.player.col) == self.treasure_pos

    def check_lose(self):
        player_pos = (self.player.row, self.player.col)
        if player_pos in self.holes: return True
        if self.mummy and player_pos == (self.mummy.row, self.mummy.col): return True
        return False
