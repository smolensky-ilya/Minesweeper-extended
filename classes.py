import pygame
import random
from time import sleep


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

        self.max_bombs = max_bombs
        self.total_tiles = dimensions * dimensions
        self.safe_tiles = self.total_tiles - max_bombs
        self.opened_tiles = 0

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

    def open_tile(self, x, y, draw_object, screen):
        if not (0 <= x < self.dimensions and 0 <= y < self.dimensions):
            return  # the empty RETURN is a must here. It stops the execution of recursion.
        tile = self.field[y][x]
        #if tile.if_open or tile.if_bomb:
        if tile.if_open:
            return
        tile.open_tile()
        # beautifully updating display
        sleep(0.0000001)
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
        def __init__(self, if_bomb):
            self.bombs_around = 0
            self.if_bomb = if_bomb
            self.string = '*B*'
            self.if_open = False
            self.is_flagged = False

        def is_totally_empty(self):
            return not self.if_bomb and self.bombs_around == 0

        def open_tile(self):
            self.if_open = True

        def get_flagged(self):
            self.is_flagged = True if self.is_flagged is False else False

        def __str__(self):
            return self.string if self.if_bomb else str(self.bombs_around)

        def __repr__(self):
            return self.string if self.if_bomb else str(self.bombs_around)


class Inventory:
    def __init__(self):
        self.things_in_the_inventory = []

    def add_to_inventory(self, item):
        present = False
        for i in self.things_in_the_inventory:
            if type(i) == type(item):
                print("it's there")
                i.quantity += 1
                present = True
        if not present:
            print("it's not there")
            item.quantity += 1
            self.things_in_the_inventory.append(item)

    def remove_from_inventory(self, item):
        print('removing it')
        for index, i in enumerate(self.things_in_the_inventory):
            if type(i) == type(item):
                del self.things_in_the_inventory[index]

    def use_an_item(self, item):
        for i in self.things_in_the_inventory:
            if type(i) == type(item):
                i.use()
                if i.quantity <= 0:
                    self.remove_from_inventory(i)
                return True
        return False  # if it's not our there

    def __repr__(self):
        return str([str(item) + " x" + str(item.quantity) for item in self.things_in_the_inventory])

    def __str__(self):
        return str([str(item) + " x" + str(item.quantity) for item in self.things_in_the_inventory])


class Items:
    class DefaultClass:
        def __init__(self, name: str):
            self.quantity = 0
            self.name = name

        def use(self):
            self.quantity -= 1

        def __repr__(self):
            return self.name

        def __str__(self):
            return self.name

    class NextStepImmortality(DefaultClass):
        """
        Make the player immortal on the next opened tile.
        """
        def __init__(self):
            super().__init__(name='Imm')


def main():
    test_inventory = Inventory()
    # adding
    test_inventory.add_to_inventory(Items.NextStepImmortality())
    # adding one more
    test_inventory.add_to_inventory(Items.NextStepImmortality())
    # view inventory
    print(test_inventory)
    # using
    test_inventory.use_an_item(Items.NextStepImmortality())
    # view inventory
    print(test_inventory)
    # using
    print(test_inventory.use_an_item(Items.NextStepImmortality()))
    # view inventory
    print(test_inventory)
    # using
    print(test_inventory.use_an_item(Items.NextStepImmortality()))


if __name__ == '__main__':
    main()
