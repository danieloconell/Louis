"""Load the trained q table and make actions based on that.
"""

import time
import env
import rl

rl.load_q("")
env.make("pygame")
speed = 0.2

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
        action = rl.choose_action(env.player, "test")
        env.action(action)
        time.sleep(0.03)
        env.render()
