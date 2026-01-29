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
            self.place_hole()
        self.place_element('treasure')
        self.place_element('mummy')
        for _ in range(5):
            self.place_element('reward', 50)
        self.place_element('player')

    def place_hole(self):
        free_cells = self.get_free_cells()
        if not free_cells: return
        row, col = random.choice(free_cells)
        self.list_cells[row][col].is_hole = True
        self.holes.append((row, col))
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < 8 and 0 <= c < 8 and not self.list_cells[r][c].is_hole:
                    self.list_cells[r][c].has_slime = True

    def place_element(self, tipo, valor=0):
        free_cells = self.get_free_cells(avoid_slime=True)
        if not free_cells: return
        row, col = random.choice(free_cells)
        cell = self.list_cells[row][col]
        if tipo == 'treasure':
            cell.has_treasure = True
            self.treasure_pos = (row, col)
        elif tipo == 'mummy': self.mummy = Mummy(row, col)
        elif tipo == 'reward': cell.reward_points = valor
        elif tipo == 'player': self.player = Player(row, col)

    def get_free_cells(self, avoid_slime=False):
        occupied_pos = set(self.holes)
        if self.treasure_pos: occupied_pos.add(self.treasure_pos)
        if self.mummy: occupied_pos.add((self.mummy.row, self.mummy.col))
        if self.player: occupied_pos.add((self.player.row, self.player.col))
        free_cells = []
        for r in range(8):
            for c in range(8):
                is_occupied = (r, c) in occupied_pos
                cell = self.list_cells[r][c]
                if not cell.is_hole and not is_occupied:
                    if avoid_slime and cell.has_slime: continue
                    free_cells.append((r, c))
        return free_cells

    def draw_map(self, screen):
        for row_idx, row in enumerate(self.list_cells):
            for col_idx, cell in enumerate(row):
                color = (50, 50, 50) # Color por defecto para celdas no visitadas

                # El orden de las comprobaciones es importante aquí
                if cell.has_treasure:
                    color = COLOR_TREASURE
                elif cell.has_slime: # El lodo es visible siempre si está presente
                    color = COLOR_SLIME
                elif cell.visited: # Celda visitada normal (no lodo, no tesoro)
                    color = COLOR_VISITED
                # Los agujeros se pintarán con el color que les corresponda (lodo, visitado o por defecto)

                # El jugador y la momia se dibujan encima de otros colores
                if self.mummy and (row_idx, col_idx) == (self.mummy.row, self.mummy.col):
                    color = COLOR_MUMMY
                if self.player and (row_idx, col_idx) == (self.player.row, self.player.col):
                    color = COLOR_PLAYER

                x = MARGIN + col_idx * SIZE_CELL
                y = MARGIN + row_idx * SIZE_CELL

                pygame.draw.rect(screen, color, pygame.Rect(x, y, SIZE_CELL, SIZE_CELL))
                pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect(x, y, SIZE_CELL, SIZE_CELL), 10)

                if not cell.walls['RIGHT']: pygame.draw.circle(screen, COLOR_PASSAGE, (x + SIZE_CELL, y + SIZE_CELL / 2), 4)
                if not cell.walls['DOWN']: pygame.draw.circle(screen, COLOR_PASSAGE, (x + SIZE_CELL / 2, y + SIZE_CELL), 4)
                if not cell.walls['LEFT']: pygame.draw.circle(screen, COLOR_PASSAGE, (x, y + SIZE_CELL / 2), 4)
                if not cell.walls['UP']: pygame.draw.circle(screen, COLOR_PASSAGE, (x + SIZE_CELL / 2, y), 4)

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
        if not (0 <= row < 8 and 0 <= col < 8): return False
        if entity_type == 'mummy':
            if self.list_cells[row][col].is_hole: return False
        return True

    def check_victory(self):
        return (self.player.row, self.player.col) == self.treasure_pos

    def check_lose(self):
        player_pos = (self.player.row, self.player.col)
        if player_pos in self.holes: return True
        if self.mummy and player_pos == (self.mummy.row, self.mummy.col): return True
        return False
