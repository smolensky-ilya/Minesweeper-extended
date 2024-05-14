import random
import pygame
from time import sleep


class Game:
    def __init__(self, max_bombs, dimensions, cell_size_pix=50):
        # PARAMS
        self.cell_size = cell_size_pix
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
        self.field_object = None
        self.field = None
        self.obtain_a_new_field()

        # INIT
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('SMK: Minesweeper')
        self.font = pygame.font.Font(None, 24)  # INIT THE FOND - AFTER PYGAME ITSELF
        self.first_click = True
        self.menu_text = self.change_menu_text()

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
                        if event.button == 1:  # LEFT MOUSE BUTTON
                            #print(f"Clicked: {field_x}, {field_y}")

                            # Saving ourselves on the first click - it will recreate the field until safe.
                            while self.first_click and self.field[field_y][field_x].if_bomb:
                                #print('FIRST CLICK - RECREATING')
                                self.obtain_a_new_field()
                            self.first_click = False  # It's no longer the first click!
                            if not self.field[field_y][field_x].is_flagged:  # If not flagged - OPEN
                                self.field_object.open_tile(x=field_x, y=field_y, draw_object=self.draw_the_field,
                                                            screen=screen)
                            if self.check_if_we_click_on_a_bomb(field_x, field_y):
                                self.game_over()
                            else:
                                self.change_menu_text()  # updating the number of remaining tiles to open
                            self.first_click = False
                        elif event.button == 3:  # RIGHT MOUSE BUTTON
                            #print('RMB')
                            self.field[field_y][field_x].get_flagged()
                if self.field_object.count_remaining_tiles() <= 0:  # checking the winning condition
                    self.change_menu_text(won=True)
            screen.fill(self.WHITE)
            self.draw_menu(screen, menu_text=self.menu_text)
            self.draw_the_field(screen)
            pygame.display.flip()  # this updates the window as I see. Nothing works w/o it.

    def draw_the_field(self, screen):
        for y in range(self.dimensions):
            for x in range(self.dimensions):
                rect_y = y * self.cell_size + self.menu_height
                rect = pygame.Rect(x * self.cell_size, rect_y, self.cell_size, self.cell_size)

                each_cell = self.field[y][x]
                if each_cell.if_open:
                    if each_cell.if_bomb:
                        background_color = 'red'
                    else:
                        background_color = self.WHITE

                    pygame.draw.rect(screen, background_color, rect)  # Fill the cell with the background color
                    cell_text = each_cell.string if each_cell.if_bomb else each_cell.bombs_around \
                        if each_cell.bombs_around > 0 else ""
                else:
                    # Closed cells are dark gray
                    pygame.draw.rect(screen, self.GRAY, rect)
                    cell_text = '' if not each_cell.is_flagged else '*'

                # Draw a black border for all cells
                pygame.draw.rect(screen, self.BLACK, rect, 1)  # 1 pixel border

                # Render the text for each cell
                if cell_text != '':  # Only render text if there's something to display
                    text = self.font.render(str(cell_text), True, self.BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

    def obtain_a_new_field(self):
        self.field_object = Field(max_bombs=self.max_bombs, dimensions=self.dimensions)
        self.field = self.field_object.get()
        self.first_click = True

    def draw_menu(self, screen, menu_text):
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
        mine_surf = font.render(menu_text, True, self.WHITE)
        screen.blit(mine_surf, (260, 12))

    def change_menu_text(self, won=False, lost=False):
        if won:
            self.menu_text = f"Amazing job!"
        elif lost:
            self.menu_text = f"Better luck next time! :("
        else:
            self.menu_text = f"Good luck! Mines: {self.max_bombs}. Left: {self.field_object.count_remaining_tiles()}"

        return self.menu_text

    def check_if_we_click_on_a_bomb(self, x, y):
        if self.field[y][x].if_bomb:
            return True
        else:
            return False

    def menu_button_clicks(self, pos):
        if self.menu_button.collidepoint(pos):
            print('Clicked New Game')
            self.obtain_a_new_field()
            self.change_menu_text()
        elif self.another_button.collidepoint(pos):
            print('Another button')
        else:
            print('Missed all buttons')

    def game_over(self):
        self.field_object.open_all_tiles()
        self.change_menu_text(lost=True)


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
        if tile.if_open or tile.if_bomb:
            return
        tile.open_tile()

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


def main():
    dim = 20
    bombs = 50
    Game(max_bombs=bombs, dimensions=dim, cell_size_pix=25)


if __name__ == "__main__":
    main()
