import pygame
import random


class Field:
    def __init__(self, max_bombs: int, dimensions: int, possible_inventory_items: dict):
        self.dimensions: int = dimensions

        if max_bombs <= dimensions * dimensions:
            tiles = [self.Tile(if_bomb=False,
                               possible_inventory_items=possible_inventory_items)
                     for _ in range((dimensions*dimensions) - max_bombs)] + \
                    [self.Tile(if_bomb=True,
                               possible_inventory_items=possible_inventory_items) for _ in range(max_bombs)]
            random.shuffle(tiles)
            self.field: list = [tiles[i:i+dimensions] for i in range(0, len(tiles), dimensions)]
        else:
            self.field: list = [[self.Tile(if_bomb=True,
                                 possible_inventory_items=possible_inventory_items)
                                 for _ in range(dimensions)] for _ in range(dimensions)]

        self.max_bombs: int = max_bombs
        self.total_tiles: int = dimensions * dimensions
        self.safe_tiles: int = self.total_tiles - max_bombs
        self.opened_tiles: int = 0

    def get(self):
        changed_field: list = self.field
        for y in range(self.dimensions):
            for x in range(self.dimensions):
                if not changed_field[y][x].if_bomb:
                    changed_field[y][x].bombs_around = self.count_bombs_around(x, y)
                    changed_field[y][x].generate_an_item()  # item generation
        return changed_field

    def count_bombs_around(self, x, y):
        counted_bombs = 0
        for i in range(-1, 2):  # this stuff generates the numbers -1, 0 and 1 to access adjacent cells
            for j in range(-1, 2):
                nx, ny = x + i, y + j
                if 0 <= nx < self.dimensions and 0 <= ny < self.dimensions:
                    if self.field[ny][nx].if_bomb:
                        counted_bombs += 1
        return counted_bombs

    def open_tile(self, x: int, y: int, draw_object, screen):
        if not (0 <= x < self.dimensions and 0 <= y < self.dimensions):
            return  # the empty RETURN is a must here. It stops the execution of recursion.
        tile = self.field[y][x]
        if tile.if_open:
            return
        tile.open_tile()
        draw_object(screen)
        pygame.display.update()
        self.opened_tiles += 1
        if tile.is_totally_empty():  # checking and opening adjacent
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if j != 0 or i != 0:
                        self.open_tile(x + i, y + j, draw_object, screen)

    def open_all_tiles(self):
        for row in self.field:
            for tile in row:
                tile.if_open = True

    def count_remaining_tiles(self):
        return self.total_tiles - self.opened_tiles - self.max_bombs

    def __str__(self):
        return str(self.field)

    def __repr__(self):
        return str(self.field)

    class Tile:
        def __init__(self, if_bomb: bool, possible_inventory_items: dict):
            self.bombs_around = 0
            self.if_bomb = if_bomb
            self.bomb_string = '*B*'
            self.if_open = False
            self.is_flagged = False
            self.possible_inventory_items = possible_inventory_items
            self.item = None
            self.item_taken = False

        def is_totally_empty(self):
            return not self.if_bomb and self.bombs_around == 0

        def open_tile(self):
            self.if_open = True

        def get_flagged(self):
            self.is_flagged = True if self.is_flagged is False else False

        def generate_an_item(self):
            if not self.if_bomb and self.bombs_around == 0:
                for item, probability in self.possible_inventory_items.items():  # adding items with certain probability
                    if self.item is not None:
                        break
                    self.item = item if random.random() < probability else None

        def __str__(self):
            return self.bomb_string if self.if_bomb else str(self.bombs_around)

        def __repr__(self):
            return self.bomb_string if self.if_bomb else str(self.bombs_around)


if __name__ == '__main__':
    pass
