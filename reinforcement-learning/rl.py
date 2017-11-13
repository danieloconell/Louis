"""Basic reinforcement learning functions.
"""

from env import reward
import numpy as np
import env
import os

actions = ["left", "right", "stay"]
np.random.seed(0)   # to make results the same
gamma = 0.8         # make the agent explore a bit


def choose_action(state, type):
    """Choose action based on q table."""
    if np.random.uniform() > gamma and type == "train":
        # random action
        action = np.random.choice(actions)
        return action
    else:
        if len(set(table[env.object[0]][env.player])) == 1:
            # if all rewards are the same choose a random action
            action = np.random.choice(actions)
            return action
        action_index = np.argmax(table[env.object[0]][env.player])

        # convert action_index to string action
        for index in range(3):
            if index == action_index:
                action = actions[index]
                return action


def q(state, action):
    """Update the q table."""
    # chosen action as a number
    index = -1
    for item in actions:
        index += 1
        if item == action:
            action_n = index

    # max future reward based on action
    if action == actions[0]:
        new_value = reward(action) + gamma \
                * np.max(table[env.object[0]][env.player - 1])
    elif action == actions[1]:
        new_value = reward(action) + gamma \
                * np.max(table[env.object[0]][env.player + 1])
    elif action == actions[2]:
        new_value = reward(action) + gamma \
                * np.max(table[env.object[0]][env.player])
    else:
        print("Invalid action")

    # update q table
    table[env.object[0]][int(state)][action_n] = new_value


def save_q():
    """Locally save the q table."""
    np.save("q-table", table)


def load_q():
    """Load q table if one exists."""
    global table
    file = "q-table.npy"
    if os.path.isfile(file):
        table = np.load(file)
    else:
        table = np.zeros((28, 28, 3))
