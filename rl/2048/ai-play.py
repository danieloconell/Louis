from random import choice

import pygame as pg

from env import Tiles

env = Tiles()
print(len(env.tiles))
n_sims = 100

env.reset()
while not env.done:

    scores = {action: [] for action in env.ACTIONS}

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    with env.simulate():
        for _ in range(n_sims):
            env.reset()
            start_move = choice(env.ACTIONS)
            env.make_action(start_move)
            while not env.sim_done:
                env.random_action()
            scores[start_move].append(env.sim_score)

    for action in scores:
        scores[action] = sum(scores[action]) / len(scores[action])

    action = max(scores.items(), key=lambda x: x[1])[0]

    env.make_action(action)
    env.render()
    # x = input(f"{env.score} next game: ")
    print(env.score)
