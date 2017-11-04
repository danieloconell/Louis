"""This is the agent which currently takes the action with highest immediate reward."""

import env

for episode in range(10):
    env.reset()
    episode_reward = 0
    for t in range(100):
        observation, reward, done = env.observation
        episode_reward += reward
        if env.done:
            print(
                "Episode %d finished after %d timesteps, with reward %d"
                % ((episode + 1), (t + 1), episode_reward))
            break
        elif env.create_reward(0) > env.create_reward(1) or env.create_reward(0) > env.create_reward(2):
            print(env.create_reward(0), env.create_reward(1), env.create_reward(2))
            env.action(0)
            env.render()
            print("Action 0")
        elif env.create_reward(1) > env.create_reward(0) or env.create_reward(1) > env.create_reward(2):
            print(env.create_reward(0), env.create_reward(1), env.create_reward(2))
            env.action(1)
            env.render()
            print("Action 1")
        else:
            print(env.create_reward(0), env.create_reward(1), env.create_reward(2))
            env.action(2)
            env.render()
            print("Action 2")
