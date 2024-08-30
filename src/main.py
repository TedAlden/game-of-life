from conway import Conway
from settings import *

import pygame
import pathlib


class Game:

    def __init__(self, rows, cols, cellsize):      
        pygame.init()
        pygame.display.set_caption("Conway's Game of Life")
        self.screen_size = (cols * cellsize, rows * cellsize)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.conway = None
        self.rows = rows
        self.cols = cols
        self.cellsize = cellsize
        self.running = True

    def new(self):
        self.conway = Conway(self.rows, self.cols)
        self.conway.load_from_csv(pathlib.Path(__file__).parent.joinpath("example.csv").resolve())

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # 'Space' pauses the game
                if event.key == pygame.K_SPACE:
                    self.conway.running = not self.conway.running
                # 'R' key resets the game
                if event.key == pygame.K_r:
                    self.new()
                # 'Esc' exits the game
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        pressed = pygame.mouse.get_pressed()
        x, y = pygame.mouse.get_pos()
        # Left mouse click places an alive cell
        if pressed[0]:
            self.conway.data[y // self.cellsize][x // self.cellsize] = 1
        # Right mouse click removes an alive cell
        elif pressed[2]:
            self.conway.data[y // self.cellsize][x // self.cellsize] = 0

    def update(self):
        if self.conway.running:
            self.conway.next_generation()
        self.clock.tick(FPS)

    def draw(self):
        # Draw background
        self.screen.fill(WIN_COLOUR_BACKGROUND)
        # Draw grid and cells
        data = self.conway.get_generation()
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                # Draw cells
                if cell == 1:
                    pygame.draw.rect(self.screen,
                                     CELL_COLOUR_ALIVE_NEXT,
                                     (x * self.cellsize,
                                      y * self.cellsize,
                                      self.cellsize,
                                      self.cellsize))
                # Draw dying cells
                elif cell == 2:
                    # TODO

                    pass
                # Draw gridlines
                start1 = (x * self.cellsize, 0)
                finish1 = (x * self.cellsize, y * self.cellsize * self.rows)
                start2 = (0, y * self.cellsize)
                finish2 = (x * self.cellsize * self.cols, y * self.cellsize)
                pygame.draw.line(self.screen, WIN_COLOUR_GRID, start1, finish1)
                pygame.draw.line(self.screen, WIN_COLOUR_GRID, start2, finish2)

        pygame.display.set_caption(f"Game of life - Generation {self.conway.generation}")
        pygame.display.flip()


if __name__ == "__main__":
    game = Game(50, 75, 10)
    game.new()
    while game.running:
        game.events()
        game.update()
        game.draw()
