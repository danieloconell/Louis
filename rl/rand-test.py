import numpy as np

from env import Falling
import rl

import pygame


def dec_log(x): return 1 / np.log(x)


rl.load_q()
env = Falling()
won = lost = 0

while True:
    env.reset()
    while not env.done:
        # env.render()
        env.make_action
        # why does making random move drastically increase performance
        action = np.random.choice(env.ACTIONS)
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

    print(f"\rWon: {won}, loss: {won / (won + lost):.4f}", end="")
