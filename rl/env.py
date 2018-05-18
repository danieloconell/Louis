import numpy as np
import pygame as pg

# make results reproducible
np.random.seed(0)

# get pg ready!
pg.init()


class Falling:
    """Falling environment.

    The aim of this environment is to catch a falling square.  The environment
    is rendered using pg. The environment gives information such as:
    object location, player location and that's about it, (very basic).
    """

    ACTIONS = ["left", "right", "stay"]
    BLOCK = pg.display.Info().current_w // 50
    SCREEN_WIDTH = 22
    SCREEN_HEIGHT = 12
    INTERVAL = 1

    def __init__(self, duel=False):
        """Create the environment using pg.

        Args:
            duel: Create duel between ai and human player.
        """

        self.duel = duel
        self.pg_init = True
        pg.display.set_caption("Falling")

    def reset(self):
        """Reset all the necessary variables for the environment."""

        # create object
        self.square = [np.random.randint(1, self.SCREEN_WIDTH + 1), 0]

        # create agent
        self.agent = (self.SCREEN_WIDTH // 2 + 1)

        # create human player
        if self.duel:
            self.human = self.agent

        # reset done
        self.done = False

    def quit(self):
        """Quit the Falling environment."""
        pg.quit()

    def make_action(self, action: str, ai=True, player=False):
        """Move agent or human player and update falling square.

        Args:
            action: Left, right or stay.
            ai: Move agent.
            player: Move player.
        """

        # only update when not in duel mode
        if not self.duel:
            self.update()

        if self.duel and player:
            # if player is at one of the screen borders do not move
            if self.human == self.SCREEN_WIDTH and action == "right":
                pass
            elif self.human == 1 and action == "left":
                pass
            # based on chosen action move human player
            elif action == "left":
                self.old_player = self.human
                self.human -= self.INTERVAL
            elif action == "right":
                self.old_player = self.human
                self.human += self.INTERVAL
            elif action == "stay":
                self.old_player = self.human - 1
                self.human = self.human
            else:
                print("Invalid action")

        elif ai:
            # if agent is at one of the screen borders do not move
            if self.agent == self.SCREEN_WIDTH and action == "right":
                pass
            elif self.agent == 1 and action == "left":
                pass
            # based on chosen action move agent
            elif action == "left":
                self.old_agent = self.agent
                self.agent -= self.INTERVAL
            elif action == "right":
                self.old_agent = self.agent
                self.agent += self.INTERVAL
            elif action == "stay":
                self.old_agent = self.agent - 1
                self.agent = self.agent
            else:
                print("Invalid action")

    def update(self):
        """Make the square fall and update score."""

        # if square at bottom of screen GAME OVER
        if self.square[1] == self.SCREEN_HEIGHT - 1:
            self.done = True
        else:
            self.square[1] += 1

    def update_score(self, ai_won: int, ai_lost: int, **pl_stats):
        """Display the new score on the screen"""
        # show games won
        font = pg.font.SysFont("SFNS Display", 50)
        if ai_won == 0:
            score_text = "Games won: 0, 0.0000 "
        else:
            score_text = \
                    f"Games won: {ai_won}, {ai_won / (ai_won + ai_lost):.4f} "
        text = font.render(score_text, True, (255, 255, 255), (96,) * 3)
        textrect = text.get_rect()
        textrect.x = 0
        textrect.y = (self.SCREEN_HEIGHT + 1) * self.BLOCK
        self.display.blit(text, textrect)

        if self.duel and len(pl_stats) > 0:
            pl_stats = pl_stats["pl_stats"]
            if pl_stats[0] == 0:
                score_text = "Games won: 0, 0.0000 "
            else:
                score_text = f"Games won: {pl_stats[0]}, " + \
                        f"{pl_stats[0] / (pl_stats[0] + pl_stats[1]):.4f} "
            text = font.render(score_text, True, (255, 255, 255), (96,) * 3)
            textrect = text.get_rect()
            textrect.x = 2 * self.BLOCK + self.SCREEN_WIDTH * self.BLOCK
            textrect.y = (self.SCREEN_HEIGHT + 1) * self.BLOCK
            self.display.blit(text, textrect)

        pg.display.update()

    def show_player_titles(self):
        """Show title of players."""
        font = pg.font.SysFont("SFNS Display", 50)
        ai_text = font.render("AI", True, (255, 255, 255), (96,) * 3)
        pl_text = font.render("Player", True, (255, 255, 255), (96,) * 3)
        ai_textrect = ai_text.get_rect()
        pl_textrect = ai_text.get_rect()
        ai_textrect.x = self.BLOCK + (self.SCREEN_WIDTH / 2) * self.BLOCK
        pl_textrect.x = 2 * self.BLOCK + (self.SCREEN_WIDTH * 1.5) * self.BLOCK
        ai_textrect.y = 1
        pl_textrect.y = 1
        self.display.blit(ai_text, ai_textrect)
        self.display.blit(pl_text, pl_textrect)

        # pg.display.update()

    def render(self):
        """Render everything that needs to be seen."""

        # only on first run initialise screen
        if self.pg_init:
            if self.duel:
                width = self.BLOCK * (self.SCREEN_WIDTH * 2 + 3)
                height = self.BLOCK * (self.SCREEN_HEIGHT + 2)
            else:
                width = self.BLOCK * (self.SCREEN_WIDTH + 2)
                height = self.BLOCK * (self.SCREEN_HEIGHT + 2)
            self.display = pg.display.set_mode([width, height])
            self.display.fill((96,) * 3)
            # show player titles in duel mode
            if self.duel:
                self.show_player_titles()
                self.update_score(0, 0)

            self.pg_init = False

        # empty space
        pg.draw.rect(self.display, (236,) * 3,
                     (self.BLOCK, self.BLOCK,
                      self.SCREEN_WIDTH * self.BLOCK,
                      self.SCREEN_HEIGHT * self.BLOCK))
        # object
        pg.draw.rect(self.display, (96, 148, 188),
                     (self.BLOCK * self.square[0],
                      self.BLOCK * (self.square[1] + 1),
                      self.BLOCK, self.BLOCK))
        # player
        pg.draw.rect(self.display, (229, 0, 27),
                     (self.BLOCK * self.agent,
                      self.SCREEN_HEIGHT * self.BLOCK,
                      self.BLOCK, self.BLOCK))

        # render human player if dueling
        if self.duel:
            # empty space
            pg.draw.rect(self.display, (236,) * 3,
                             ((self.SCREEN_WIDTH + 2) * self.BLOCK, self.BLOCK,
                             self.SCREEN_WIDTH * self.BLOCK,
                             self.SCREEN_HEIGHT * self.BLOCK))
            # object
            pg.draw.rect(self.display, (229, 0, 27),
                             ((self.SCREEN_WIDTH + 1 + self.square[0]) *
                              self.BLOCK,
                              (self.square[1] + 1) * self.BLOCK,
                              self.BLOCK, self.BLOCK))
            # player
            pg.draw.rect(self.display, (96, 148, 188),
                             ((self.SCREEN_WIDTH + 1 + self.human) *
                              self.BLOCK,
                              (self.SCREEN_HEIGHT) * self.BLOCK,
                              self.BLOCK, self.BLOCK))
        pg.display.update()

    def reward(self, action: str):
        """Return the reward based on an action location and square.

        Args:
            action: Action for agent to make
        """

        # reward agent alot for moving to and staying on square and punish for
        # not going next or on square
        if self.agent == self.square[0] and action == "stay":
            return 200
        elif self.agent == self.square[0] and action == "left":
            return -100
        elif self.agent == self.square[0] and action == "right":
            return -100
        elif self.agent == self.square[0] - 1 and action == "right":
            return 100
        elif self.agent == self.square[0] + 1 and action == "left":
            return 100
        else:
            return -50

    def sample_action(self):
        """Make a random action based on the possible actions."""

        # random action
        action = np.random.choice(self.ACTIONS)
        self.make_action(action)


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

    def __init__(self):
        # to init pg
        self.pg_init = True
        self.clock = pg.time.Clock()
        pg.display.set_caption("Flappy")

        self.SCREEN_WIDTH = pg.display.Info().current_w // 5
        self.PIPE_DIFF = 240 * self.SCREEN_WIDTH // 768

        self.SCREEN_HEIGHT = 1024 * self.SCREEN_WIDTH // 768
        self.BLOCK = self.SCREEN_WIDTH // 20

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
        self.bird_y = self.SCREEN_HEIGHT // 2
        self.bird_angle = 0
        self.gravity = self.scale(2.3)
        self.velocity = 0

        # reset pipes
        self.pipes_loc = [[
            self.SCREEN_WIDTH,
            np.random.randint(self.scale(400), self.scale(860))
            ]]

        # reset ground
        # self.ground_loc = list(
        #         map(lambda x: x * 37, range(1, self.SCREEN_WIDTH // 37))
        #     )
        self.ground_loc = 1

    def update(self):
        """Bring pipes and ground forward, add new pipe if nevessary, remove
        pipe and ground if off screen, update gravity and bird position, limit
        velocity and stop game if bird at top or bottom."""

        # move pipes forward
        for pipe in self.pipes_loc:
            pipe[0] -= self.scale(8)

        # if pipe halfway or more and only one pipe add new pipe
        if len(self.pipes_loc) < 2:
            if self.pipes_loc[0][0] <= self.SCREEN_WIDTH / 2:
                self.pipes_loc.append(
                    [self.pipes_loc[0][0] + self.SCREEN_WIDTH // 2 + self.scale(140),
                     np.random.randint(self.scale(400), self.scale(860))])

        # remove pipe if off screen
        if self.pipes_loc[0][0] <= -self.scale(140):
            del self.pipes_loc[0]

        # move ground forward
        self.ground_loc -= self.scale(8)

        # remove ground if off screen and add new ground
        if self.ground_loc <= -37:
            self.ground_loc = 1

        # limit bird rotation
        if self.bird_angle <= -90 or self.bird_angle >= 90:
            self.bird_angle = 90

        # update velocity and bird position
        self.velocity += self.gravity
        self.bird_y += self.velocity

        # limit velocity to reduce drastic movement
        if self.velocity > 50:
            self.velocity = 50
        elif self.velocity < -50:
            self.velocity = -50

        # if at bottom or top, GAMEOVER
        if self.bird_y >= self.SCREEN_HEIGHT - self.scale(60):
            self.done = True

        # only check for mask collision if there is a rect collision
        for pipe in self.pipes:
            if self.bird.colliderect(pipe):
                bird_mask = pg.mask.from_surface()
                pipe_mask = pg.mask.from_surface(pipe)
                self.done = True
                # convert image to array
                # pg.surfarray.array3d(pg.display.get_surface())

        # or if gone over pipe, GAMEOVER
        if self.bird.topright[0] >= self.pipes_loc[0][0] and self.bird.y <= 0:
            self.done = True

    def render(self):
        """Render everything that needs to be seen."""
        # setup pg on first run
        if self.pg_init:
            # set window width and height
            self.display = pg.display.set_mode(
                    [self.SCREEN_WIDTH, self.SCREEN_HEIGHT + self.scale(128)])
            # load and scale bird
            self.bird_img = pg.transform.scale(
                pg.image.load("assets/bird.gif").convert_alpha(),
                (self.scale(90), self.scale(64)))
            # load and scale background
            self.bg_img = pg.transform.scale(
                    pg.image.load("assets/background.gif").convert(),
                    (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            # load and scale top pipe
            self.pipe_top_img = pg.transform.scale(
                pg.image.load("assets/pipe-top.gif").convert_alpha(),
                (self.scale(140), self.scale(628)))
            # load and scale bottom pipe
            self.pipe_bottom_img = pg.transform.scale(
                pg.image.load("assets/pipe-bottom.gif").convert_alpha(),
                (self.scale(140), self.scale(628)))
            # load and scale ground
            self.ground_img = pg.transform.scale(
                pg.image.load("assets/ground.gif").convert_alpha(),
                (self.SCREEN_WIDTH + self.scale(37), self.scale(128)))
            self.pg_init = False

        # draw background
        self.display.fill((255, 0, 0))
        self.display.blit(self.bg_img, (0, 0))

        # pipes
        self.pipes = []
        for pipe in self.pipes_loc:
            # bottom pipe
            self.pipes.append(self.display.blit(self.pipe_bottom_img,
                                                (pipe[0], pipe[1])))
            # top pipe
            self.pipes.append(self.display.blit(
                    self.pipe_top_img,
                    (pipe[0], pipe[1] - self.PIPE_DIFF - self.scale(628))))

        # ground
        self.display.blit(self.ground_img, (self.ground_loc, self.SCREEN_HEIGHT))

        # rotate bird
        self.rotated_bird = self.rotate(self.bird_img, self.bird_angle)
        # and the rect around bird
        self.rotated_bird_rect = self.rotated_bird.get_rect(
                center=(self.BLOCK * 4, self.bird_y))
        # display it
        self.bird = self.display.blit(self.rotated_bird,
                                      self.rotated_bird_rect)

        # update screen
        pg.display.update()

    def make_action(self, action):
        """Move bird."""
        if action == "up":
            self.bird_angle = -30
            self.velocity += self.scale(-24)
            # self.velocity *= self.scale(0.09)
        elif action == "stay":
            self.bird_angle += 3

        self.update()

        self.clock.tick(40)

    def get_screen(self):
        """Return the game display as an image."""
        return pg.surfarray.array3d(pg.display.get_surface())
