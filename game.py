import random
import sys
import pygame
from classes import Field


class Game:
    def __init__(self, bombs_perc: float, dimensions: int, cell_size_pix: int = 50):
        # PARAMS
        self.cell_size: int = cell_size_pix
        self.menu_height: int = 40

        self.dimensions: int = dimensions
        self.chosen_bomb_perc: float = bombs_perc
        self.max_bombs: int = int(self.dimensions * self.dimensions * self.chosen_bomb_perc)

        self.window_height: int = self.dimensions * self.cell_size + self.menu_height
        self.window_width: int = self.dimensions * self.cell_size
        # COLORS
        self.WHITE: tuple = (255, 255, 255)
        self.GRAY: tuple = (192, 192, 192)
        self.BLACK: tuple = (0, 0, 0)
        self.DARK_GRAY: tuple = (60, 60, 60)

        # GAME FEATURES
        self.player_inventory, self.player_immortality = self.initiate_game_features()
        # {item_name: probability}
        self.possible_inventory_items: dict = {'Im': bombs_perc / 5,
                                               'Rn': bombs_perc * 2}
        # GETTING THE FIELD
        self.field_object = None
        self.field = None
        self.obtain_a_new_field()

        # INIT
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('SMK: Minesweeper')
        self.font = pygame.font.Font(None, 24)  # INIT THE FOND - AFTER PYGAME ITSELF
        self.first_click: bool = True
        self.menu_text = self.change_menu_text()

        # BUTTON INIT (SIZE and POSITIONS)
        self.menu_button = pygame.Rect(10, 5, 100, 30)
        self.another_button = pygame.Rect(120, 5, 130, 30)
        self.inventory_buttons: dict = {}
        self.game_loop(self.screen)

    def initiate_game_features(self):
        self.player_immortality = False
        self.player_inventory = {}  # {item: quantity}
        return self.player_inventory, self.player_immortality

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
                            if self.field[field_y][field_x].if_open:  # IF THE TILE IS ALREADY OPEN
                                if self.field[field_y][field_x].item is not None:  # checking if there is an item
                                    if self.field[field_y][field_x].item not in self.player_inventory.keys():
                                        self.player_inventory[self.field[field_y][field_x].item] = 1
                                    else:
                                        self.player_inventory[self.field[field_y][field_x].item] += 1
                                    self.field[field_y][field_x].item_taken = True
                            else:
                                # Saving ourselves on the first click - it will recreate the field until safe.
                                while self.first_click and self.field[field_y][field_x].if_bomb:
                                    self.obtain_a_new_field()
                                self.first_click = False  # It's no longer the first click!
                                if not self.field[field_y][field_x].is_flagged:  # If not flagged - OPEN
                                    self.field_object.open_tile(x=field_x, y=field_y, draw_object=self.draw_the_field,
                                                                screen=screen)
                                    if self.check_if_we_click_on_a_bomb(field_x, field_y):
                                        if self.player_immortality:  # Handing immortality logic
                                            self.player_immortality = False
                                            self.field_object.open_tile(x=field_x, y=field_y,
                                                                        draw_object=self.draw_the_field, screen=screen)
                                        else:
                                            self.game_over()

                                    else:
                                        self.change_menu_text()  # updating the number of remaining tiles to open
                                self.first_click = False
                        elif event.button == 3:  # RIGHT MOUSE BUTTON
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
                    cell_text = each_cell.bomb_string if each_cell.if_bomb else each_cell.bombs_around \
                        if each_cell.bombs_around > 0 else each_cell.item if each_cell.item is \
                        not None and not each_cell.item_taken else ''
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
        self.field_object = Field(max_bombs=self.max_bombs, dimensions=self.dimensions,
                                  possible_inventory_items=self.possible_inventory_items)
        self.field = self.field_object.get()
        self.first_click = True

    def draw_menu(self, screen, menu_text: str):
        # Draw the menu background
        pygame.draw.rect(screen, self.DARK_GRAY, [0, 0, self.window_width, self.menu_height])

        # Draw the "New Game" button
        button_rect = self.menu_button
        pygame.draw.rect(screen, self.GRAY, button_rect)

        # Add text to the button
        text = self.font.render("New Game", True, self.BLACK)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

        # Add other text, e.g., number of mines
        mine_surf = self.font.render(menu_text, True, self.WHITE)
        screen.blit(mine_surf, (120, 12))

        # DRAWING INVENTORY ITEMS!!!!!!!
        y_coord = 363
        for item, quantity in self.player_inventory.items():
            item_string = str(item) + f" x {str(quantity)}"
            # adding their coordinates to the dict for functional reference in another func
            self.inventory_buttons[item] = pygame.Rect(y_coord, 10, len(item_string) * 9, 20)
            pygame.draw.rect(screen, self.GRAY, self.inventory_buttons[item])
            text = self.font.render(item_string, True, self.BLACK)
            text_rect = text.get_rect(center=self.inventory_buttons[item].center)
            screen.blit(text, text_rect)
            y_coord += (len(item) * 8) + 50

    def change_menu_text(self, won: bool = False, lost: bool = False):
        if won:
            self.menu_text = f"Amazing job!"
        elif lost:
            self.menu_text = f"Better luck next time! :("
        else:
            self.menu_text = f"Good luck! Mines: {self.max_bombs}. Left: {self.field_object.count_remaining_tiles()}"

        return self.menu_text

    def check_if_we_click_on_a_bomb(self, x: int, y: int):
        if self.field[y][x].if_bomb:
            return True
        else:
            return False

    def menu_button_clicks(self, pos: tuple):
        # checking if inventory was used
        for item, button_rect in self.inventory_buttons.items():
            if button_rect.collidepoint(pos):
                if item in self.player_inventory.keys():
                    if self.use_an_item(item):  # USING IT HERE - True if successful use
                        self.player_inventory[item] -= 1  # reducing the quantity
                        if self.player_inventory[item] <= 0:  # deleting it if 0
                            del self.player_inventory[item]
                        return  # stopping the func
        # other buttons
        if self.menu_button.collidepoint(pos):
            print('Clicked New Game')
            self.open_settings_window()
        else:
            print('Missed all buttons')

    def use_an_item(self, item: str):
        if item == list(self.possible_inventory_items.keys())[0]:  # rule for immortality
            if not self.player_immortality:
                self.player_immortality = True
                return True
            else:
                print('already in use')
                return False

        elif item == list(self.possible_inventory_items.keys())[1]:  # rule for a random bomb
            all_hidden_bombs_with_open_adj_tiles = []
            for ri, row in enumerate(self.field):
                for ti, tile in enumerate(row):
                    if tile.if_bomb and not tile.if_open and not tile.is_flagged:
                        adjacent_tiles = [
                            (ri + i, ti + j)
                            for i in range(-1, 2)
                            for j in range(-1, 2)
                            if 0 <= ri + i < self.dimensions and 0 <= ti + j < self.dimensions and (i != 0 or j != 0)
                        ]
                        if any(self.field[adj_ri][adj_ti].if_open for adj_ri, adj_ti in adjacent_tiles):
                            all_hidden_bombs_with_open_adj_tiles.append(tile)

            if len(all_hidden_bombs_with_open_adj_tiles) > 0:
                random.choice(all_hidden_bombs_with_open_adj_tiles).if_open = True
                return True
            else:
                return False
        else:
            print('Wrong item')

    def game_over(self):
        self.field_object.open_all_tiles()
        self.change_menu_text(lost=True)

    def open_settings_window(self):
        pygame.quit()
        SettingsWindow(dimensions=self.dimensions, bomb_perc=self.chosen_bomb_perc, tile_size=self.cell_size)


