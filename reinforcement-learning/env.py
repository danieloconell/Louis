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

    def __init__(self, duel=False):
        """Create the environment using pygame.
        Args:
            duel: Create duel between ai and human player.
        """

        self.duel = duel
        self.pygame_init = True

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
        pygame.quit()

    def make_action(self, action: str, ai=True, player=False):
        """Move agent or human player and update falling square.
        Args:
            action: Left, right or stay.
            ai: Move agent.
            player: Move player.
        """

        if self.duel and player:
            # if player is at one of the screen borders do not move
            if self.human >= self.SCREEN_WIDTH or self.human <= 0:
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

        # only update when not in duel mode
        if not self.duel:
            self.update()

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
        font = pygame.font.SysFont("SFNS Display", 50)
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
                score_text = "Games won: {pl_stats[0]}, {pl_stats[0] / (pl_stats[0] + pl_stats[1]):.4f} "
            text = font.render(score_text, True, (255, 255, 255), (96,) * 3)
            textrect = text.get_rect()
            textrect.x = 2 * self.BLOCK + self.SCREEN_WIDTH * self.BLOCK
            textrect.y = (self.SCREEN_HEIGHT + 1) * self.BLOCK
            self.display.blit(text, textrect)

        pygame.display.update()

    def show_player_titles(self):
        """Show title of players."""
        font = pygame.font.SysFont("SFNS Display", 50)
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

        # pygame.display.update()

    def render(self):
        """Render everything that needs to be drawn."""

        # only on first run initialise screen
        if self.pygame_init:
            if self.duel:
                width = self.BLOCK * (self.SCREEN_WIDTH * 2 + 3)
                height = self.BLOCK * (self.SCREEN_HEIGHT + 2)
            else:
                width = self.BLOCK * (self.SCREEN_WIDTH + 2)
                height = self.BLOCK * (self.SCREEN_HEIGHT + 2)
            self.display = pygame.display.set_mode([width, height])
            self.display.fill((96,) * 3)
            # show player titles in duel mode
            if self.duel:
                self.show_player_titles()
                self.update_score(0, 0)

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

        # render human player if dueling
        if self.duel:
            # empty space
            pygame.draw.rect(self.display, (236,) * 3,
                             ((self.SCREEN_WIDTH + 2) * self.BLOCK, self.BLOCK,
                             self.SCREEN_WIDTH * self.BLOCK,
                             self.SCREEN_HEIGHT * self.BLOCK))
            # object
            pygame.draw.rect(self.display, (229, 0, 27),
                             ((self.SCREEN_WIDTH + 1 + self.square[0]) *
                              self.BLOCK,
                              (self.square[1] + 1) * self.BLOCK,
                              self.BLOCK, self.BLOCK))
            # player
            pygame.draw.rect(self.display, (96, 148, 188),
                             ((self.SCREEN_WIDTH + 1 + self.human) *
                              self.BLOCK,
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
