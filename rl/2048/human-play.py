import pygame

from env import Tiles

env = Tiles()

env.reset()
while not env.done:
    env.render()
    action = "stay"

    # user actions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                action = "up"
            elif event.key == pygame.K_DOWN:
                action = "down"
            elif event.key == pygame.K_LEFT:
                action = "left"
            elif event.key == pygame.K_RIGHT:
                action = "right"

    env.make_action(action)
    # print(env.score)
    # print(f"\rFPS: {env.clock.get_fps():.2f}", end="")
