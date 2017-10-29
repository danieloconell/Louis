"""This is the agen which currently takes random actions."""

import env

for episode in range(10):
    env.reset()
    for t in range(100):
        if env.create_reward(2) > env.create_reward(0) or env.create_reward(2) > env.create_reward(1):
            print("action 2")
            env.action(2)
            env.render()
        if env.create_reward(0) > env.create_reward(1) or env.create_reward(0) > env.create_reward(2):
            print("action 0")
            env.action(0)
            env.render()
        elif env.create_reward(1) > env.create_reward(0) or env.create_reward(1) > env.create_reward(2):
            print("action 1")
            env.action(1)
            env.render()
        else:
            print(env.create_reward(0), env.create_reward(1), env.create_reward(2))
            env.action(2)
            env.render()
        observation, reward, done = env.observation
        if done:
            print(
                "Episode %d finished after %d timesteps, with reward %d"
                % ((episode + 1), (t + 1), reward))
            break
