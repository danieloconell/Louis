"""Basic reinforcement learning functions.
"""

from pathlib import Path
from env import reward
import numpy as np
import env
import time

actions = ["left", "right", "stay"]
gamma = 0.8 # make the agent explore a bit
np.random.seed(0) # to make results the same


def all_zero(list):
    """Return true if all item in an array are 0."""
    list = table[env.object[0]][int(list)]
    for item in list:
        if item != 0:
            return False
    return True


def choose_action(state, type):
    """Choose action based on q table."""
    if int(env.player) < env.object[0]:
        stay = [np.argmax(table[env.object[0]][int(state)]), np.max(table[env.object[0]][int(state)])]
        right = [np.argmax(table[env.object[0]][int(state) + 1]), np.max(table[env.object[0]][int(state) + 1])]
        left = [np.argmax(table[env.object[0]][int(state) - 1]), np.max(table[env.object[0]][int(state) - 1])]
    elif int(env.player) == env.object[0]:
        action = "stay"
        return action
    else:
        stay = [np.argmax(table[env.object[0]][int(state)]), np.max(table[env.object[0]][int(state)])]
        right = [np.argmax(table[env.object[0]][int(state) + 1]), np.max(table[env.object[0]][int(state) - 1])]
        left = [np.argmax(table[env.object[0]][int(state) - 1]), np.max(table[env.object[0]][int(state) + 1])]
    if type == "train":
        if np.random.uniform() > gamma or all_zero(state):
            action = np.random.choice(actions)
            return action
        else:
            if stay[1] > right[1] and left[1]:
                action = "stay"
            elif left[1] > stay[1] and right[1]:
                action = "left"
            else:
                action = "right"
            return action
    elif type == "test":
        if int(env.player) < env.object[0]:
            if stay[1] > right[1] and left[1]:
                action = "stay"
            elif left[1] > stay[1] and right[1]:
                action = "left"
            else:
                action = "right"
            return action
        else:
            if stay[1] > right[1] and left[1]:
                action = "stay"
            elif right[1] > stay[1] and left[1]:
                action = "right"
            else:
                action = "left"
            return action
    else:
        print("Invalid option")
        quit()


def q(state, action):
    """Update the q table."""
    index = -1
    for item in actions:
        index += 1
        if item == action:
            action_n = index

    # q learning
    new_value = reward(action) + gamma * np.amax(table[env.object[0]][int(env.player)])

    table[env.object[0]][int(state)][action_n] = new_value


def save_q():
    """Locally save the q table."""
    np.save("q-table", table)


def load_q():
    """Load q table if one exists."""
    global table
    table = Path("q-table.npy")
    file = "q-table.npy"
    if table.is_file():
        table = np.load(file)
    else:
        table = np.zeros((28, 28, 3))
