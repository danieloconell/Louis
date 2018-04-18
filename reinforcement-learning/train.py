import argparse
import os

import matplotlib.pyplot as plt
from tqdm import trange

from env import Falling
import rl

# create environment and other variables
env = Falling()
won = lost = 0
won_list = []
games_list = []

# parse some arguments
parser = argparse.ArgumentParser(description="Train agent on the falling " +
                                 "environment")
parser.add_argument("--remove-file", "-r", type=bool, help="Remove existing " +
                    "q table", default=True)
parser.add_argument("--episodes", "-e", type=int, help="Number of episodes " +
                    "to train for", default=1400)
args = parser.parse_args()

# do what the arguments say
if args.remove_file and os.path.isfile("q-table.npy"):
    os.remove("q-table.npy")
    rl.load_q(new=True)
elif args.remove_file and not os.path.isfile("q-table.npy"):
    rl.load_q(new=True)

# train agent
with trange(1, args.episodes + 1) as t:
    for episode in t:
        env.reset()
        while not env.done:
            action = rl.choose_action(env.agent, env.square, train=True)
            rl.update_q(env.agent, action, env.reward(action), env.square)
            env.make_action(action)
            # env.render()  # if you want to see the training process

        # keep track of how many won and lost
        if env.agent == env.square[0]:
            won += 1
        else:
            lost += 1
        t.set_postfix(loss=f"{won / (won + lost):.2f}")
        games_list.append(won + lost)
        won_list.append(won / (won + lost))

# save trained agent
rl.save_q()

# show loss in a graph and save it
plt.plot(games_list, won_list)
plt.xlabel("Episode")
plt.ylabel("Loss")
plt.title("Falling environment")
plt.savefig("falling-env.png")
plt.show()
