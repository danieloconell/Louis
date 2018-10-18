from random import random, choice
from contextlib import contextmanager

import pygame as pg

pg.init()


class Tiles:

    TILE_COLOURS = {
        2: (238, 228, 218),
        4: (237, 224, 200),
        8: (242, 177, 120),
        16: (245, 149, 99),
        32: (246, 124, 94),
        64: (246, 93, 60),
        128: (237, 207, 114),
        256: (237, 204, 96),
        512: (237, 201, 80),
        1024: (237, 197, 63),
        2048: (237, 194, 46),
    }
    MAX_COLOUR = (60, 58, 50)

    ACTIONS = ["left", "right", "up", "down"]

    large_font = pg.font.SysFont(None, 72)
    regular_font = pg.font.SysFont(None, 64)
    small_font = pg.font.SysFont(None, 50)
    clock = pg.time.Clock()

    class board:
        def __init__(self, size=4):
            self.size = size
            self.flipped = False
            self.reset()

        def reset(self):
            self.tiles = [[None] * self.size for row in range(self.size)]
            self.add_tiles(2)

        def flip(self):
            self.flipped = not self.flipped

            for row in self.tiles:
                row.reverse()

        def add_tiles(self, num_tiles):
            if self.full:
                return

            for _ in range(num_tiles):
                row_i, tile_i = int(random() * self.size), int(random() * self.size)
                while self.tiles[row_i][tile_i] is not None:
                    row_i, tile_i = int(random() * self.size), int(random() * self.size)
                self.tiles[row_i][tile_i] = 2 if random() < 0.9 else 4

        @property
        def full(self):
            if len(self) == self.size ** 2:
                for row_i, row in enumerate(self.tiles):
                    for tile_i, tile in enumerate(row):
                        if tile:
                            if tile_i > 0 and tile == row[tile_i - 1]:
                                return False
                            elif tile_i != self.size - 1 and tile == row[tile_i + 1]:
                                return False
                            elif row_i != 0 and tile == self.tiles[row_i - 1][tile_i]:
                                return False
                            elif (
                                row_i != self.size - 1
                                and tile == self.tiles[row_i + 1][tile_i]
                            ):
                                return False
                return True

        def __getitem__(self, row_index, tile_index=None):
            if tile_index:
                return self.tiles[row_index][tile_index]
            return self.tiles[row_index]

        def __setitem__(self, row_key, value, tile_key=None):
            if tile_key:
                self.tiles[row_key][tile_key] = value
            self.tiles[row_key] = value

        def __iter__(self):
            for tile in self.tiles:
                yield tile

        def __len__(self):
            return len([tile for row in self.tiles for tile in row if tile])

    def __init__(self, size=4):
        self.tiles = self.board(size=size)
        self.memory = self.board(size=size)
        self.tiles.last_move = [row.copy() for row in self.tiles.tiles]
        self.pg_init = True
        self.is_sim = False

    def slide(self, row, left=None, right=None):
        non_zero = [tile for tile in row if tile]
        missing = [None] * (self.tiles.size - len(non_zero))

        return non_zero + missing if left else missing + non_zero

    def merge(self, row):
        for tile_i, tile in enumerate(row):
            if tile and tile_i is not 0 and tile == row[tile_i - 1]:
                row[tile_i] = None
                row[tile_i - 1] = tile * 2
                if self.is_sim:
                    self.sim_score += tile * 2
                else:
                    self.score += tile * 2
        return row

    def move(self, row, left=None, right=None):
        """Wrapper for the slide and merge function for convenience.
        Args:
            row"""
        if left:
            return self.slide(self.merge(self.slide(row, left=True)), left=True)
        elif right:
            return self.slide(self.merge(self.slide(row, right=True)), right=True)

    @contextmanager
    def simulate(self):
        self.is_sim = True
        yield
        self.is_sim = False

    def render(self):
        """Render everything that needs to be seen."""
        if self.pg_init:
            pg.display.set_caption("2048")
            width = height = self.tiles.size * 100 + (self.tiles.size + 1) * 15
            self.display = pg.display.set_mode((width, height))
            self.display.fill((188, 172, 160))
            self.pg_init = False

        for row_i, row in enumerate(self.tiles):
            for tile_i, tile in enumerate(row):
                if tile:
                    pg.draw.rect(
                        self.display,
                        self.TILE_COLOURS.get(tile, self.MAX_COLOUR),
                        (115 * tile_i + 15, 115 * row_i + 15, 100, 100),
                    )

                    font_colour = (249, 246, 242) if tile > 4 else (117, 110, 101)
                    font = self.small_font if tile > 512 else self.regular_font
                    font = self.large_font if tile < 64 else self.regular_font

                    tile_num = font.render(str(tile), True, font_colour)
                    num_rect = tile_num.get_rect(
                        center=(115 * tile_i + 65, 115 * row_i + 65)
                    )
                    self.display.blit(tile_num, num_rect)
                else:
                    pg.draw.rect(
                        self.display,
                        (205, 192, 180),
                        (115 * tile_i + 15, 115 * row_i + 15, 100, 100),
                    )

        pg.display.update()

    def possible(self, action):
        if self.is_sim:
            tiles = self.memory
        else:
            tiles = self.tiles

        if tiles.full:
            if self.is_sim:
                self.sim_done = True
            return False

        initial_tiles = [row.copy() for row in tiles]
        self.make_action(action)
        if tiles.tiles == initial_tiles:
            tiles.tiles = initial_tiles
            return False
        else:
            tiles.tiles = initial_tiles
            return True

    def random_action(self):
        # actions = [action for action in self.ACTIONS if self.possible(action)]
        actions = self.ACTIONS
        if len(actions) is 0:
            return
        self.make_action(choice(actions))

    def make_action(self, action):
        """Move agent or human player and update falling square.

        Args:
            action (str): one of the items from the ACTIONS list.
        """
        if self.is_sim:
            tiles = self.memory
        else:
            tiles = self.tiles

        if tiles.full and self.is_sim:
            self.sim_done = True
            return

        elif tiles.full:
            self.done = True
            return

        self.prev_state = [row.copy() for row in tiles.tiles]

        if action == "up":
            for row_i in range(self.tiles.size):
                row = self.move([row[row_i] for row in tiles], left=True)
                for tile_i in range(self.tiles.size):
                    tiles[tile_i][row_i] = row[tile_i]
        elif action == "down":
            for row_i in range(self.tiles.size):
                row = self.move([row[row_i] for row in tiles], right=True)
                for tile_i in range(self.tiles.size):
                    tiles[tile_i][row_i] = row[tile_i]
        elif action == "left":
            for row_i, row in enumerate(tiles):
                tiles[row_i] = self.move(row, left=True)
        elif action == "right":
            for row_i, row in enumerate(tiles):
                tiles[row_i] = self.move(row, right=True)

        if tiles.tiles != self.prev_state:
            tiles.add_tiles(1)

    def reset(self):
        """Reset all the necessary variables for the environment."""
        if self.is_sim:
            self.sim_done = False
            self.sim_score = self.score
            self.memory.tiles = [row.copy() for row in self.tiles.tiles]
        else:
            self.tiles.reset()
            self.done = False
            self.score = 0
