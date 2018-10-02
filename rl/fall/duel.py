import time

from env import Falling
import rl

import pygame

rl.load_q()
env = Falling(duel=True)
ai_won = ai_lost = pl_won = pl_lost = 0

while True:
    env.reset()
    while not env.done:
        env.render()
        env.update_score(ai_won, ai_lost, pl_stats=[pl_won, pl_lost])
        # why does making random move drastically increase performance
        ai_action = rl.choose_action(env.agent, env.square, train=True)
        env.make_action(ai_action, ai=True)
        time.sleep(0.05)

        # quit if the user wants and get the human players action
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    action = "left"
                elif event.key == pygame.K_RIGHT:
                    action = "right"
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    action = "stay"
            else:
                action = "stay"

        # move human player
        env.make_action(action, player=True)
        env.update()

    # keep track of how many won and lost
    if env.agent == env.square[0]:
        ai_won += 1
    else:
        ai_lost += 1

    if env.human == env.square[0]:
        pl_won += 1
    else:
        pl_lost += 1
