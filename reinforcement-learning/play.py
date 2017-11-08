"""This is the agent which currently takes the action with highest immediate reward."""

import env
import time
env.make("pygame")

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
        for item in env.actions:
            if env.create_reward(item) > max_action:
                max_action = env.create_reward(item)
                action = [item, index]
            else:
                index += 1
        print(action[0])
        episode_reward += env.create_reward(action[0])
        env.action(action[0])
        env.render()
