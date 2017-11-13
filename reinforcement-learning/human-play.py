"""A version of the environment in which the user is able to play.
"""

import pygame
import time
import env
import rl

pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
rl.load_q()
env.make("pygame")
speed = 0.2
x = y = move_x = move_y = 0


def joystick():
    global x, y, move_x, move_y, running, action
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            if event.joy == 0 and event.axis == 4:
                action = "right"
            elif event.joy == 0 and event.axis == 1:
                action = "left"
            else:
                action = "stay"
        else:
            action = "stay"


while True:
    if speed >= 0.02:
        speed -= 0.05
    elif speed <= 0.005 and speed >= 0.05:
        speed -= 0.005
    elif speed <= 0.005 and speed > 0.0005:
        speed -= 0.0005
    else:
        speed = 0
    env.reset()
    for _ in range(15):
        if env.done:
            break
        joystick()
        env.action(action)
        time.sleep(0.03)
        env.render()
