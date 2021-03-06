"""Load the trained q table and make actions based on that.
"""

import numpy as np

from env import Falling
import rl

import pygame


def dec_log(x): return 1 / np.log(x) if x > 0 else 0


rl.load_q()
env = Falling()
won = lost = 0

while True:
    env.reset()
    while not env.done:
        env.render()
        env.make_action
        action = rl.choose_action(env.agent, env.square)
        env.make_action(action)

        # quit if the user wants
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

    # keep track of wins and loses
    if env.agent == env.square[0]:
        won += 1
    else:
        lost += 1

    env.update_score(won, lost)
