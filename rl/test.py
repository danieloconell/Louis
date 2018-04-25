import pygame
import cv2

from env import Flappy

env = Flappy()
episodes = 1000

for episode in range(episodes):
    env.reset()
    while not env.done:
        # see the environment
        env.render()
        # default action stay
        action = "stay"

        # user actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or pygame.K_UP:
                    action = "up"

        cv2.imshow("screen", cv2.cvtColor(cv2.resize(env.get_screen(), (80, 80)), cv2.COLOR_BGR2GRAY))
        cv2.waitKey(0)


        # apply action
        env.make_action(action)
        # print(f"\rFPS: {env.clock.get_fps():.2f}", end="")
