"""This is the agent which currently takes the action with proper q learning."""

import time
start = time.time()
from tqdm import tqdm
import env
import os
import rl
env.make("text")
episodes = 10000

import argparse
parser = argparse.ArgumentParser(description="Train agent on the falling game.")
parser.add_argument("--remove-file", help="Remove existing q table.", default=True)
parser.add_argument("--episodes", type=str, help="Number of episodes to train for.", default=10000)
args = parser.parse_args()

if args.remove_file == True:
    os.remove("q-table.npy")
    rl.load_q()
elif args.remove_file == "False":
    rl.load_q()
else:
    print("Invalid argument.")
    quit()

episodes = int(args.episodes)

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
