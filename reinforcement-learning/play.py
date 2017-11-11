"""Load the trained q table and make actions based on that.
"""

import time
import env
import rl

rl.load_q()
env.make("pygame")

while True:
    env.reset()
    for _ in range(15):
        if env.done:
            break
        action = rl.choose_action(env.player, "test")
        env.action(action)
        time.sleep(0.03)
        env.render()
