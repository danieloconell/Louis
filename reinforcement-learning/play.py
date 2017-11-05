"""This is the agent which currently takes the action with highest immediate reward."""

import pandas as pd
import numpy as np
import env

actions = ["left", "right", "stay"]

left = {x: [0]*(env.screen_width - 1) for x in range(2)}
right = {x: [0]*(env.screen_width - 1) for x in range(2)}
table = pd.DataFrame(left)

def max(list):
    max = 0
    index = 0
    for item in list:
        item += 1
        if item > max:
            max = item
    return item


"""if np.random.uniform() > epsilon or all_zero:
    action = np.random.choice(actions)
else:
    action = None"""

for episode in range(10):
    env.reset()
    episode_reward = 0
    for t in range(100):
        episode_reward += env.actual_reward
        if env.done:
            print(
                "Episode %d finished after %d timesteps, with reward %d"
                % ((episode + 1), (t + 1), episode_reward))
            break
        max_action = 0
        index = -1
        for item in actions:
            if env.create_reward(item) > max_action:
                max_action = env.create_reward(item)
                action = [item, index]
            else:
                index += 1
        print(action[0])
        episode_reward += env.create_reward(action[0])
        env.action(action[0])
        env.render()