class SettingsWindow:
    def __init__(self, dimensions: int = None, bomb_perc: float = None, tile_size: int = None):
        # PARAMS
        self.dimensions_def: int = dimensions if dimensions is not None else 20
        self.bomb_perc_def: float = bomb_perc if bomb_perc is not None else 0.25
        self.tile_size_def: int = tile_size if tile_size is not None else 25

        # UI elements
        self.dimensions_box = None
        self.bombs_perc_box = None
        self.cell_size_pix_box = None
        self.start_button = None

        # INIT
        pygame.init()
        self.window_width = 400
        self.window_height = 300
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('New Game Settings')
        self.font = pygame.font.Font(None, 24)
        self.input_boxes = []
        self.user_input = {}
        self.error_message = ""
        self.init_ui()
        self.run()

    def init_ui(self):
        self.screen.fill((255, 255, 255))

        self.draw_label("Dimensions (5-50):", 50, 50)
        self.dimensions_box = self.create_input_box(200, 50, f"{self.dimensions_def}", "dimensions")

        self.draw_label("Bomb Percentage (0.1-0.9):", 50, 100)
        self.bombs_perc_box = self.create_input_box(200, 100, f"{self.bomb_perc_def}", "bombs_perc")

        self.draw_label("Tile size (px):", 50, 150)
        self.cell_size_pix_box = self.create_input_box(200, 150, f"{self.tile_size_def}", "cell_size_pix")

        self.start_button = pygame.Rect(150, 200, 100, 40)
        pygame.draw.rect(self.screen, (192, 192, 192), self.start_button)

        text = self.font.render("Start Game", True, (0, 0, 0))
        text_rect = text.get_rect(center=self.start_button.center)
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def create_input_box(self, x, y, default_text, key):
        input_box = pygame.Rect(x, y, 140, 32)
        self.input_boxes.append((input_box, default_text, key))
        pygame.draw.rect(self.screen, (192, 192, 192), input_box)
        text_surface = self.font.render(default_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (input_box.x+5, input_box.y+5))
        self.user_input[key] = default_text
        return input_box

    def draw_label(self, text, x, y):
        label = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(label, (x, y))

    def display_error_message(self):
        if self.error_message:
            error_label = self.font.render(self.error_message, True, (255, 0, 0))
            self.screen.blit(error_label, (50, 250))
            pygame.display.flip()

    def validate_input(self):
        try:
            dimensions = int(self.user_input["dimensions"])
            bombs_perc = float(self.user_input["bombs_perc"])
            cell_size_pix = int(self.user_input["cell_size_pix"])

            if dimensions < 5 or dimensions > 50:
                self.error_message = "Dimensions must be between 5 and 50."
                return False
            if bombs_perc < 0.1 or bombs_perc > 0.9:
                self.error_message = "Bomb percentage must be between 0.1 and 0.9."
                return False
            if cell_size_pix < 10 or cell_size_pix > 100:
                self.error_message = "Tile size must be between 10 and 100 px."
                return False
        except ValueError:
            self.error_message = "Please enter valid numbers."
            return False
        return True

    def run(self):
        running = True
        active_box = None
        active_key = None

        while running:
            self.display_error_message()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        if self.validate_input():
                            dimensions = int(self.user_input["dimensions"])
                            bombs_perc = float(self.user_input["bombs_perc"])
                            cell_size_pix = int(self.user_input["cell_size_pix"])
                            running = False
                            self.close()
                            Game(bombs_perc=bombs_perc, dimensions=dimensions, cell_size_pix=cell_size_pix)
                        else:
                            self.screen.fill((255, 255, 255))  # Clear the screen before re-drawing
                            self.init_ui()
                    for box, _, key in self.input_boxes:
                        if box.collidepoint(event.pos):
                            active_box = box
                            active_key = key
                elif event.type == pygame.KEYDOWN and active_box:
                    if event.key == pygame.K_RETURN:
                        active_box = None
                        active_key = None
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_input[active_key] = self.user_input[active_key][:-1]
                    else:
                        self.user_input[active_key] += event.unicode
                    pygame.draw.rect(self.screen, (192, 192, 192), active_box)
                    text_surface = self.font.render(self.user_input[active_key], True, (0, 0, 0))
                    self.screen.blit(text_surface, (active_box.x+5, active_box.y+5))
                    pygame.display.flip()

    @staticmethod
    def close():
        pygame.display.quit()


def main():
    SettingsWindow()


if __name__ == "__main__":
    main()
