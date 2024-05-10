import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 20
GRID_SIZE = 10
NUM_MINES = 15
WIDTH = HEIGHT = CELL_SIZE * GRID_SIZE

# Colors
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

grid = [[random.choice([0, 1, 'B']) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

print(grid)


def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)
            cell = grid[y][x]
            if isinstance(cell, int) and cell > 0:
                text = font.render(str(cell), True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)


font = pygame.font.Font(None, 24)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
            print(f"Clicked on {grid_x}, {grid_y}")

    screen.fill(WHITE)
    draw_grid()
    pygame.display.flip()

pygame.quit()
sys.exit()
