"""This is the agent which currently takes the action with highest immediate reward."""

import time
start = time.time()
import env
import rl
env.make("text")

for episode in range(1000):
    env.reset()
    episode_reward = 0
    for t in range(100):
        episode_reward += env.actual_reward
        if env.done:
            print(
                "Episode %d finished after %d timesteps, with reward %d"
                % ((episode + 1), (t + 1), episode_reward))
            break
        action = rl.choose_action(rl.table[env.object[0]])
        rl.q(env.player, action)
        print(action)
        episode_reward += env.reward(action)
        env.action(action)
        env.update()
print(rl.table[env.object[0]])
print("Finished after", str(time.time() - start), "seconds")
