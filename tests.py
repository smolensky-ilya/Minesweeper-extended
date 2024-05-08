import random


class Field:
    def __init__(self, max_bombs, dimensions):
        if max_bombs <= dimensions * dimensions:
            tiles = [self.Tile(if_bomb=False) for _ in range((dimensions*dimensions) - max_bombs)] + \
                    [self.Tile(if_bomb=True) for _ in range(max_bombs)]
            random.shuffle(tiles)
            self.field = [tiles[i:i+dimensions] for i in range(0, len(tiles), dimensions)]
        else:
            self.field = [[self.Tile(if_bomb=True) for _ in range(dimensions)] for _ in range(dimensions)]

    def get(self):
        return self.field

    def __str__(self):
        return str(self.field)

    def __repr__(self):
        return str(self.field)

    class Tile:
        def __init__(self, if_bomb):
            self.string = 'lol'
            self.if_bomb = if_bomb

        def __str__(self):
            return self.string

        def __repr__(self):
            return '*******' if self.if_bomb else 'No_bomb'


def main():
    dim = 10
    bombs = 5
    #print(Field(max_bombs=bombs, dimensions=dim))
    for line in Field(max_bombs=bombs, dimensions=dim).get():
        print(line)


if __name__ == "__main__":
    main()
