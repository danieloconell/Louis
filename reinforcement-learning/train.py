"""This is the agent which currently takes the action with highest immediate reward."""

import time
start = time.time()
from tqdm import tqdm
import env
import rl
env.make("text")
rl.load_q()
episodes = 10000

with tqdm(total=episodes) as pbar:
    for episode in range(episodes):
        env.reset()
        episode_reward = 0
        for t in range(100):
            episode_reward += env.actual_reward
            if env.done:
                pbar.update(1)
                break
            action = rl.choose_action(rl.table[env.object[0]])
            rl.q(env.player, action)
            episode_reward += env.reward(action)
            env.action(action)
            env.update()
rl.save_q()
print("Q table:")
print(rl.table[env.object[0]])
