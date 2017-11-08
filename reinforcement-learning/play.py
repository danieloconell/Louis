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
        max_action = -1
        index = -1
        for item in env.actions:
            print(item)
            print(env.reward(item))
            if env.reward(item) > max_action:
                print("greater")
                max_action = env.reward(item)
                action = [item, index]
            else:
                index += 1
        print(action[0])
        episode_reward += env.reward(action[0])
        env.action(action[0])
        env.render()
