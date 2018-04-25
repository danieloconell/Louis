import time

from env import Falling

import pygame

env = Falling()
won = lost = 0

while True:
    env.reset()
    while not env.done:
        env.render()
        env.update_score(won, lost)
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
        env.make_action(action)
        env.update()

    # keep track of how many won and lost
    if env.agent == env.square[0]:
        won += 1
    else:
        lost += 1
