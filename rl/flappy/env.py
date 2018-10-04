from random import randint
from dataclasses import dataclass

import pygame as pg

# get pygame ready!
pg.init()


class Flappy:
    """Flappy environment.

    The aim of this environment is to survive as long as possible without
    hitting a pipe, as I'm sure you know."""

    ACTIONS = ["up", "stay"]

    FPS = 60
    WIN_WIDTH = 640
    WIN_HEIGHT = 959

    if pg.display.Info().current_w < 3000:
        WIN_WIDTH //= 2
        WIN_HEIGHT //= 2
        INIT_GRAVITY = 0.76
        VELOCTY_STEP = 16
    GROUND_HEIGHT = WIN_WIDTH // 64 * 11
    BACKGROUND_HEIGHT = WIN_HEIGHT - GROUND_HEIGHT

    PIPE_DIFF = WIN_WIDTH // 64 * 20
    PIPE_HEIGHT = WIN_WIDTH // 160 * 131
    PIPE_WIDTH = WIN_WIDTH // 160 * 29
    PIPE_OVERFLOW = PIPE_HEIGHT * 2 + PIPE_DIFF - BACKGROUND_HEIGHT

    UPWARDS_BIRD_ANGLE = -35
    MAX_BIRD_ANGLE = 90
    ANGLE_STEP = 2.5
    INIT_BIRD_ANGLE = 0
    MAX_VELOCTY = -12
    VELOCTY_STEP = 20
    INIT_VELOCITY = 0
    PIPE_STEP = 4
    INIT_GRAVITY = 0.84

    def __init__(self):
        # use smaller images for smaller screens
        if pg.display.Info().current_w < 3000:
            self.display = pg.display.set_mode([self.WIN_WIDTH, self.WIN_HEIGHT])
            self.bg_img = pg.image.load("assets/background.small.gif").convert()
            self.bird_img = pg.image.load("assets/bird.small.gif").convert_alpha()
            self.top_pipe_img = pg.image.load("assets/pipe-top.small.gif").convert_alpha()
            self.bot_pipe_img = pg.image.load("assets/pipe-bot.small.gif").convert_alpha()
            self.ground_img = pg.image.load("assets/ground.small.gif").convert()
        else:
            self.display = pg.display.set_mode([self.WIN_WIDTH, self.WIN_HEIGHT])
            self.bg_img = pg.image.load("assets/background.gif").convert()
            self.bird_img = pg.image.load("assets/bird.gif").convert_alpha()
            self.top_pipe_img = pg.image.load("assets/pipe-top.gif").convert_alpha()
            self.bot_pipe_img = pg.image.load("assets/pipe-bot.gif").convert_alpha()
            self.ground_img = pg.image.load("assets/ground.gif").convert()

        pg.display.set_caption("Flappy")

        self.pipe_top_mask = pg.mask.from_surface(self.top_pipe_img)
        self.pipe_bot_mask = pg.mask.from_surface(self.bot_pipe_img)

        self.clock = pg.time.Clock()
        self.bird = bird()
        self.ground_loc = 0

    def reset(self):
        """Reset all the necessary variables for the environment."""
        self.done = False
        self.bird.y = self.BACKGROUND_HEIGHT // 2
        self.bird.angle = self.INIT_BIRD_ANGLE
        self.gravity = self.INIT_GRAVITY
        self.velocity = self.INIT_GRAVITY

        # reset pipes between
        rand_y = randint(0, self.PIPE_OVERFLOW)
        self.pipes = [
            (pipe(-rand_y), pipe(-rand_y + self.PIPE_HEIGHT + self.PIPE_DIFF))
        ]

    def update(self):
        """Bring pipes and ground forward, add new pipe if nevessary, remove
        pipe and ground if off screen, update gravity and bird position, limit
        velocity and stop game if bird at top or bottom."""

        # move pipes forward
        for top_pipe, bot_pipe in self.pipes:
            top_pipe.x -= self.PIPE_STEP
            bot_pipe.x -= self.PIPE_STEP

        # if pipe halfway or more and only one pipe add new pipe
        if self.pipes[-1][0].x <= self.WIN_WIDTH / 2:
            rand_y = randint(0, self.PIPE_OVERFLOW)
            self.pipes.append(
                (pipe(-rand_y), pipe(-rand_y + self.PIPE_HEIGHT + self.PIPE_DIFF))
            )

        if self.ground_loc <= -32:
            self.ground_loc = 0
        else:
            self.ground_loc -= 4

        # remove first pipe if off screen
        if self.pipes[0][0].x <= -self.PIPE_WIDTH:
            del self.pipes[0]

        # update velocity and bird position
        self.velocity += self.gravity
        self.bird.y += int(self.velocity)

        # limit bird angle
        if self.bird.angle > self.MAX_BIRD_ANGLE:
            self.bird.angle = self.MAX_BIRD_ANGLE

        # limit velocity
        if self.velocity < self.MAX_VELOCTY:
            self.velocity = self.MAX_VELOCTY

    def render(self):
        """Render everything that needs to be seen."""
        # draw background
        self.display.blit(self.bg_img, (0, 0))

        # pipes
        for top_pipe, bot_pipe in self.pipes:
            self.display.blit(self.top_pipe_img, (top_pipe.x, top_pipe.y))
            self.display.blit(self.bot_pipe_img, (bot_pipe.x, bot_pipe.y))

        # rotate bird
        rotated_bird = pg.transform.rotate(self.bird_img, -self.bird.angle)
        # create rectange from the bird
        rotated_bird_rect = rotated_bird.get_rect(center=(self.bird.x, self.bird.y))

        # create mask to check for collision between bird and pipes
        bird_mask = pg.mask.from_surface(rotated_bird)

        x_diff = rotated_bird_rect.x - self.pipes[0][0].x
        top_y_diff = rotated_bird_rect.y - self.pipes[0][1].y
        bot_y_diff = rotated_bird_rect.y - self.pipes[0][0].y

        overlap_top = self.pipe_top_mask.overlap(bird_mask, (x_diff, top_y_diff))
        overlap_bot = self.pipe_bot_mask.overlap(bird_mask, (x_diff, bot_y_diff))
        overlap_bot = overlap_top = None

        # if there is a collision or bird at top or bottom of screen, gameover
        # otherwise render frame
        if overlap_top or overlap_bot:
            self.done = True
        elif rotated_bird_rect.bottomright[1] >= self.BACKGROUND_HEIGHT:
            self.done = True
        elif (
            rotated_bird_rect.topright[0] >= self.pipes[0][0].x
            and rotated_bird_rect.y <= 0
        ):
            self.done = True
        else:
            self.display.blit(rotated_bird, rotated_bird_rect)
            self.display.blit(self.ground_img, (self.ground_loc, self.BACKGROUND_HEIGHT))
            pg.display.update()

    def make_action(self, action):
        """Move bird."""
        if action == "up":
            self.bird.angle = self.UPWARDS_BIRD_ANGLE
            self.velocity -= self.VELOCTY_STEP
        elif action == "stay":
            self.bird.angle += self.ANGLE_STEP

        self.update()

        self.clock.tick(self.FPS)


@dataclass
class pipe:
    y: int
    x: int = Flappy.WIN_WIDTH


@dataclass
class bird:
    x: int = Flappy.WIN_WIDTH * 0.2
    y: int = Flappy.BACKGROUND_HEIGHT // 2
    angle: int = 0
