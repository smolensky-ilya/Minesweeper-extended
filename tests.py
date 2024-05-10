import random


class Field:
    def __init__(self, max_bombs, dimensions):
        self.dimensions = dimensions

        if max_bombs <= dimensions * dimensions:
            tiles = [self.Tile(if_bomb=False) for _ in range((dimensions*dimensions) - max_bombs)] + \
                    [self.Tile(if_bomb=True) for _ in range(max_bombs)]
            random.shuffle(tiles)
            self.field = [tiles[i:i+dimensions] for i in range(0, len(tiles), dimensions)]
        else:
            self.field = [[self.Tile(if_bomb=True) for _ in range(dimensions)] for _ in range(dimensions)]

    def get(self):
        changed_field = self.field
        for y in range(self.dimensions):
            for x in range(self.dimensions):
                if not changed_field[y][x].if_bomb:
                    changed_field[y][x].bombs_around = self.count_bombs_around(x, y)
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

    def __str__(self):
        return str(self.field)

    def __repr__(self):
        return str(self.field)

    class Tile:
        def __init__(self, if_bomb):
            self.bombs_around = 0
            self.if_bomb = if_bomb

        def __str__(self):
            return str(self.bombs_around)

        def __repr__(self):
            return 'B' if self.if_bomb else str(self.bombs_around)


def main():
    dim = 10
    bombs = 15
    #print(Field(max_bombs=bombs, dimensions=dim))
    f = Field(max_bombs=bombs, dimensions=dim)
    for line in f.get():
        print(line)
    #print(f.count_bombs_around(1, 0))


if __name__ == "__main__":
    main()
