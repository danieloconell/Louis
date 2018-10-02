from random import randint
from dataclasses import dataclass

import pygame as pg

# get pg ready!
pg.init()


@dataclass
class bird:
    x: int
    y: int
    angle: int
    img: pg.Surface


class Flappy:
    """Flappy environment.

    The aim of this environment is to survive as long as possible without
    hitting a pipe, as I'm sure you know. This environment is rendered using
    pg."""

    ACTIONS = ["up", "stay"]

    # colours
    C_SKY = (66, 188, 244)
    C_RED = (96, 148, 188)
    C_GREEN = (58, 193, 46)

    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 1024 * SCREEN_WIDTH // 768
    PIPE_DIFF = 240 * SCREEN_WIDTH // 768
    BLOCK = SCREEN_WIDTH // 20

    def __init__(self):
        # to init pg
        self.pg_init = True
        self.clock = pg.time.Clock()
        pg.display.set_caption("Flappy")
        self.display = pg.display.set_mode(
            [self.SCREEN_WIDTH, self.SCREEN_HEIGHT + 106]
        )

        self.bird = bird(
            self.BLOCK * 4,
            self.SCREEN_HEIGHT // 2,
            0,
            pg.transform.scale(
                pg.image.load("assets/bird.gif").convert_alpha(), (75, 53)
            )
        )

    def scale(self, pixels):
        """Scale an amount of pixels based on the display's size.

        Args:
            pixels (int): Dimension of object to be scaled.

        Returns:
            Scaled dimension.
        """
        return pixels * self.SCREEN_WIDTH // 768

    def rotate(self, image, angle):
        """Rotate image by n degrees.

        Args:
            surface (pg.Surface): The surface that is to be rotated.
            angle (int): Amount for image to be rotated
        """
        rotated_image = pg.transform.rotate(image, -angle)
        return rotated_image

    def reset(self):
        """Reset all the necessary variables for the environment."""
        # reset vars
        self.done = False
        self.bird.y = self.SCREEN_HEIGHT // 2
        self.bird.angle = 0
        self.gravity = 0.85
        self.velocity = 0

        # reset pipes between
        self.pipes_loc = [[self.SCREEN_WIDTH, randint(330, 721)]]

        # reset ground
        self.ground_loc = 1

    def update(self):
        """Bring pipes and ground forward, add new pipe if nevessary, remove
        pipe and ground if off screen, update gravity and bird position, limit
        velocity and stop game if bird at top or bottom."""

        # move pipes forward
        for pipe in self.pipes_loc:
            pipe[0] -= 4

        # if pipe halfway or more and only one pipe add new pipe
        if len(self.pipes_loc) < 2 and self.pipes_loc[0][0] <= self.SCREEN_WIDTH / 2:
            self.pipes_loc.append(
                [self.pipes_loc[0][0] + self.SCREEN_WIDTH // 2 + 116, randint(330, 721)]
            )

        # remove first pipe if off screen
        if self.pipes_loc[0][0] <= -116:
            del self.pipes_loc[0]

        # move ground forward
        self.ground_loc -= 4

        # remove ground if off screen and add new ground
        if self.ground_loc <= -37:
            self.ground_loc = 1

        # limit bird rotation
        if self.bird.angle <= -90 or self.bird.angle >= 90:
            self.bird.angle = 90

        # update velocity and bird position
        self.velocity += self.gravity
        self.bird.y += int(self.velocity)

        # limit velocity to reduce drastic movement
        if self.velocity > 16:
            self.velocity = 16
        elif self.velocity < -16:
            self.velocity = -16

    def render(self):
        """Render everything that needs to be seen."""
        # setup pg on first run
        if self.pg_init:
            # set window width and height
            # load and scale bird
            # load and scale background
            self.bg_img = pg.transform.scale(
                pg.image.load("assets/background.gif").convert(),
                (self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            )
            # load and scale top pipe
            self.pipe_top_img = pg.transform.scale(
                pg.image.load("assets/pipe-top.gif").convert_alpha(), (116, 523)
            )
            # load and scale bottom pipe
            self.pipe_bottom_img = pg.transform.scale(
                pg.image.load("assets/pipe-bottom.gif").convert_alpha(), (116, 523)
            )
            # load and scale ground
            self.ground_img = pg.transform.scale(
                pg.image.load("assets/ground.gif").convert_alpha(),
                (self.SCREEN_WIDTH + 30, 106),
            )
            self.pg_init = False

        # draw background
        self.display.blit(self.bg_img, (0, 0))

        # pipes
        for pipe in self.pipes_loc:
            # bottom pipe
            self.display.blit(self.pipe_bottom_img, (pipe[0], pipe[1]))
            # top pipe
            self.display.blit(
                self.pipe_top_img, (pipe[0], pipe[1] - self.PIPE_DIFF - 523)
            )

        # ground
        # self.display.blit(self.ground_img, (self.ground_loc, self.SCREEN_HEIGHT))

        # rotate bird
        rotated_bird = self.rotate(self.bird.img, self.bird.angle)
        # create rectange from the bird
        rotated_bird_rect = rotated_bird.get_rect(center=(self.bird.x, self.bird.y))

        # create masks to check for collision
        bird_mask = pg.mask.from_surface(rotated_bird)
        pipe_top_mask = pg.mask.from_surface(self.pipe_top_img)
        pipe_bottom_mask = pg.mask.from_surface(self.pipe_bottom_img)

        x_diff = rotated_bird_rect.x - self.pipes_loc[0][0]
        top_y_diff = rotated_bird_rect.y - self.pipes_loc[0][1] + self.PIPE_DIFF + 523
        bot_y_diff = rotated_bird_rect.y - self.pipes_loc[0][1]

        overlap_top = pipe_top_mask.overlap(bird_mask, (x_diff, top_y_diff))
        overlap_bottom = pipe_bottom_mask.overlap(bird_mask, (x_diff, bot_y_diff))

        # if there is a collision or bird at top or bottom of screen, gameover
        if overlap_top or overlap_bottom:
            self.done = True
        elif rotated_bird_rect.y >= self.SCREEN_HEIGHT - 50:
            self.done = True
        elif (
            rotated_bird_rect.topright[0] >= self.pipes_loc[0][0]
            and rotated_bird_rect.y <= 0
        ):
            self.done = True
        else:
            self.display.blit(rotated_bird, rotated_bird_rect)
            pg.display.update()

    def make_action(self, action):
        """Move bird."""
        if action == "up":
            self.bird.angle = -35
            self.velocity += -20
        elif action == "stay":
            self.bird.angle += 2

        self.update()

        self.clock.tick(60)

    def get_screen(self):
        """Return the game display as an image."""
        return pg.surfarray.array3d(pg.display.get_surface())
