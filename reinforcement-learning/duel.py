import time

from env import Falling
import rl

import pygame

rl.load_q()
env = Falling(duel=True)
speed = 0.2
won = lost = 0

while True:
    env.reset()
    while not ai_env.done and not pl_env.done:
        ai_env.render()
        pl_env.render
        # why does making random move drastically increase performance
        ai_action = rl.choose_action(ai_env.agent, ai_env.square, train=True)
        pl_action = rl.choose_action(pl_env.agent, pl_env.square, train=True)
        ai_env.make_action(ai_action)
        pl_env.make_action(pl_action)
        time.sleep(0.03)

        # quit if the user wants
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

    # keep track of how many won and lost
    if ai_env.agent == ai_env.square[0]:
        won += 1
    else:
        lost += 1
    ai_env.update_score(won, lost)
