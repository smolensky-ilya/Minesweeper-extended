import random
import pygame


class Game:
    def __init__(self, max_bombs, dimensions):
        # PARAMS
        self.cell_size = 50
        self.menu_height = 40

        self.dimensions = dimensions
        self.max_bombs = max_bombs

        self.window_height = self.dimensions * self.cell_size + self.menu_height
        self.window_width = self.dimensions * self.cell_size
        # COLORS
        self.WHITE = (255, 255, 255)
        self.GRAY = (192, 192, 192)
        self.BLACK = (0, 0, 0)
        self.DARK_GRAY = (60, 60, 60)

        # GETTING THE FIELD
        self.field = None
        self.obtain_a_new_field()

        # INIT
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('SMK: Minesweeper')
        self.font = pygame.font.Font(None, 24)  # INIT THE FOND - AFTER PYGAME ITSELF

        # BUTTON INIT (SIZE and POSITIONS)
        self.menu_button = pygame.Rect(10, 5, 100, 30)
        self.another_button = pygame.Rect(120, 5, 130, 30)

        self.game_loop(self.screen)

    def game_loop(self, screen):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos
                    if y < self.menu_height:  # CLICKED the MENU
                        self.menu_button_clicks(event.pos)
                    else:
                        field_x, field_y = x // self.cell_size, (y-self.menu_height) // self.cell_size
                        print(f"Clicked: {field_x}, {field_y}")
                        if self.check_if_we_click_on_a_bomb(field_x, field_y):
                            print('BOOOOM!')

            screen.fill(self.WHITE)
            self.draw_menu(screen)
            self.draw_the_field(screen)
            pygame.display.flip()  # this updates the window as I see. Nothing works w/o it.

    def draw_the_field(self, screen):
        for y in range(self.dimensions):
            for x in range(self.dimensions):
                rect_y = y * self.cell_size + self.menu_height
                rect = pygame.Rect(x * self.cell_size, rect_y, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, self.GRAY, rect, 1)
                each_cell = self.field[y][x]

                cell_text = each_cell.string if each_cell.if_bomb else each_cell.bombs_around \
                    if each_cell.bombs_around > 0 else ""

                text = self.font.render(str(cell_text), True, self.BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

    def obtain_a_new_field(self):
        self.field = Field(max_bombs=self.max_bombs, dimensions=self.dimensions).get()

    def draw_menu(self, screen):
        # Draw the menu background
        pygame.draw.rect(screen, self.DARK_GRAY, [0, 0, self.window_width, self.menu_height])

        # Draw the "New Game" button
        button_rect = self.menu_button
        pygame.draw.rect(screen, self.GRAY, button_rect)

        # Add text to the button
        font = pygame.font.Font(None, 24)
        text = font.render("New Game", True, self.BLACK)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

        # Draw the Another button
        button_rect = self.another_button
        pygame.draw.rect(screen, self.GRAY, button_rect)

        # Add text to the button
        font = pygame.font.Font(None, 24)
        text = font.render("Another button", True, self.BLACK)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

        # Add other text, e.g., number of mines
        #mine_text = f"Mines: asdasd"
        #mine_surf = font.render(mine_text, True, self.WHITE)
        #screen.blit(mine_surf, (120, 10))

    def check_if_we_click_on_a_bomb(self, x, y):
        if self.field[y][x].if_bomb:
            return True
        else:
            return False

    def menu_button_clicks(self, pos):
        if self.menu_button.collidepoint(pos):
            print('Clicked New Game')
            self.obtain_a_new_field()
        elif self.another_button.collidepoint(pos):
            print('Another button')
        else:
            print('Missed all buttons')


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
            self.string = '*B*'

        def __str__(self):
            return self.string if self.if_bomb else str(self.bombs_around)

        def __repr__(self):
            return self.string if self.if_bomb else str(self.bombs_around)


def main():
    dim = 10
    bombs = 15
    Game(max_bombs=bombs, dimensions=dim)


if __name__ == "__main__":
    main()
