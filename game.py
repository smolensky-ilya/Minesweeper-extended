import random

import pygame
from classes import Field


class Game:
    def __init__(self, bombs_perc: float, dimensions: int, cell_size_pix: int = 50):
        # PARAMS
        self.cell_size = cell_size_pix
        self.menu_height = 40

        self.dimensions = dimensions
        self.max_bombs = int(self.dimensions * self.dimensions * bombs_perc)

        self.window_height = self.dimensions * self.cell_size + self.menu_height
        self.window_width = self.dimensions * self.cell_size
        # COLORS
        self.WHITE = (255, 255, 255)
        self.GRAY = (192, 192, 192)
        self.BLACK = (0, 0, 0)
        self.DARK_GRAY = (60, 60, 60)

        # GAME FEATURES
        self.player_inventory, self.player_immortality = self.initiate_game_features()
        #self.possible_inventory_items = {'Im': 0.01, 'Rn': 0.01}  # {item_name: probability}
        self.possible_inventory_items = {'Im': ((self.dimensions * self.dimensions) - self.max_bombs) / 200 / 100,
                                         'Rn': ((self.dimensions * self.dimensions) - self.max_bombs) / 100 / 100}  # {item_name: probability}

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
        self.inventory_buttons = {}
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

    def draw_menu(self, screen, menu_text):
        # Draw the menu background
        pygame.draw.rect(screen, self.DARK_GRAY, [0, 0, self.window_width, self.menu_height])

        # Draw the "New Game" button
        button_rect = self.menu_button
        pygame.draw.rect(screen, self.GRAY, button_rect)

        # Add text to the button
        text = self.font.render("New Game", True, self.BLACK)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

        # Draw the Another button
        button_rect = self.another_button
        pygame.draw.rect(screen, self.GRAY, button_rect)

        # Add text to the button
        text = self.font.render("Another button", True, self.BLACK)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

        # Add other text, e.g., number of mines
        mine_surf = self.font.render(menu_text, True, self.WHITE)
        screen.blit(mine_surf, (260, 12))

        # DRAWING INVENTORY ITEMS!!!!!!!
        y_coord = 520
        for item, quantity in self.player_inventory.items():
            item_string = str(item) + f" x {str(quantity)}"
            #adding their coords to the dict for functional reference in another func
            self.inventory_buttons[item] = pygame.Rect(y_coord, 10, len(item_string) * 9, 20)
            pygame.draw.rect(screen, self.GRAY, self.inventory_buttons[item])
            text = self.font.render(item_string, True, self.BLACK)
            text_rect = text.get_rect(center=self.inventory_buttons[item].center)
            screen.blit(text, text_rect)
            y_coord += (len(item) * 8) + 50

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
            self.obtain_a_new_field()
            self.change_menu_text()
            self.initiate_game_features()
        elif self.another_button.collidepoint(pos):
            print('Another button')
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
            all_hidden_bombs = []
            for row in self.field:
                for tile in row:
                    if tile.if_bomb and not tile.if_open and not tile.is_flagged:
                        all_hidden_bombs.append(tile)
            if len(all_hidden_bombs) > 0:
                random.choice(all_hidden_bombs).if_open = True
                return True
            else:
                return False

        else:
            print('Wrong item')

    def game_over(self):
        self.field_object.open_all_tiles()
        self.change_menu_text(lost=True)


def main():
    dim = 38
    Game(bombs_perc=0.05, dimensions=dim, cell_size_pix=25)


if __name__ == "__main__":
    main()
