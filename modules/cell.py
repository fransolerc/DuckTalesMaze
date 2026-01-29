class Cell:
    def __init__(self, row, column, has_treasure=False, is_hole=False, reward_points=0):
        self.row = row
        self.column = column
        self.has_treasure = has_treasure
        self.is_hole = is_hole
        self.has_slime = False
        self.reward_points = reward_points
        self.visited = False

        # Diccionario para almacenar las paredes. True significa que hay una pared.
        self.walls = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}

    def __str__(self):
        # ... (el resto del método __str__ no necesita cambios)
        if self.has_treasure:
            return 'T'
        elif self.is_hole:
            return 'O'
        # ...

    def visit(self):
        self.visited = True
        if self.reward_points > 0:
            reward = self.reward_points
            self.reward_points = 0
            return reward
        return 0
