"""Falling environment.

The aim of this environment is to catch a falling square.  The environment is
rendered using pygame.
"""

import numpy as np
import pygame

# make results reproducible
np.random.seed(0)

# get pygame ready!
pygame.init()


class Falling:

    ACTIONS = ["left", "right", "stay"]
    BLOCK = pygame.display.Info().current_w // 50
    SCREEN_WIDTH = 22
    SCREEN_HEIGHT = 12
    INTERVAL = 1

    def __init__(self):
        """Create the environment using pygame."""

        self.pygame_init = True

    def reset(self):
        """Reset all the necessary variables for the environment."""

        # create object
        self.square = [np.random.randint(1, self.SCREEN_WIDTH + 1), 0]

        # create agent
        self.agent = (self.SCREEN_WIDTH // 2 + 1)

        # reset done
        self.done = False

    def quit(self):
        """Quit the Falling environment."""
        pygame.quit()

    def make_action(self, action: str):
        """Move agent and update acion reward.
        Args:
            action: left, right or stay.
        """

        # if agent is at one of the screen borders do not move
        if self.agent >= self.SCREEN_WIDTH or self.agent <= 0:
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

        self.update()

    def update(self):
        """Make the square fall and update score."""

        # if square at bottom of screen GAME OVER
        if self.square[1] == self.SCREEN_HEIGHT - 1:
            self.done = True
        else:
            self.square[1] += 1

    def update_score(self, won: int, lost: int):
        """Display the new score on the screen"""
        # show games won
        basicfont = pygame.font.SysFont("SFNS Display", 50)
        text = basicfont.render(f"Games won: {won}, {won / (won + lost):.6f} ",
                                True, (255, 255, 255), (96,) * 3)
        textrect = text.get_rect()
        textrect.x = 0
        textrect.y = (self.SCREEN_HEIGHT + 1) * self.BLOCK
        self.display.blit(text, textrect)

        pygame.display.update()

    def render(self):
        """Render everything that needs to be drawn."""

        # only on first run initialise screen
        if self.pygame_init:
            width = self.BLOCK * (self.SCREEN_WIDTH + 2)
            height = self.BLOCK * (self.SCREEN_HEIGHT + 2)
            self.display = pygame.display.set_mode([width, height])
            self.display.fill((96,) * 3)
            self.pygame_init = False

        # empty space
        pygame.draw.rect(self.display, (236,) * 3,
                         (self.BLOCK, self.BLOCK,
                         self.SCREEN_WIDTH * self.BLOCK,
                         self.SCREEN_HEIGHT * self.BLOCK))
        # object
        pygame.draw.rect(self.display, (96, 148, 188),
                         (self.BLOCK * self.square[0],
                          self.BLOCK * (self.square[1] + 1),
                          self.BLOCK, self.BLOCK))
        # player
        pygame.draw.rect(self.display, (229, 0, 27),
                         (self.BLOCK * self.agent,
                          (self.SCREEN_HEIGHT) * self.BLOCK,
                          self.BLOCK, self.BLOCK))
        pygame.display.update()

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
