"""Basic reinforcement learning functions.
"""

from env import reward
import pandas as pd
import numpy as np
import env

actions = ["left", "right", "stay"]
gamma = 0.9
table = np.zeros((28, 3, 28))


def all_zero(list):
    for item in list:
        for x in item:
            if x != 0:
                return False
    return True


def choose_action(state):
    """Choose action based on q table."""
    if np.random.uniform() > gamma or all_zero(state):
        action = np.random.choice(actions)
        print("zero")
        return action
    else:
        action = np.argmax(state)
        action += 1
        index_1 = int(round(action / 3))
        index_2 = int(action - index_1 * 3)
        index_1 -= 1
        index_2 -= 1
        action = state[index_1][index_2]
        return action

def q(state, action):
    """Update the q table."""
    index = -1
    for item in actions:
        index += 1
        if item == action:
            action_n = index

    # q learning
    print(new_value)
    table[env.object[0]][action_n][state] = new_value
